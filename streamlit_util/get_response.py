import os

import pandas as pd
import requests

# 環境変数 DEPLOYMENT_ENV からデプロイ環境を取得
deployment_env = os.environ.get("DEPLOYMENT_ENV")

# デプロイ環境に応じてベースURLを返す
if deployment_env == "production":
    base_url = "https://booking-1-x3709405.deta.app"
else:
    base_url = "http://127.0.0.1:8000"


def get_user(user_id):
    url_user = f"{base_url}/users/{user_id}"
    res = requests.get(url_user)
    user = res.json()
    return user


def get_users():
    url_users = f"{base_url}/users"
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


def get_room(room_id):
    url_room = f"{base_url}/rooms/{room_id}"
    res = requests.get(url_room)
    room = res.json()
    return room


def get_rooms():
    url_rooms = f"{base_url}/rooms"
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
    url_bookings = f"{base_url}/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()
    return bookings
