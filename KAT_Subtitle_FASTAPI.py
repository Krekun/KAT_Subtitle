from pickle import GET
from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# origins = ["http://localhost:8000/"]

# To avoid a CORS problem
# https://qiita.com/satto_sann/items/0e1f5dbbe62efc612a78
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # 追記により追加
    allow_methods=["*"],  # 追記により追加
    allow_headers=["*"],  # 追記により追加
)

# 必要なコマンド
# テキストを送信
#

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api_keys")
def post_apikey():
    return {"GAS": "https://script.google.com/macros/s/AKfycbxPHHgYIEn8sJSeH6B-9RtsWqKk2U43GRANO4kkfJiMSlRgnCTcK-sPjKxACfDRp5Qb/exec"}

@app.get("/osc_setting")
def post_oscsetting():
    return None

def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


if __name__ == "__main__":
    start_fastapi()
