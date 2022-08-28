from logging import getLogger, config
import json
import os
import datetime
import glob
import sys
from tkinter import Tk, filedialog
from time import sleep
from argparse import ArgumentParser
from typing import Any, Final, Union
import webbrowser

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn


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


def get_conver_file(PRESENT_LOCATION: str, select: bool = True) -> str:
    """
    It opens a file dialog box and returns the path of the file selected by the user

    :param PRESENT_LOCATION: The path to the folder where the file is located
    :return: The file path of the file that the user selected.
    """
    title = "convertlistを選択"
    filetypes = [("CSVファイル", "*.csv")]
    if select:
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            title=title, filetypes=filetypes, initialdir=PRESENT_LOCATION
        )
        root.destroy()  # you need to destroy Tk windows if you want to run this function again
    else:
        file = PRESENT_LOCATION + "//ラノベPOP v2__77lines_converter.csv"
    return file


PRESENT_LOCATION: Final[str] = os.path.dirname(os.path.abspath(sys.argv[0]))
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


class SpokenSentence(BaseModel):
    spoken_sentece: str


class avatar_config(BaseModel):
    avatar_config: str


class ConfigSetting(BaseModel):
    """
    `ConfigSetting` is a class that has four attributes: `text_length`.
    """

    new_convert_file: Union[bool, None]
    text_length: Union[int, None]
    sync_wait: Union[float, None]
    line_length: Union[int, None]


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
def update_api_key(item: Item) -> None:
    edit_database.update_api_table(item.api_name, item.url)


@app.get("/kat_config")
def get_kat_config() -> dict[str, str]:
    """
    Trying to get the text length, line length, and sync wait from the database.
  
    """
    try:
        text_length, line_length, sync_wait = edit_database.get_kat_config()
        return {
            "text_length": text_length,
            "line_length": line_length,
            "sync_wait": sync_wait,
        }
    except TypeError:
        pass


@app.post("/kat_config")
def post_kat_config(config_value: ConfigSetting) -> None:
    """
    Updating the database with the new values.
    """
    text_length, line_length, sync_wait = edit_database.get_kat_config()
    if config_value.new_convert_file:
        NEW_CONVERT_FILE: Final[str] = get_conver_file(PRESENT_LOCATION, True)
        if NEW_CONVERT_FILE == "":
            raise HTTPException(status_code=500, detail="Select a file")
        else:
            Lib.change_convertlist(NEW_CONVERT_FILE)
            # Lib.resend_text()
    if config_value.text_length:
        text_length = config_value.text_length

        Lib.change_text_length(config_value.text_length)
    if config_value.sync_wait:
        sync_wait = config_value.sync_wait
        Lib.change_sync_wait(config_value.sync_wait)
    if config_value.line_length:
        line_length = config_value.line_length
        Lib.change_line_length(config_value.line_length)

    edit_database.update_kat_config(text_length, line_length, sync_wait)


@app.post("/text-message/")
def post_text_message(textmessage: TextMessage) -> None:
    """
    It takes a TextMessage object, and depending on the text_type attribute, it either sets the text of
    the textbox, updates the database, or sends an OSC message
    class TextMessage(BaseModel):
        text_type: str
        text_message: str
    text_type:
        message:Sentence for KAT
        osc-command: OSC command
        offical-text-chat:Sentence for offical text chat
    """
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
        # print(address, value)
        Lib.osc_client.send_message(address, value)
    elif textmessage.text_type == "offical-text-chat":
        Lib.osc_client.send_message("/chatbox/input", (textmessage.text_message, True))
    else:
        raise HTTPException(status_code=422, detail="item_not_found")
    # elif textmessage.text_type == "toggle-offical-text-chat":
    #     Lib.osc_client.send_message("/chatbox/typing", True)


@app.get("/fetch-all-avatar-name")
def fetch_all_avatar_name() -> list:
    """
    It opens all the files in the CONFIGFILES list, and then appends the name of the avatar to a list
    :return: A list of all the names of the avatars.
    """
    lis = []
    for filenames in CONFIGFILES:
        json_open = open(
            filenames,
            "r",
            encoding="utf_8_sig",
        )
        json_load = json.load(json_open)
        name = json_load["name"]
        blueprint = json_load["id"]
        time = os.path.getmtime(filenames)
        date = datetime.datetime.fromtimestamp(time)
        edit_database.update_avatar_config(blueprint, date, json_load)
        lis.append((blueprint, name))
    return lis


@app.get("/fetch-avatar-config/{blueprint}")
def fetch_avatar_config(blueprint: str) -> list:
    """
    It opens a json file, loads it, and if the name in the json file matches the name passed to the
    function, it returns the json file

    :param name: The name of the avatar you want to fetch
    :return: A list of dictionaries.
    """
    json_config = edit_database.get_avatar_config(blueprint)
    json_data = json_config[0]
    json_load = json.loads(json_data)
    if json is None:
        raise HTTPException(status_code=422, detail="item_not_found")
    else:
        return json_load


@app.put("/save-avatar-config/")
def save_avatar_config(avatar_config: avatar_config) -> None:
    # print(avatar_config)
    json_config = json.loads(str(avatar_config.avatar_config))
    # print(json_config)
    edit_database.save_avatar_config(json_config)


@app.get("/fetch-kat-version/")
def fetch_kat_version():
    """
    This function check the connection to a web server and returns the version of the local server
    :return: The version of the KAT software.
    """
    logger.info("Connected to Web server")
    return float(0.4)


@app.get("/toggle-mic/")
def toggle_mic() -> bool:
    """
    It sends a message to the server to toggle the mic on or off.
    Try five times and raise erro in case of failure
    :return: a boolean value.
    """
    temp = Lib.ismicmute
    inc = 0
    while inc < 3:
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
    """
    > This function returns a list of sentences that have been spoken by the user
    :return: A list of spoken sentences.
    """
    return edit_database.get_spoken_sentences()


@app.post("/update-spoken-sentences/")
def update_spoken_sentences(spoken_sentece: SpokenSentence):
    """
    Update the spoken sentences in the database
    """
    edit_database.update_spoken_sentences(spoken_sentece.SpokenSentence)


@app.get("/")
def index() -> None:
    """
    Redirect to documents
    """
    return RedirectResponse(url="/docs/")


def start_fastapi(host: str = "127.0.0.1", port: int = 8080):
    """
    Start local server
    """
    uvicorn.run(app, host=host, port=port, log_level="info")


def get_option():
    """
    Read argument
    """
    parser = ArgumentParser()
    parser.add_argument("--no_web", action="store_true", help="not open chrome")
    parser.add_argument(
        "--no_select",
        action="store_false",
        help="read the default convertfile\
        ラノベPOP v2__77lines_converter.csv",
    )
    parser.add_argument(
        "--host_ip", help="ip of local server default: 127.0.0.1", default="127.0.0.1"
    )
    parser.add_argument(
        "--port", help="port of local server default:8080", default=8080, type=int
    )
    parser.add_argument("--debug", action="store_true", help="debug")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_option()
    CONFIGFILES: Final[list] = glob.glob(
        os.path.expanduser("~")
        + "\\AppData\\LocalLow\\VRChat\\VRChat\\OSC\\\**\\*.json",
        recursive=True,
    )
    edit_database = edit_database.Edit_database(logger_object=logger)
    dic = get_kat_config()
    if not dic:
        # default value
        default_text_length = 128
        default_line_length = 16
        default_sync_wait = 0.1
        edit_database.update_kat_config(
            default_text_length, default_line_length, default_sync_wait
        )

    if args.debug:
        logger.info("Start Debugmode")
        CONVERT_FILE = get_conver_file(PRESENT_LOCATION, False)
        Lib_config = lib.KatOscConfig(
            file=CONVERT_FILE,
            logger_object=logger,
            osc_port=9002,
            osc_server_port=9003,
            text_length=dic["text_length"] if dic else default_text_length,
            line_length=dic["line_length"] if dic else default_line_length,
            sync_wait=dic["sync_wait"] if dic else default_sync_wait,
        )

    else:
        logger.info("Start FAST_api")
        if not args.no_web:
            URL: Final[str] = "kuretan-lab.com"
            try:
                browser = webbrowser.get(
                    '"C:\Program Files\Google\Chrome\Application\chrome.exe" %s '
                )
                browser.open_new(URL)
            except:
                logger.warning("Fail to run Chrome.")
                webbrowser.open(URL)
        CONVERT_FILE = get_conver_file(PRESENT_LOCATION, args.no_select)
        # CONVERT_FILE = get_conver_file(PRESENT_LOCATION, False)
        Lib_config = lib.KatOscConfig(
            file=CONVERT_FILE,
            logger_object=logger,
            text_length=dic["text_length"] if dic else default_text_length,
            line_length=dic["line_length"] if dic else default_line_length,
            sync_wait=dic["sync_wait"] if dic else default_sync_wait,
        )
    Lib = lib.KatOsc(config=Lib_config)
    start_fastapi(host=args.host_ip, port=args.port)
