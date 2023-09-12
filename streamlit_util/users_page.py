import streamlit as st

from streamlit_util.get_response import convert_users_to_df, get_user, get_users
from streamlit_util.post_response import delete_response, show_response, update_response
from streamlit_util.session import session_check


def show_user_page(page_title):
    st.title("ユーザー登録")
    users = get_users()
    df_users = convert_users_to_df(users)
    if users:
        st.write("#### ユーザー一覧")
        st.table(df_users)

        create, update, delete = st.tabs(["登録", "変更", "削除"])
        with create:
            create_user(page_title)
        with update:
            update_user(df_users, page_title)
        with delete:
            delete_user(df_users, page_title)

    else:
        st.info("ユーザーを登録してください。", icon="ℹ️")
        create_user(page_title)

    session_check()


def create_user(page_title):
    with st.form(key=f"{page_title}_create"):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_name": user_name}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        if user_name:
            show_response(page_title, data)
        else:
            st.error("ユーザー名を入力してください。", icon="🔥")


def update_user(df_users, page_title):
    with st.form(key=f"{page_title}_update"):
        user_id = st.selectbox("ユーザーID", df_users["ユーザーID"], key="update")
        user_name: str = st.text_input(
            "ユーザー名", value=get_user(user_id)["user_name"], max_chars=12
        )
        update_button = st.form_submit_button("変更")

    if update_button:
        payload = {
            "user_id": user_id,
            "user_name": user_name,
        }
        update_response(page_title, user_id, payload)


def delete_user(df_users, page_title):
    with st.form(key=f"{page_title}_delete"):
        user_id = st.selectbox("ユーザーID", df_users["ユーザーID"], key="delete")
        delete_button = st.form_submit_button("削除")

    if delete_button:
        delete_response(page_title, user_id)
