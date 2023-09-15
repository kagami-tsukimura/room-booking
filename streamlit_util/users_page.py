import streamlit as st

from streamlit_util.delete_response import delete_response
from streamlit_util.get_response import (
    convert_users_to_df,
    get_bookings_filtered_user,
    get_user,
    get_users,
)
from streamlit_util.post_response import show_response
from streamlit_util.put_response import update_response
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
            create_user(df_users, page_title)
        with update:
            update_user(df_users, page_title)
        with delete:
            delete_user(df_users, page_title)

    else:
        st.info("ユーザーを登録してください。", icon="ℹ️")
        create_user(df_users, page_title)

    session_check()


def create_user(df_users, page_title):
    with st.form(key=f"{page_title}_create"):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_name": user_name}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        validation_error = validate_check(user_name, df_users)
        if validation_error:
            st.error(validation_error, icon="🔥")
        else:
            show_response(page_title, data)


def validate_check(user_name, df_users):
    if not user_name:
        return "ユーザー名を入力してください。"
    if not df_users.empty and user_name in df_users["ユーザー名"].values:
        return f"{user_name}さんは登録済みです。別のユーザー名に変更してください。"


def update_user(df_users, page_title):
    with st.form(key=f"{page_title}_update"):
        user_id = st.selectbox("ユーザーID", df_users["ユーザーID"], key="update")
        user_name: str = st.text_input(
            "ユーザー名", value=get_user(user_id)["user_name"], max_chars=12
        )
        update_button = st.form_submit_button("変更")

    if update_button:
        validation_error = validate_check(user_name, df_users)
        if validation_error:
            st.error(validation_error, icon="🔥")
        else:
            payload = {
                "user_id": user_id,
                "user_name": user_name,
            }
            update_response(page_title, user_id, payload)


def delete_user(df_users, page_title):
    with st.form(key=f"{page_title}_delete"):
        user_name = st.selectbox("ユーザー名", df_users["ユーザー名"], key="delete")
        delete_button = st.form_submit_button("削除")

    if delete_button:
        user_id = df_users[df_users["ユーザー名"] == user_name]["ユーザーID"].values[0]
        used_user = validate_used_user(user_id)
        if used_user:
            st.error(
                f"{used_user}さんの予約がされています。先に{used_user}さんの予約を変更してください。",
                icon="🔥",
            )
        else:
            delete_response(page_title, user_id)


def validate_used_user(user_id):
    used_user_booking = get_bookings_filtered_user(user_id)
    if len(used_user_booking) == 0:
        return False
    used_user_id = [booking.get("user_id") for booking in used_user_booking]
    used_user = get_user(used_user_id[0])
    used_user_name = used_user["user_name"]
    return used_user_name
