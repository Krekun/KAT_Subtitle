import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union

import KAT_Subtitle_editdatabase
import KAT_Subtitle_Lib
import KAT_Subtitle_Gui

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

Gui = KAT_Subtitle_Gui.KATSubtitleGui(_use_chrome=True)


class Item(BaseModel):
    api_name: str
    url: str


class TextMessage(BaseModel):
    text_type: str
    text_message: str


@app.get("/api_key/{api_type}")
def post_api_key(api_type: str):
    api_key = edit_database.get_api_table(api_type)
    return {api_type: api_key}


@app.post("/api_key/")
async def update_api_key(item: Item):
    edit_database.update_api_table(item.api_name, item.url)


@app.post("/text-message/")
def post_text_message(textmessage: TextMessage):
    if textmessage.text_type == "message":
        print(textmessage)
    else:
        print(textmessage, 2)


def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


if __name__ == "__main__":
    start_fastapi()
