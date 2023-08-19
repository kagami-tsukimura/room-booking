import json

import requests
import streamlit as st


def show_response(page, data):
    url = f"http://127.0.0.1:8000/{page}"
    res = requests.post(url, data=json.dumps(data))

    if res.status_code == 200:
        st.session_state.create_success = "登録完了しました。"
        st.experimental_rerun()
    elif res.status_code == 404 and res.json()["detail"] == "Already booked":
        st.error("指定の時間は既に予約が入っています。")
    else:
        st.error(f"Error: {res.status_code}")


def update_response(page, id, payload):
    res = requests.put(
        f"http://127.0.0.1:8000/{page}/{id}",
        json=payload,
    )
    st.write(res.json())
    if res.status_code == 200:
        st.session_state.update_success = "更新完了しました。"
        st.experimental_rerun()
    else:
        st.sidebar.error("更新に失敗しました。")


def delete_response(page, id):
    url = f"http://127.0.0.1:8000/{page}/{id}"
    res = requests.delete(url)
    if res.status_code == 200:
        st.session_state.delete_success = "削除完了しました。"
        st.experimental_rerun()
    else:
        st.sidebar.error("削除に失敗しました。")
