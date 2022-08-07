from logging import getLogger, config
import json
import os
import glob
import sys
import json
from tkinter import Tk, filedialog
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import KAT_Subtitle_editdatabase
import KAT_Subtitle_Lib
import KAT_Subtitle_Gui

# Setting Log file
PRESENT_LOCATION = os.path.dirname(os.path.abspath(sys.argv[0]))
with open("log_config.json", "r", encoding="UTF") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)
logger.info("Start FAST_api")
CONFIGFILES = glob.glob(
    os.path.expanduser("~") + "\\AppData\\LocalLow\\VRChat\\VRChat\\OSC\\\**\\*.json",
    recursive=True,
)
#
# run external library


def get_conver_file(present_location: str) -> str:
    """
    It opens a file dialog box and returns the path of the file selected by the user

    :param PRESENT_LOCATION: The path to the folder where the file is located
    :return: The file path of the file that the user selected.
    """
    # title = "convertlistを選択"
    # filetypes = [("CSVファイル", "*.csv")]
    # root = Tk()
    # root.withdraw()
    # file = filedialog.askopenfilename(
    #     title=title, filetypes=filetypes, initialdir=PRESENT_LOCATION
    # )
    file = r"C:\Users\baryo\Documents\Vrchat\KAT\KAT_Subtitle\ラノベPOP v2__77lines_converter.csv"
    return file


CONVERT_FILE = get_conver_file(PRESENT_LOCATION)
Lib = KAT_Subtitle_Lib.KatOsc(file=CONVERT_FILE, logger=logger)
# threading_gui = threading.Thread(
#     target=KAT_Subtitle_Gui.KATSubtitleGui, kwargs={"logger": logger, "kat": Lib}
# )
# threading_gui.start()
#############


edit_database = KAT_Subtitle_editdatabase.edit_database()
app = FastAPI()
# To avoid a CORS problem
# https://qiita.com/satto_sann/items/0e1f5dbbe62efc612a78
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    api_name: str
    url: str

class TextMessage(BaseModel):
    text_type: str
    text_message: str

class spoken_sentece(BaseModel):
    spoken_sentece: str

@app.get("/api_key/")
def post_api_key() -> dict[str, str]:
    """
    It gets the api_key from the database and returns it as a dictionary.
    :return: A dictionary with the api_type as the key and the api_key as the value.
    """
    apilist = ("DeepL_auth", "GAS_URL")
    dic = {}
    for api_type in apilist:
        api_key = edit_database.get_api_table(api_type)
        dic[api_type] = api_key
    return dic


@app.post("/api_key/")
async def update_api_key(item: Item) -> None:
    edit_database.update_api_table(item.api_name, item.url)


@app.post("/text-message/")
def post_text_message(textmessage: TextMessage) -> None:
    # raise HTTPException(status_code=456, detail="item_not_found")
    if textmessage.text_type == "message":
        Lib.set_text(textmessage.text_message)
        print(textmessage.text_message)
        edit_database.update_spoken_sentences(textmessage.text_message)
    elif textmessage.text_type == "osc-command":
        address, value = textmessage.text_message.split(",")
        if value == "True":
            value = True
        else:
            value = float(value)
        print(address, value)
        Lib.osc_client.send_message(address, value)


@app.get("/fetch-all-avatar-name")
def fetch_all_avatar_name() -> list:
    lis = []
    inc = 0
    for filenames in CONFIGFILES:
        json_open = open(
            filenames,
            "r",
            encoding="utf_8_sig",
        )
        json_load = json.load(json_open)
        lis.append(json_load["name"])
    return lis


@app.get("/fetch-avatar-config/{name}")
def fetch_avatar_config(name) -> list:
    for filenames in CONFIGFILES:
        json_open = open(
            filenames,
            "r",
            encoding="utf_8_sig",
        )
        json_load = json.load(json_open)
        if json_load["name"] == name:
            return json_load
    raise HTTPException(status_code=422, detail="item_not_found")


@app.get("/fetch-kat-version/")
def fetch_kat_version():
    return float(3.1)


@app.get("/toggle-mic/")
def toggle_mic() -> bool:
    temp = Lib.ismicmute
    while True:
        if Lib.ismicmute == temp:
            Lib.osc_client.send_message("/input/Voice", True)
            Lib.osc_client.send_message("/input/Voice", float(0.0))
        else:
            break
    return Lib.ismicmute

@app.get("/get-spoekn-sentences/")
def get_spoken_sentences() ->list:
    return edit_database.get_spoken_sentences()

@app.post("/update-spoken-sentences/")
def update_spoken_sentences(spoken_sentece: spoken_sentece):
    edit_database.update_spoken_sentences(spoken_sentece.spoken_sentece)


def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


if __name__ == "__main__":
    start_fastapi()
