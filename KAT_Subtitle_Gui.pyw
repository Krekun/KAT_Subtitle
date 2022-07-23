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

from tkinter import Tk, Text, Button, messagebox, filedialog
import math
import time
import threading
import queue
import os
import sys
import json
from logging import getLogger, config

import KAT_Subtitle_Lib
import KAT_Subtitle_Websocket

# main class
# A class that creates a GUI.
class KATSubtitleGui:

    # A GUI that allows you to enter text and send it to the KAT.
    def __init__(self, loop=None, _use_chrome=False):
        # Call Library
        file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(file_path)
        with open("log_config.json", "r", encoding="UTF") as f:
            log_conf = json.load(f)
        config.dictConfig(log_conf)
        logger = getLogger(__name__)
        logger.info("Start KAT_GUI")
        title = "convertlistを選択"
        filetypes = [("CSVファイル", "*.csv")]
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            title=title, filetypes=filetypes, initialdir=file_path
        )
        self.kat = KAT_Subtitle_Lib.KatOsc(loop=loop, file=file, logger=logger)
        # Call Websocket
        self.q_sentence = queue.Queue()
        Threading_chrome = threading.Thread(
            target=KAT_Subtitle_Websocket.Websocket, kwargs={"queue": self.q_sentence}
        )
        Threading_chrome.start()
        self.text_length = self.kat.text_length
        self.line_length = self.kat.line_length
        self.line_count = self.kat.line_count
        self.old_sentence = ""
        self.present_sentence = ""
        self.queue = queue  # for multi threading
        self.max_letter_length = 64  # max length of a sentence
        self._use_chrome = _use_chrome
        self.delay = 0.25  #
        if _use_chrome:
            KAT_Subtitle_Lib.RepeatedTimer(self.delay, self.chrome_to_KAT)
        # --------------
        # GUI Setup
        # --------------
        self.window = window = Tk()
        window.title("KAT Subtile")
        # window.geometry("525x140")
        window.configure(bg="#333")
        window.resizable(False, False)
        # Create text box
        self.gui_text = Text(
            window,
            font=("Courier New", 24),
            width=28,
            height=2,
            border=0,
            wrap="char",
            fg="#fff",
            bg="#222",
            insertbackground="#fff",
        )
        self.gui_text.grid(column=0, row=0, padx=0, pady=10)
        self.gui_text.bind_all("<Key>", self._limit_text_length)

        # Create clear button
        self.gui_clear = Button(
            window,
            text="Clear",
            command=lambda: self.set_text(""),
            font=("Arial", 10),
            border=5,
            fg="#ddd",
            bg="#444",
            width=16,
            height=6,
        )
        self.gui_clear.grid(column=1, row=0, padx=0, pady=0, sticky="ne")

        # Start App
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.mainloop()

    # A function that asks if you want to close the window.
    def close_window(self):
        if messagebox.askokcancel("確認", "本当に閉じていいですか？"):
            self.set_text("")
            os._exit(0)

    # For Chrome  web speech API
    def chrome_to_KAT(self):
        if not self.q_sentence.empty():
            # check if sentence is json or not
            var = self.q_sentence.get().replace('"', "")
            if "/avatar/" in var:
                address, value = var.split(",")
                print(address, value)
                try:
                    value = float(value)
                except ValueError:
                    value = int(value)
                self.kat.osc_client.send_message(address, value)
            else:
                self.set_text(var)

    # Set the text to any value
    def set_text(self, text: str):

        self.kat.set_text(text)
        self.gui_text.delete(1.0, "end")
        self.gui_text.insert(1.0, text)
        self._limit_text_length()
        self.gui_text.focus_set()

    # Limits the text length of the text box
    def _limit_text_length(self, *args):
        # Prevent too many line feeds
        self.gui_text.delete(2.0, "end")

        # Grab the text from the text box
        gui_text_original = self.gui_text.get(1.0, "end")
        text_lines = gui_text_original.split("\n")

        # Remove that empty line at the end
        if len(text_lines[len(text_lines) - 1]) == 0:
            text_lines = text_lines[:-1]

        # Calculate effective text length
        length_padded = 0
        for index, text in enumerate(text_lines):
            if index == len(text_lines) - 1:  # Do not add padding to the last line
                length_padded += len(text)
            else:
                length_padded += self._get_padded_length(text)

        # Delete text if it's too long
        if length_padded > self.max_letter_length:
            self.gui_text.delete("end-" + str(length_padded - 32 + 1) + "c", "end")
            self.present_sentence = self.gui_text.get(1.0, "end") + "\n"
            self.set_text("")
        else:
            self.present_sentence = self.gui_text.get(1.0, "end") + "\n"
        # Send text
        self.kat.set_text(self.present_sentence)
        # process for windows 11 voice input
        # ? and 。 mean the end of a sentence
        # After texting a sentence, show the sentence for seconds then  remove it.
        if (
            "？" in self.present_sentence
            or "。" in self.present_sentence
            or "." in self.present_sentence
            or "?" in self.present_sentence
        ):
            if self.present_sentence == self.old_sentence:
                pass
            else:
                self.old_sentence = self.present_sentence
            time.sleep(2)  # Keep showing a sentence
            self.set_text("")

    # Gets the effective padded length of a line
    def _get_padded_length(self, text: str):
        lines = max(math.ceil(len(text) / self.line_length), 1)
        return self.line_length * lines


if __name__ == "__main__":
    app = KATSubtitleGui(_use_chrome=True)
