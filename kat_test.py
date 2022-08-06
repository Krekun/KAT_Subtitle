from fastapi.testclient import TestClient
from KAT_Subtitle_FASTAPI import app
import os
import sys
from tkinter import messagebox

client = TestClient(app)


def test_get_products_all():
    response = client.get("/api_key/deepL")
    assert response.status_code == 200


def test_send_message():
    file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(file_path)
    respose = client.post(
        "/text-message/",
        json={"text_type": "message", "text_message": "Fucking"},
    )
    assert 200
