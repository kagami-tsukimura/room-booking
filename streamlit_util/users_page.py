import streamlit as st

from streamlit_util.get_response import convert_users_to_df, get_users
from streamlit_util.post_response import show_response
from streamlit_util.session import session_check


def show_user_page(page_title):
    st.title("ユーザー登録")
    st.write("#### ユーザー一覧")
    users = get_users()
    df_users = convert_users_to_df(users)
    st.table(df_users)

    with st.form(key=page_title):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_name": user_name}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        show_response(page_title, data)

    session_check()
