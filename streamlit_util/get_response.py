import pandas as pd
import requests


def get_users():
    url_users = "http://127.0.0.1:8000/users"
    res = requests.get(url_users)
    users = res.json()
    return users


def convert_users_to_df(users):
    df_users = pd.DataFrame(users)
    df_users = df_users.rename(
        columns={
            "user_name": "ユーザー名",
            "user_id": "ユーザーID",
        }
    )
    return df_users


def get_rooms():
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()
    return rooms


def convert_rooms_to_df(rooms):
    df_rooms = pd.DataFrame(rooms)
    df_rooms = df_rooms.rename(
        columns={
            "room_name": "会議室名",
            "capacity": "定員",
            "room_id": "会議室ID",
        }
    )
    return df_rooms


def get_bookings():
    url_bookings = "http://127.0.0.1:8000/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()
    return bookings
