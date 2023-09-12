import streamlit as st

from streamlit_util.get_response import convert_rooms_to_df, get_room, get_rooms
from streamlit_util.post_response import show_response, update_response
from streamlit_util.session import session_check


def show_room_page(page_title):
    st.title("会議室登録")
    rooms = get_rooms()
    if rooms:
        st.write("#### 会議室一覧")
        df_rooms = convert_rooms_to_df(rooms)
        st.table(df_rooms)

        create, update, delete = st.tabs(["登録", "変更", "削除"])
        with create:
            create_room(page_title)
        with update:
            update_room(df_rooms, page_title)
        with delete:
            pass
    else:
        st.info("会議室を登録してください。", icon="ℹ️")

    session_check()


def create_room(page_title):
    with st.form(key=f"{page_title}_create"):
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", 1, step=1)
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        if room_name:
            show_response(page_title, data)
        else:
            st.error("会議室名を入力してください。")


def update_room(df_rooms, page_title):
    with st.form(key=f"{page_title}_update"):
        room_id = st.selectbox("会議室ID", df_rooms["会議室ID"], key="update")
        room_name: str = st.text_input("会議室名", value=get_room(room_id)["room_name"])
        capacity: int = st.number_input(
            "定員", value=get_room(room_id)["capacity"], min_value=1
        )
        update_button = st.form_submit_button("変更")

    if update_button:
        payload = {
            "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity,
        }
        update_response(page_title, room_id, payload)
