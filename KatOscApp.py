# K's Avatar Text
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


from ast import arg
from tkinter import Tk, Text, Button,Checkbutton,BooleanVar
import math
import sys
import time
import katosc_kanji
from hook_for_voiceroid2 import Make_sound
# import re
import winsound
import requests
import threading
import asyncio
import vosk_rec

class KatOscApp:
	def __init__(self,loop=None):
		self.kat = katosc_kanji.KatOsc(loop=loop)
		self.Make_sound=Make_sound(_who_speak=6)
		self.text_length = self.kat.text_length
		self.line_length = self.kat.line_length
		self.line_count = self.kat.line_count
		self.old_sentence=""
		# self.p = re.compile('[a-zA-Z]+$')
		# --------------
		# GUI Setup
		# --------------
		self.window = window = Tk()
		window.title("Subtiles for VRChat")
		# window.geometry("525x140")
		window.configure(bg = "#333")
		window.resizable(False, False)

		filepath = sys.argv[0]
		try:
			window.iconbitmap(filepath)
		except:
			print("Warning: Could not load icon from " + filepath)

		# Create text box
		global full
		full = False

		self.gui_text = Text(window,
			font = ("Courier New", 24),
			width = 28,
			height = 2,
			border = 0,
			wrap = "char",
			fg = "#fff",
			bg = "#222",
			insertbackground = "#fff"
		)
		self.gui_text.grid(column = 0, row = 0, padx = 0, pady = 10)
		self.gui_text.bind_all('<Key>', self._limit_text_length)

		# Create clear button
		self.gui_clear = Button(window,
			text = "Clear",
			command = lambda:self.set_text(""),
			border = 0,
			fg = "#ddd",
			bg = "#444",
			width = 16,
			height = 2
		)
		# self.gui_clear.grid(column = 1, row = 1, padx = 0, pady = 0, sticky = "ne")
		# self.gui_clear.grid(column = 0, row = 1, padx = 0, pady = 0, sticky = "ne")

		# Create cheack button
		self.bln = BooleanVar()
		self.bln.set(True)
		self.gui_voice = Checkbutton(window,
			text = "Voice",
			 variable=self.bln,
			border = 0,
			width = 16,
			bg = "#444",
			height = 2
		)
		# self.gui_voice.grid(column = 1, row = 0, padx = 0, pady = 0)

		# Start App
		self.window.mainloop()
			# self.foreground()
		# Stop App
		self.kat.stop()

	# def foreground(self):
	# 	hwnd = ctypes.windll.user32.FindWindowW("Subtiles for VRChat", 0)
	# 	win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
	# 	#2つ目の要素の内容
	# 	#HWND_TOPMOST:ウィンドウを常に最前面にする。
	# 	#HWND_BOTTOM:ウィンドウを最後に置く。
	# 	#HWND_NOTOPMOST:ウィンドウの最前面解除。
	# 	#HWND_TOP:ウィンドウを先頭に置く。

	# 	left, top, right, bottom = win32gui.GetWindowRect(hwnd)
	# 	win32gui.SetForegroundWindow(hwnd)
	# 	pyautogui.moveTo(left+60, top + 10)
	# 	pyautogui.click()


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
			if index == len(text_lines) - 1: # Do not add padding to the last line
				length_padded += len(text)
			else:
				length_padded += self._get_padded_length(text)

		# Delete text if it's too long
		if length_padded >= 32:
			self.gui_text.delete("end-" + str(length_padded - 32 + 1) + "c", "end")
			self.present_sentence=self.gui_text.get(1.0, "end")+"\n"
			self.set_text("")
		else:
			self.present_sentence=self.gui_text.get(1.0, "end")+"\n"
		# Send text
		self.kat.set_text(self.present_sentence)
		#Windowsの音声認識を利用する際の処理
		#？と。の存在は文の終わりを示している
		#文章が終わったら音声を読み上げ、任意の秒数字幕を表示してから文章を削除する
		# eng=self.p.search(self.present_sentence)
		# print(self.present_sentence,eng)
		if "早くしゃべります。" in self.present_sentence:
					self.Make_sound.vc.param.speed = 1.987
					self.Make_sound.vc.param.pitch = 1.911
		if "普通にしゃべります。" in self.present_sentence:
					self.Make_sound.vc.param.speed = 0.987
					self.Make_sound.vc.param.pitch =  1.111
		if "音声オフ" in self.present_sentence:
					self.bln.set(False)
					self.set_text("")
		if "？" in self.present_sentence or "。" in self.present_sentence or "." in self.present_sentence or "?" in self.present_sentence:
			if self.present_sentence==self.old_sentence:
				pass
			else:
				if (self.bln.get()):
					if "何言ってんだこいつ？" in self.present_sentence:
						self.play_exvoice(r"D:\Documents\投稿動画\素材\kiritan_exVOICE\0よく使うやつ\なにいってんだこいつ。.wav")
					elif "ありがとうございます。" in self.present_sentence:
						self.play_exvoice(r"D:\Documents\投稿動画\素材\kiritan_exVOICE\挨拶・相槌\ありがとうございます　興奮.wav")
					else:
						##翻訳機能実装の試み
						# url_base="https://script.google.com/macros/s/AKfycbwQQzNfDj9-Oou2-xTC7lrH6WbQakX2La89fVJ6z_i7XiX5WhoWUZIrbxDIFKkI6AzG/exec?text="
						# url=url0+self.gui_text.get(1.0, "end")+"&source=ja&target=en"
						# lang_from="ja"
						# lang_to="en"
						# url=url_base+self.gui_text.get(1.0, "end")+"&source="+lang_from+"&target="+lang_to
						# res=requests.get(url)
						# # res.text="テスト用"
						# self.present_sentence=res.text
						self.Make_sound.speech(self.present_sentence)
						# self.kat.set_text(self.present_sentence)
						# self.kat.set_text(self.present_sentence)
						# time.sleep(3)#ここなんとかしたい　フリーズっぽい
				if "音声オン" in self.present_sentence:
					self.bln.set(True)
				self.old_sentence=self.present_sentence
			time.sleep(4)#ここなんとかしたい　フリーズっぽい
			self.set_text("")

	# Gets the effective padded length of a line
	def _get_padded_length(self, text: str):
		lines = max(math.ceil(len(text) / self.line_length), 1)
		return self.line_length * lines
	def change_voie(self,_who_speak):
		del self.Make_sound
		self.Make_sound=Make_sound(_who_speak)
	def play_exvoice(Self,path):
		with open(path, 'rb') as f:
			data = f.read()
			winsound.PlaySound(data, winsound.SND_MEMORY)



if __name__ == "__main__":
	# thread1=threading.Thread(target=KatOscApp,kwargs={"loop":asyncio.get_event_loop()})
	thread2=threading.Thread(target=vosk_rec.Vosk_rec)
	thread2.start()
	# thread1.start()
	thread3=threading.Thread(target=KatOscApp,kwargs={"loop":asyncio.get_event_loop()})
	thread3.start()