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

from asyncio.log import logger
from threading import Timer
from pythonosc import udp_client, osc_server, dispatcher
import math, asyncio, threading, sys, os, csv
from tkinter import messagebox


class KatOscConfig:
    def __init__(self):
        self.osc_ip = "127.0.0.1"  # OSC network IP
        self.osc_port = 9000  # OSC network port for sending messages

        self.osc_enable_server = True  # Used to improve sync with in-game avatar and autodetect sync parameter count used for the avatar.
        self.osc_server_ip = "127.0.0.1"  # OSC server IP to listen too
        self.osc_server_port = 9001  # OSC network port for recieving messages

        self.osc_delay = 0.25  # Delay between network updates in seconds. Setting this too low will cause issues.
        self.sync_params = 4  # Default sync parameters. This is automatically updated if the OSC server is enabled.

        self.line_length = 32  # Characters per line of text
        self.line_count = 4  # Maximum lines of text


class KatOsc:
    def __init__(
        self, loop=None, file=None, logger=None, config: KatOscConfig = KatOscConfig()
    ):
        file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(file_path)
        self.logger = logger
        self.logger.info("StartKatOSC")
        self.osc_ip = config.osc_ip
        self.osc_port = config.osc_port

        self.osc_enable_server = config.osc_enable_server
        self.osc_server_ip = config.osc_server_ip
        self.osc_server_port = config.osc_server_port

        self.osc_delay = config.osc_delay
        self.sync_params = config.sync_params

        self.line_length = config.line_length
        self.line_count = config.line_count

        self.text_length = 128  # Maximum length of text
        self.sync_params_max = 35  # Maximum sync parameters
        self.old_sentence = ""

        self.pointer_count = int(self.text_length / self.sync_params)
        self.pointer_clear = 255

        self.sync_params_test_char_value = (
            97  # Character value to use when testing sync parameters
        )

        self.param_visible = "KAT_Visible"
        self.param_pointer = "KAT_Pointer"
        self.param_sync = "KAT_CharSync"

        self.osc_parameter_prefix = "/avatar/parameters/"
        self.osc_avatar_change_path = "/avatar/change"
        self.osc_text = ""
        self.target_text = ""
        # Read convert list
        try:
            with open(file, "r", encoding="UTF") as f:
                reader = csv.reader(f)
                self.letters_list = [row for row in reader]
            self.logger.info("Convertlist {} was loaded successfully".format(file))
        except:
            message = "Convertlistが見当たりません。"
            self.logger.critical(message)
            messagebox.showwarning("エラー", message)
            os._exit(1)
        self.invalid_char = "?"  # character used to replace invalid characters
        self.conv_key1 = {}
        self.conv_key2 = {}
        for i in range(0, len(self.letters_list)):
            self.conv_key1[self.letters_list[i][0]] = i % 128
            self.conv_key2[self.letters_list[i][0]] = int(i / 128)
        self.conv_key1[" "] = 0  # 応急処置　BOMの処理がうまくいかない
        # self.conv_key2[" "]=0#応急処置　BOMの処理がうまくいかない

        # Character to use in place of unknown characters
        self.invalid_char_value = self.conv_key1.get(self.invalid_char, 0)

        # --------------
        # OSC Setup
        # --------------

        # Setup OSC Client
        self.osc_client = udp_client.SimpleUDPClient(self.osc_ip, self.osc_port)
        self.osc_timer = RepeatedTimer(self.osc_delay, self.osc_timer_loop)

        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, True
        )  # Make KAT visible
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_pointer, self.pointer_clear
        )  # Clear KAT text
        for value in range(self.sync_params):
            self.osc_client.send_message(
                self.osc_parameter_prefix + self.param_sync + str(value), 0.0
            )  # Reset KAT characters sync

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
            self.osc_dispatcher.map("*", print)
            if loop == None:
                loop = asyncio.get_event_loop()
            try:
                self.osc_server = osc_server.ThreadingOSCUDPServer(
                    (self.osc_server_ip, self.osc_server_port),
                    self.osc_dispatcher,
                    loop,
                )
                threading.Thread(target=self.osc_server_start, daemon=True).start()
            except:
                message = "同時に複数の起動はできません。"
                self.logger.critical(message)
                messagebox.showwarning("エラー", message)
                os._exit(1)
        # Start timer loop
        self.osc_timer.start()

    # Set the text to any value
    def set_text(self, text: str):
        text = self.remove_offensive_word(text)
        self.target_text = text

    # Avoid Recognition/translation problem
    def remove_offensive_word(self, text: str):
        # nglist_en is retrived from https://www.freewebheaders.com/full-list-of-bad-words-banned-by-google/
        # nglist_jp is retrieved from https://dic.nicovideo.jp/a/%E3%83%8B%E3%82%B3%E3%83%8B%E3%82%B3%E7%94%9F%E6%94%BE%E9%80%81%3A%E9%81%8B%E5%96%B6ng%E3%83%AF%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7
        with open("setting/nglist_en.csv", "r", encoding="UTF") as f:
            nglist_en = csv.reader(f, delimiter=",")
            for row in nglist_en:
                text = self.remove_from_list_en(row, text)
        with open("setting/nglist_jp.csv", "r", encoding="UTF") as f:
            nglist_jp = csv.reader(f, delimiter=",")
            for row in nglist_jp:
                text = self.remove_from_list_jp(row, text)
        return text

    def remove_from_list_en(self, list, text):
        temp_text =""
        for word in text.split(" "):
            for ng in list:
                ng_title = ng.title()
                if word.replace("/n","") == ng:
                    word = word.replace(ng, ng[0] + "x" * (len(ng) - 1))
                if word.replace("/n","") == ng_title:
                  word = word.replace(ng_title, ng_title[0] + "x" * (len(ng) - 1))
            temp_text =temp_text+" "+"".join(word)
        return temp_text

    def remove_from_list_jp(self, list, text):
        for ng in list:
            text = text.replace(ng, "x" * (len(ng)))
        return text

    # Syncronisation loop
    def osc_timer_loop(self):
        gui_text = self.target_text

        # Test parameter count if an update is requried
        if self.osc_enable_server:
            if self.osc_server_test_step > 0:
                # Keep text cleared during test
                self.osc_client.send_message(
                    self.osc_parameter_prefix + self.param_pointer, self.pointer_clear
                )

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
            self.osc_client.send_message(
                self.osc_parameter_prefix + self.param_pointer, self.pointer_clear
            )
            self.osc_text = " ".ljust(self.text_length)
            return

        # Make sure KAT is visible even after avatar change
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, True
        )

        # Pad line feeds with spaces for OSC
        text_lines = gui_text.split("\n")
        for index, text in enumerate(text_lines):
            text_lines[index] = self._pad_line(text)
        gui_text = self._list_to_string(text_lines)

        # Pad text with spaces up to the text limit
        gui_text = gui_text.ljust(int(self.text_length))
        gui_text = gui_text[
            0 : int(self.text_length / 2)
        ]  # cut sentence longer than 64
        gui_text += gui_text
        osc_text = self.osc_text.ljust(self.text_length)

        # Text syncing
        if gui_text != self.osc_text:  # GUI text is different, needs sync
            osc_chars = list(osc_text)

            for pointer_index in range(self.pointer_count):
                # Check if characters within this pointer are different
                equal = True
                for char_index in range(self.sync_params):
                    index = (pointer_index * self.sync_params) + char_index

                    if gui_text[index] != osc_text[index]:
                        equal = False
                        break

                if (
                    equal == False
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
                        if index < 64:
                            key = self.conv_key1.get(gui_char, None)
                            if key == None:
                                key = self.invalid_char_value
                                self.logger.warning(
                                    "illegal letter {} detected. Replaced with ?".format(
                                        gui_char
                                    )
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

                    self.osc_text = self._list_to_string(osc_chars)
                    if self.old_sentence != gui_text:
                        self.logger.info(
                            "Sent {}".format(
                                gui_text[0 : int(self.text_length / 2)].rstrip()
                            )
                        )
                        self.old_sentence = gui_text
                    return

    # Starts the OSC server
    def osc_server_start(self):
        self.osc_server.serve_forever(2)

    # Handle OSC server to detect the correct sync parameters to use
    def osc_server_handler_char(self, address, value, *args):
        if self.osc_server_test_step > 0:
            length = len(self.osc_parameter_prefix + self.param_sync)
            self.sync_params = max(self.sync_params, int(address[length:]) + 1)

    # Handle OSC server to retest sync on avatar change
    def osc_server_handler_avatar(self, address, value, *args):
        self.osc_server_test_step = 1

    # Combines an array of strings into a single string
    def _list_to_string(self, string: str):
        return "".join(string)

    # Pads the text line to its effective length
    def _pad_line(self, text: str):
        return text.ljust(self._get_padded_length(text))

    # Gets the effective padded length of a line
    def _get_padded_length(self, text: str):
        lines = max(math.ceil(len(text) / self.line_length), 1)
        return self.line_length * lines

    # Stop the timer and hide the text overlay
    def stop(self):
        self.osc_timer.stop()
        self.hide()

    # Restart the timer for syncing texts and show the overlay
    def start(self):
        self.osc_timer.start()
        self.show()

    # show overlay
    def show(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, True
        )  # Hide KAT

    # hide overlay
    def hide(self):
        self.osc_client.send_message(
            self.osc_parameter_prefix + self.param_visible, False
        )  # Hide KAT


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
