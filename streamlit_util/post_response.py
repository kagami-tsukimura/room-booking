import json
import os

import requests
import streamlit as st

# 環境変数 DEPLOYMENT_ENV からデプロイ環境を取得
deployment_env = os.environ.get("DEPLOYMENT_ENV")

# デプロイ環境に応じてベースURLを返す
if deployment_env == "production":
    base_url = "https://room-booking-api-v4f1.onrender.com"
else:
    base_url = "http://127.0.0.1:8000"


def show_response(page, data):
    url = f"{base_url}/{page}"
    res = requests.post(url, data=json.dumps(data))

    if res.status_code == 200:
        st.session_state.create_success = "登録完了しました。"
        st.experimental_rerun()
    elif res.status_code == 404 and res.json()["detail"] == "Already booked":
        st.error("指定の時間は既に予約が入っています。")
    else:
        st.error(f"Error: {res.status_code}")
