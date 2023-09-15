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


def delete_response(page, id):
    url = f"{base_url}/{page}/{id}"
    res = requests.delete(url)
    if res.status_code == 200:
        st.session_state.delete_success = "削除完了しました。"
        st.experimental_rerun()
    else:
        st.error("削除に失敗しました。")
