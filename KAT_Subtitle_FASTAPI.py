from logging import getLogger, config
import json
import os
import sys
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


@app.get("/api_key/{api_type}")
def post_api_key(api_type: str):
    api_key = edit_database.get_api_table(api_type)
    # raise HTTPException(status_code=456, detail="item_not_found")
    return {api_type: api_key}


@app.post("/api_key/")
async def update_api_key(item: Item):
    edit_database.update_api_table(item.api_name, item.url)


@app.post("/text-message/")
def post_text_message(textmessage: TextMessage):
    # raise HTTPException(status_code=456, detail="item_not_found")
    if textmessage.text_type == "message":
        Lib.set_text(textmessage.text_message)
    elif textmessage.text_type == "osc-command":
        address, value = textmessage.text_message.split(",")
        if value == "True":
            value = True
        else:
            value = float(value)
        Lib.osc_client.send_message(address, value)


def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


if __name__ == "__main__":
    start_fastapi()
