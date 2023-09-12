import streamlit as st

from streamlit_util.get_response import convert_users_to_df, get_user, get_users
from streamlit_util.post_response import show_response
from streamlit_util.session import session_check


def show_user_page(page_title):
    st.title("ユーザー登録")
    users = get_users()
    df_users = convert_users_to_df(users)
    if users:
        st.write("#### ユーザー一覧")
        st.table(df_users)

        st.sidebar.title("ユーザー更新")
        user_id = st.sidebar.selectbox("ユーザーID", df_users["ユーザーID"], key="delete")
        user_name: str = st.sidebar.text_input(
            "ユーザー名", value=get_user(user_id)["user_name"], max_chars=12
        )

    else:
        st.info("ユーザーを登録してください。", icon="ℹ️")

    with st.form(key=page_title):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_name": user_name}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        if user_name:
            show_response(page_title, data)
        else:
            st.error("ユーザー名を入力してください。", icon="🔥")

    session_check()
