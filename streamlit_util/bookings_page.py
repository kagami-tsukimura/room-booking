import datetime

import pandas as pd
import streamlit as st

import streamlit_util.get_response as get_response
import streamlit_util.post_response as post_response


def show_bookings_page(page_title):
    st.title("会議室予約")
    users = get_response.get_users()
    users_name = {}
    for user in users:
        users_name[user["user_name"]] = user["user_id"]

    rooms = get_response.get_rooms()
    df_rooms = get_response.convert_rooms_to_df(rooms)

    bookings = get_response.get_bookings()
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

    # ユーザーと会議室が登録されている場合
    if not users_id or not rooms_id:
        st.error("ユーザーと会議室を登録してください。")
    # 会議室が予約されている場合
    elif bookings:
        # 一覧にはidではなく名称を表示
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
        st.write("### 予約一覧")
        st.table(df_bookings)

        # 予約更新
        with st.sidebar.form(key=f"{page_title}_update"):
            st.sidebar.title("予約更新")
            rooms_name = {}
            for room in rooms:
                rooms_name[room["room_name"]] = {
                    "room_id": room["room_id"],
                    "capacity": room["capacity"],
                }
            booking_id: int = st.sidebar.selectbox(
                "予約番号", df_bookings["予約番号"], key="update_number"
            )
            user_name: str = st.sidebar.selectbox("予約者名", users_name.keys())
            room_name: str = st.sidebar.selectbox("会議室名", rooms_name.keys())
            booked_num: int = st.sidebar.number_input(
                "予約人数",
                value=df_bookings.loc[df_bookings["予約番号"] == booking_id, "予約人数"].values[
                    0
                ],
                step=1,
                min_value=1,
            )
            date = st.sidebar.date_input("日付", min_value=datetime.date.today())
            start_time = st.sidebar.time_input(
                "開始時刻", value=datetime.time(hour=9, minute=0)
            )
            end_time = st.sidebar.time_input(
                "終了時刻", value=datetime.time(hour=10, minute=0)
            )

            update_button = st.sidebar.button("予約を更新する")
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
                    st.sidebar.error(validation_error)
                else:
                    post_response.update_response(page_title, booking_id, payload)

        # 予約削除
        with st.sidebar.form(key=f"{page_title}_delete"):
            st.sidebar.title("予約削除")
            booking_id: int = st.sidebar.selectbox(
                "予約番号", df_bookings["予約番号"], key="delete"
            )
            delete_button = st.sidebar.button("予約を削除する")

        if delete_button:
            post_response.delete_response(page_title, booking_id)

    st.write("#### 会議室一覧")
    st.table(df_rooms)

    with st.form(key=f"{page_title}_create"):
        user_name: str = st.selectbox("予約者名", users_name.keys())
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
            post_response.show_response(
                page_title,
                data,
            )

    session_check()


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


def session_check():
    if hasattr(st.session_state, "create_success"):
        st.success(st.session_state.create_success)
        del st.session_state.create_success
    if hasattr(st.session_state, "update_success"):
        st.sidebar.success(st.session_state.update_success)
        del st.session_state.update_success
    if hasattr(st.session_state, "delete_success"):
        st.sidebar.success(st.session_state.delete_success)
        del st.session_state.delete_success
