import json
import os

import requests
import streamlit as st

# 環境変数 DEPLOYMENT_ENV からデプロイ環境を取得
deployment_env = os.environ.get("DEPLOYMENT_ENV")

# デプロイ環境に応じてベースURLを返す
if deployment_env == "production":
    base_url = "https://booking-1-x3709405.deta.app"
else:
    base_url = "http://127.0.0.1:8000"
