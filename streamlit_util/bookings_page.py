import datetime

import pandas as pd
import streamlit as st

from streamlit_util.delete_response import delete_response
from streamlit_util.get_response import (
    convert_rooms_to_df,
    get_bookings,
    get_rooms,
    get_users,
)
from streamlit_util.post_response import show_response
from streamlit_util.put_response import update_response
from streamlit_util.session import session_check


def show_bookings_page(page_title):
    st.title("会議室予約")
    users = get_users()
    users_name = {}
    for user in users:
        users_name[user["user_name"]] = user["user_id"]
    rooms = get_rooms()
    df_rooms = convert_rooms_to_df(rooms)
    bookings = get_bookings()
    df_bookings = pd.DataFrame(bookings)
    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["user_name"]
    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"],
        }

    if not users_id or not rooms_id:
        st.error("ユーザーと会議室を登録してください。")
    elif bookings:
        df_bookings = format_df_bookings(users_id, rooms_id, df_bookings)
        st.write("#### 予約一覧")
        st.table(df_bookings)
        st.write("#### 会議室一覧")
        st.table(df_rooms)

        create, update, delete = st.tabs(["登録", "変更", "削除"])
        with create:
            create_booking(page_title, users_name, rooms)
        with update:
            update_booking(page_title, rooms, df_bookings, users_name)
        with delete:
            delete_booking(page_title, df_bookings)
    else:
        st.write("#### 会議室一覧")
        st.table(df_rooms)
        create_booking(page_title, users_name, rooms)

    session_check()


def format_df_bookings(users_id, rooms_id, df_bookings):
    to_user_name = lambda x: users_id[x]  # NOQA
    to_room_name = lambda x: rooms_id[x]["room_name"]  # NOQA
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime(  # NOQA
        "%Y/%m/%d %H:%M"
    )
    df_bookings["user_id"] = df_bookings["user_id"].map(to_user_name)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)
    df_bookings = df_bookings.rename(
        columns={
            "user_id": "予約者名",
            "room_id": "会議室名",
            "booked_num": "予約人数",
            "start_datetime": "開始時刻",
            "end_datetime": "終了時刻",
            "booking_id": "予約番号",
        }
    )

    return df_bookings


def create_booking(page_title, users_name, rooms):
    with st.form(key=f"{page_title}_create"):
        user_name: str = st.selectbox("予約者名", users_name.keys())
        rooms_name = {}
        for room in rooms:
            rooms_name[room["room_name"]] = {
                "room_id": room["room_id"],
                "capacity": room["capacity"],
            }
        room_name: str = st.selectbox("会議室名", rooms_name.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻: ", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻: ", value=datetime.time(hour=10, minute=0))

        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        user_id: int = users_name[user_name]
        room_id: int = rooms_name[room_name]["room_id"]
        capacity: int = rooms_name[room_name]["capacity"]

        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat(),
        }

        validation_error = validation_check(
            booked_num, capacity, room_name, start_time, end_time
        )

        if validation_error:
            st.error(validation_error)
        else:
            # 会議室の予約
            show_response(
                page_title,
                data,
            )


def update_booking(page_title, rooms, df_bookings, users_name):
    with st.form(key=f"{page_title}_update"):
        rooms_name = {}
        for room in rooms:
            rooms_name[room["room_name"]] = {
                "room_id": room["room_id"],
                "capacity": room["capacity"],
            }
        booking_id: int = st.selectbox("予約番号", df_bookings["予約番号"], key="update_number")
        user_name: str = st.selectbox("予約者名", users_name.keys())
        room_name: str = st.selectbox("会議室名", rooms_name.keys())
        booked_num: int = st.number_input(
            "予約人数",
            value=df_bookings.loc[df_bookings["予約番号"] == booking_id, "予約人数"].values[0],
            step=1,
            min_value=1,
        )
        date = st.date_input("日付", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻", value=datetime.time(hour=10, minute=0))

        update_button = st.form_submit_button("変更")
        if update_button:
            user_id: int = users_name[user_name]
            room_id: int = rooms_name[room_name]["room_id"]
            capacity: int = rooms_name[room_name]["capacity"]

            payload = {
                "user_id": user_id,
                "room_id": room_id,
                "booked_num": booked_num,
                "start_datetime": datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=start_time.hour,
                    minute=start_time.minute,
                ).isoformat(),
                "end_datetime": datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=end_time.hour,
                    minute=end_time.minute,
                ).isoformat(),
            }

            validation_error = validation_check(
                booked_num, capacity, room_name, start_time, end_time
            )
            if validation_error:
                st.error(validation_error)
            else:
                update_response(page_title, booking_id, payload)


def delete_booking(page_title, df_bookings):
    with st.form(key=f"{page_title}_delete"):
        booking_id: int = st.selectbox("予約番号", df_bookings["予約番号"], key="delete")
        delete_button = st.form_submit_button("削除")

    if delete_button:
        delete_response(page_title, booking_id)


def validation_check(booked_num, capacity, room_name, start_time, end_time):
    # 予約人数が定員を超過
    if booked_num > capacity:
        return f"{room_name}の定員を超えています。予約人数を{capacity}名以下に変更してください。"
    # 開始時刻 >= 終了時刻
    elif start_time >= end_time:
        return "開始時刻は終了時刻より前に設定してください。"
    # 開始時刻が9時より前
    elif start_time < datetime.time(
        hour=9, minute=0, second=0
    ) or end_time > datetime.time(hour=20, minute=0, second=0):
        return "利用時刻は9:00~20:00に設定してください。"
