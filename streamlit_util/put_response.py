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


def update_response(page, id, payload):
    res = requests.put(
        f"{base_url}/{page}/{id}",
        json=payload,
    )
    st.write(res.json())
    if res.status_code == 200:
        st.session_state.update_success = "更新完了しました。"
        st.experimental_rerun()
    else:
        st.error("更新に失敗しました。")
