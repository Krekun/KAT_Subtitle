from logging import getLogger, config
import json
import os
import glob
import sys
import json
from tkinter import Tk, filedialog
from time import sleep
from argparse import ArgumentParser

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import webbrowser

import edit_database
import lib

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


def get_conver_file(present_location: str) -> str:
    """
    It opens a file dialog box and returns the path of the file selected by the user

    :param PRESENT_LOCATION: The path to the folder where the file is located
    :return: The file path of the file that the user selected.
    """
    title = "convertlistを選択"
    filetypes = [("CSVファイル", "*.csv")]
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
        title=title, filetypes=filetypes, initialdir=PRESENT_LOCATION
    )
    # file = r"C:\Users\baryo\Documents\Vrchat\KAT\KAT_Subtitle\ラノベPOP v2__77lines_converter.csv"
    return file


PRESENT_LOCATION = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(PRESENT_LOCATION)
with open("log_config.json", "r", encoding="UTF") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


class Item(BaseModel):
    api_name: str
    url: str


class TextMessage(BaseModel):
    text_type: str
    text_message: str


class spoken_sentece(BaseModel):
    spoken_sentece: str


@app.get("/api_key/")
def get_api_key() -> dict[str, str]:
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


@app.put("/api_key/")
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
    logger.info("Connected to Web server")
    return float(0.3)


@app.get("/toggle-mic/")
def toggle_mic() -> bool:
    """
    It sends a message to the server to toggle the mic on or off.
    Try five times and raise erro in case of failure
    :return: a boolean value.
    """
    temp = Lib.ismicmute
    inc = 0
    while inc < 10:
        if Lib.ismicmute == temp:
            Lib.osc_client.send_message("/input/Voice", True)
            sleep(0.5)
            Lib.osc_client.send_message("/input/Voice", float(0.0))
        else:
            return Lib.ismicmute
        inc += 1
    raise HTTPException(status_code=500, detail="fail to mute mic")


@app.get("/get-spoekn-sentences/")
def get_spoken_sentences() -> list:
    return edit_database.get_spoken_sentences()


@app.post("/update-spoken-sentences/")
def update_spoken_sentences(spoken_sentece: spoken_sentece):
    edit_database.update_spoken_sentences(spoken_sentece.spoken_sentece)


def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


def get_option():
    parser = ArgumentParser()
    parser.add_argument("--no_web", action="store_true", help="not open chrome")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_option()
    if not args.no_web:
        URL = "kuretan-lab.com"
        try:
            browser = webbrowser.get(
                '"C:\Program Files\Google\Chrome\Application\chrome.exe" %s '
            )
            browser.open_new(URL)
        except:
            logger.warning("Fail to run Chrome.")
            webbrowser.open(URL)
    logger.info("Start FAST_api")
    CONFIGFILES = glob.glob(
        os.path.expanduser("~")
        + "\\AppData\\LocalLow\\VRChat\\VRChat\\OSC\\\**\\*.json",
        recursive=True,
    )
    CONVERT_FILE = get_conver_file(PRESENT_LOCATION)
    Lib = lib.KatOsc(file=CONVERT_FILE, logger=logger)
    edit_database = edit_database.Edit_database()
    start_fastapi()
