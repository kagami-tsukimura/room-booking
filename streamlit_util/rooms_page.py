import streamlit as st

from streamlit_util.delete_response import delete_response
from streamlit_util.get_response import (
    convert_rooms_to_df,
    get_bookings_filtered_room,
    get_room,
    get_rooms,
)
from streamlit_util.post_response import show_response
from streamlit_util.put_response import update_response
from streamlit_util.session import session_check


def show_room_page(page_title):
    st.title("会議室登録")
    rooms = get_rooms()
    df_rooms = convert_rooms_to_df(rooms)
    if rooms:
        st.write("#### 会議室一覧")
        st.table(df_rooms)

        create, update, delete = st.tabs(["登録", "変更", "削除"])
        with create:
            create_room(df_rooms, page_title)
        with update:
            update_room(df_rooms, page_title)
        with delete:
            delete_room(df_rooms, page_title)
    else:
        st.info("会議室を登録してください。", icon="ℹ️")
        create_room(df_rooms, page_title)

    session_check()


def create_room(df_rooms, page_title):
    with st.form(key=f"{page_title}_create"):
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", 1, step=1)
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        validation_error = validate_same_room(df_rooms, room_name)
        if validation_error:
            st.error(validation_error, icon="🔥")
        else:
            show_response(page_title, data)


def validate_same_room(df_rooms, room_name):
    if not room_name:
        return "会議室名を入力してください。"
    if not df_rooms.empty and room_name in df_rooms["会議室名"].values:
        return f"{room_name}は登録済みです。別の会議室名に変更してください。"


def update_room(df_rooms, page_title):
    with st.form(key=f"{page_title}_update"):
        room_id = st.selectbox("会議室ID", df_rooms["会議室ID"], key="update")
        room_name: str = st.text_input("会議室名", value=get_room(room_id)["room_name"])
        capacity: int = st.number_input(
            "定員", value=get_room(room_id)["capacity"], min_value=1
        )
        update_button = st.form_submit_button("変更")

    if update_button:
        validation_error = validate_same_room(df_rooms, room_name)
        error_message = validate_update_room(
            validation_error, room_id, capacity, room_name
        )
        if error_message:
            st.error(error_message, icon="🔥")
        else:
            payload = {
                "room_id": room_id,
                "room_name": room_name,
                "capacity": capacity,
            }
            update_response(page_title, room_id, payload)


def validate_update_room(validation_error, room_id, capacity, room_name):
    if validation_error:
        return validation_error
    bookings = get_bookings_filtered_room(room_id)
    booked_num = [booking.get("booked_num") for booking in bookings]
    sort_booked_num = sorted(booked_num, reverse=True)
    capacity_over_booked_num = next(
        (num for num in sort_booked_num if num > capacity), None
    )
    validation_capacity = f"{room_name}は既に{capacity_over_booked_num}名の予約がされています。定員を{capacity_over_booked_num}名以上にしてください。"
    return validation_capacity


def delete_room(df_rooms, page_title):
    with st.form(key=f"{page_title}_delete"):
        room_name = st.selectbox("会議室名", df_rooms["会議室名"], key="delete")
        delete_button = st.form_submit_button("削除")

    if delete_button:
        room_id = df_rooms[df_rooms["会議室名"] == room_name]["会議室ID"].values[0]
        used_room = validate_used_room(room_id)
        if used_room:
            st.error(
                f"{used_room}は予約がされています。先に{used_room}の予約を変更してください。",
                icon="🔥",
            )
        else:
            delete_response(page_title, room_id)


def validate_used_room(room_id):
    used_room_booking = get_bookings_filtered_room(room_id)
    if len(used_room_booking) == 0:
        return False
    used_room_id = [booking.get("room_id") for booking in used_room_booking]
    used_room = get_room(used_room_id[0])
    used_room_name = used_room["room_name"]
    return used_room_name
