# Kuretan Avatar Text
# Copyright (C) 2022 Kuretan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from logging import raiseExceptions
from threading import Timer
from time import sleep
import math
import asyncio
import threading
import sys
import os
import csv
from tkinter import messagebox
from dataclasses import dataclass
from typing import Any

from pythonosc import udp_client, osc_server, dispatcher


@dataclass(frozen=False)
class KatOscConfig:
    """
    store the configuration for the OSC
    """

    osc_ip: str = "127.0.0.1"  # OSC network IP
    osc_port: int = 9000  # OSC network port for sending messages

    osc_enable_server: bool = True  # Used to improve sync with in-game avatar and autodetect sync parameter count used for the avatar.
    osc_server_ip: str = "127.0.0.1"  # OSC server IP to listen too
    osc_server_port: str = 9001  # OSC network port for recieving messages

    osc_delay: float = 0.20  # Delay between network updates in seconds. Setting this too low will cause issues.
    sync_params: int = 4  # Default sync parameters. This is automatically updated if the OSC server is enabled.
    line_length: int = 32  # Characters per line of text
    text_length: int = 256  # Maximum length of text
    sync_wait: float = 0.10  # Waitting time between sendings. longer, less sync bug ?
    # pointer_count: int = int(text_length / sync_params)
    file: str = None
    loop: Any = None
    logger_object: Any = None

    def __post_init__(self):
        """
        Validate inputs
        """
        variables = [
            self.osc_delay,
            self.sync_params,
            self.line_length,
            self.text_length,
        ]
        for value in variables:
            if value <= 0:
                raise ValueError("Parametrs should be valid number")


class KatOsc:
    def __init__(self, config: KatOscConfig = KatOscConfig()):
        file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(file_path)

        self.ismicmute = False
        self.file = config.file
        self.loop = config.loop
        self.logger = config.logger_object

        self.logger.info("StartKatOSC")
        self.osc_ip = config.osc_ip
        self.osc_port = config.osc_port

        self.osc_enable_server = config.osc_enable_server
        self.osc_server_ip = config.osc_server_ip
        self.osc_server_port = config.osc_server_port

        self.osc_delay = config.osc_delay
        self.sync_wait = config.sync_wait
        self.sync_params = config.sync_params

        self.line_length = config.line_length  # Characters per line of text
        self.text_length = config.text_length  # Maximum length of text

        self.sync_params_max = 25  # Maximum sync parameters
        self.old_sentence = ""

        self.pointer_count = int(self.text_length / self.sync_params)
        self.pointer_clear = 255

        self.sync_params_test_char_value = (
            97  # Character value to use when testing sync parameters
        )

        self.param_visible = "KAT_Visible"
        self.param_pointer = "KAT_Pointer"
        self.param_sync = "KAT_CharSync"
        self.param_loading = "KAT_Loading"

        self.osc_parameter_prefix = "/avatar/parameters/"
        self.osc_avatar_change_path = "/avatar/change"
        self.osc_text = ""
        self.target_text = ""

        self.invalid_char = "?"  # character used to replace invalid characters
        self.conv_key1 = {}
        self.conv_key2 = {}
        self.read_convertlist()

        # --------------
        # OSC Setup
        # --------------

        # Setup OSC Client
        self.osc_client = udp_client.SimpleUDPClient(self.osc_ip, self.osc_port)
        self.osc_timer = RepeatedTimer(self.osc_delay, self.osc_timer_loop)

        # Clear KAT text
        self._clear_text()
        # Reset KAT characters sync
        for value in range(self.sync_params):
            self.osc_client.send_message(
                self.osc_parameter_prefix + self.param_sync + str(value), 0.0
            )

        # Setup OSC Server
        if self.osc_enable_server:
            self.osc_server_test_step = 1
            self.sync_params = 0

            self.osc_dispatcher = dispatcher.Dispatcher()
            self.osc_dispatcher.map(
                self.osc_parameter_prefix + self.param_sync + "*",
                self.osc_server_handler_char,
            )
            self.osc_dispatcher.map(
                self.osc_avatar_change_path + "*", self.osc_server_handler_avatar
            )
            self.osc_dispatcher.map("/avatar/parameters/MuteSelf", self.toggle_mic)
            # self.osc_dispatcher.map("/avatar/change", print)
            if self.loop is None:
                self.loop = asyncio.get_event_loop()
            try:
                self.osc_server = osc_server.ThreadingOSCUDPServer(
                    (self.osc_server_ip, self.osc_server_port),
                    self.osc_dispatcher,
                    self.loop,
                )
                threading.Thread(target=self.osc_server_start, daemon=True).start()
            except OSError:
                message = "同時に複数の起動はできません。\n You cannot run two KAT Subtitles at the same time"
                original_message = "OSError: [WinError 10048] Only one usage of each socket address\
                 (protocol/network address/port) is normally permitted"
                self.logger.critical(original_message)
                messagebox.showwarning("エラー", message)
                os._exit(1)

        # Start timer loop
        self.osc_timer.start()

    def read_convertlist(self):
        """
        Read convert list
        """
        try:
            with open(self.file, "r", encoding="UTF") as f:
                reader = csv.reader(f)
                self.letters_list = [row for row in reader]
            self.logger.info(f"Convertlist {self.file} was loaded successfully")
        except AttributeError:
            message = "Convertlistが見当たりません。 Convertlist is missing."
            self.logger.critical(message)
            messagebox.showwarning("エラー", message)
            os._exit(1)

        # KAT uses two letters to show one letter such as a,1 ->あ
        # you need to convert letters into a pair of letters such as あ　->a,1
        for i, key in enumerate(self.letters_list):
            self.conv_key1[key[0]] = i % 128
            self.conv_key2[key[0]] = int(i / 128)
        self.conv_key1[" "] = 0  # ad-hoc fix
        # Character to use in place of unknown characters
        self.invalid_char_value = self.conv_key1.get(self.invalid_char, 0)

    def change_convertlist(self, file):
        """
        Change convertlist over using KAT
        """
        self.file = file
        self.read_convertlist()
        self.logger.info("Change convertlist ")

    def change_text_length(self, text_length):
        """
        change_text_length
        """
        if text_length <= 0:
            raise ValueError(f"text_length {text_length} should be valid number")
        self.text_length = text_length  # Maximum length of text
        self.pointer_count = int(self.text_length / self.sync_params)
        self.logger.info("text_length changed")

    def change_sync_wait(self, sync_wait):
        if sync_wait <= 0:
            raise ValueError(f"sync_wait {sync_wait} should be valid number")
        self.sync_wait = sync_wait
        self.logger.info("sync_wait changed")

    def change_line_length(self, line_length):
        if line_length <= 0:
            raise ValueError(f"line_length {line_length} should be valid number")
        self.line_length = line_length
        self.logger.info("line_length changed")

    def toggle_mic(self, _: str, muteself: bool) -> None:
        """
        Get the status of mic from OSC
        _:addres of mic -> "/avatar/parameters/MuteSelf"
        muteself: bool, true means mute
        """
        self.ismicmute = muteself

    def set_text(self, text: str):
        """
        Remove offensive words from input
        """
        text = self.remove_offensive_word(text)
        self.target_text = text

    def remove_offensive_word(self, text: str) -> str:
        """
        Read list of offensive words and remove the offensive words from the text.

        :param text: The text to be checked
        :return: The text that has been removed of offensive words.

        nglist_en is retrived from https://www.freewebheaders.com/full-list-of-bad-words-banned-by-google/
        nglist_jp is retrieved from https://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E7%94%9F%E6%94%BE%E9%80%81%3A%E9%81%8B%E5%96%B6ng%E3%83%AF%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7
        """
        with open("setting/nglist_en.csv", "r", encoding="UTF") as f:
            nglist_en = csv.reader(f, delimiter=",")
            for row in nglist_en:
                text = self.remove_from_list_en(row, text)
        with open("setting/nglist_jp.csv", "r", encoding="UTF") as f:
            nglist_jp = csv.reader(f, delimiter=",")
            for row in nglist_jp:
                text = self.remove_from_list_jp(row, text)
        return text

    def remove_from_list_en(self, row: list[str], text: str) -> str:
        """
        Replacing NG words like  Fuck -> Fxxx
        """
        temp_text = ""
        for word in text.split(" "):
            for ng in row:
                ng_title = ng.title()
                if word.replace("/n", "") == ng:
                    word = word.replace(ng, ng[0] + "x" * (len(ng) - 1))
                if word.replace("/n", "") == ng_title:
                    word = word.replace(ng_title, ng_title[0] + "x" * (len(ng) - 1))
            if temp_text != "":
                temp_text = temp_text + " " + "".join(word)
            else:
                temp_text = "".join(word)
        return temp_text

    def remove_from_list_jp(self, row: list[str], text: str) -> str:
        """
        Replace  NG words like あほ -> xx
        """
        for ng in row:
            text = text.replace(ng, "x" * (len(ng)))
        return text

    def osc_timer_loop(self) -> None:
        """
        Syncronisation loop
        This loop transmit texts to VRChat.

        """
        gui_text = self.target_text

        if self.osc_enable_server:
            if self.osc_server_test_step > 0:
                # Keep text cleared during test
                self._clear_text()

                if self.osc_server_test_step == 1:
                    # Reset sync parameters count
                    self.sync_params = 0

                    # Reset character text values
                    for char_index in range(self.sync_params_max):
                        self.osc_client.send_message(
                            self.osc_parameter_prefix
                            + self.param_sync
                            + str(char_index),
                            0.0,
                        )
                    self.osc_server_test_step = 2
                    return

                elif self.osc_server_test_step == 2:
                    # Set characters to test value
                    for char_index in range(self.sync_params_max):
                        self.osc_client.send_message(
                            self.osc_parameter_prefix
                            + self.param_sync
                            + str(char_index),
                            self.sync_params_test_char_value / 127.0,
                        )
                    self.osc_server_test_step = 3
                    return

                elif self.osc_server_test_step == 3:
                    # Finish the parameter sync test
                    if self.sync_params == 0:
                        self.logger.warning("self.sync_params=0")
                        self.sync_params = 4  # Test failed, assume default of 4 params
                    self.pointer_count = int(self.text_length / self.sync_params)
                    self.osc_server_test_step = 0
                    self.osc_text = " ".ljust(self.text_length)  # Resync letters

        # Do not process anything if sync parameters are not setup
        if self.sync_params == 0:
            return

        # Sends clear text message if all text is empty
        if gui_text.strip("\n").strip(" ") == "":
            self._clear_text()
            self.osc_text = " ".ljust(self.text_length)
            return

        # Pad line feeds with spaces for OSC
        text_lines = gui_text.split("\n")
        for index, text in enumerate(text_lines):
            text_lines[index] = self._pad_line(text)
        gui_text = self._list_to_string(text_lines)

        # Pad text with spaces up to the text limit
        gui_text = gui_text.ljust(int(self.text_length))
        gui_text = gui_text[0 : int(self.text_length / 2)]
        gui_text += gui_text
        osc_text = self.osc_text.ljust(self.text_length)

        # Text syncing
        # If you send texts too quickly, it gets garbled
        # You need wait during OSC sendings
        # Waitting time depends on situations.

        if gui_text != self.osc_text:  # GUI text is different, needs sync
            self.stop_timer()
            # Keep text clear to avoid a text garbling
            self._clear_text()
            sleep(0.1)  # You need wait till the text get cleared.
            self.load_start()
            osc_text = "".ljust(self.text_length)
            osc_chars = list(osc_text)

            for pointer_index in range(self.pointer_count):
                # Check if characters is space
                equal = True
                for char_index in range(self.sync_params):
                    index = (pointer_index * self.sync_params) + char_index

                    if gui_text[index] != " ":
                        equal = False
                        break

                if (
                    not equal
                ):  # Characters not equal, need to sync this pointer position

                    self.osc_client.send_message(
                        self.osc_parameter_prefix + self.param_pointer,
                        pointer_index + 1,
                    )  # Set pointer position
                    # Loop through characters within this pointer and set them
                    for char_index in range(self.sync_params):
                        index = (pointer_index * self.sync_params) + char_index
                        gui_char = gui_text[index]
                        # Convert character to the key value, replace invalid characters
                        if index < int(self.text_length / 2):
                            key = self.conv_key1.get(gui_char, None)
                            if key is None:
                                key = self.invalid_char_value
                                self.logger.warning(
                                    f"invalid letter {gui_char} detected. Replaced with ?"
                                )

                        else:
                            key = self.conv_key2.get(gui_char, 0)

                        # Calculate character float value for OSC
                        value = float(key)
                        if value > 127.5:
                            value = value - 256.0
                        value = value / 127.0

                        self.osc_client.send_message(
                            self.osc_parameter_prefix
                            + self.param_sync
                            + str(char_index),
                            value,
                        )
                        osc_chars[
                            index
                        ] = gui_char  # Apply changes to the networked value
                        sleep(
                            0.001
                        )  # Don't send OSC at the same time. Just wait 0.001 sec
                    sleep(self.sync_wait)  # wait till the job done
                    self.osc_text = self._list_to_string(osc_chars)
                    if self.old_sentence != gui_text:
                        self.old_sentence = gui_text
            self.osc_text = gui_text
            self.load_end()
            self.show()
            self.start_timer()
        return

    def osc_server_start(self) -> None:
        """
        Starts the OSC server
        """
        self.osc_server.serve_forever(2)

    def osc_server_handler_char(self, address, value, *args) -> None:
        """
        Handle OSC server to detect the correct sync parameters to use
        """
        if self.osc_server_test_step > 0:
            length = len(self.osc_parameter_prefix + self.param_sync)
            self.sync_params = max(self.sync_params, int(address[length:]) + 1)
            # self.logger.info(f"sync params ={self.sync_params}")

    def osc_server_handler_avatar(self, address, value, *args) -> None:
        """
        Handle OSC server to retest sync on avatar change
        """
        self.osc_server_test_step = 1

    # Combines an array of strings into a single string
    def _list_to_string(self, string: str) -> str:
        return "".join(string)

    # Pads the text line to its effective length
    def _pad_line(self, text: str) -> str:
        return text.ljust(self._get_padded_length(text))

    # Gets the effective padded length of a line
    def _get_padded_length(self, text: str) -> str:
        lines = max(math.ceil(len(text) / self.line_length), 1)
        return self.line_length * lines

    def _clear_text(self) -> None:
        self.osc_text = " ".ljust(self.text_length)
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_pointer, self.pointer_clear
        )
        self.hide()

    # Stop the timer and hide the text overlay
    def stop_timer(self):
        self.osc_timer.stop()
        self.hide()

    # Restart the timer for syncing texts and show the overlay
    def start_timer(self):
        self.osc_timer.start()
        self.show()

    # show overlay
    def show(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, True
        )

    # hide overlay
    def hide(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, False
        )

    def load_start(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_loading, True
        )

    def load_end(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_loading, False
        )


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
