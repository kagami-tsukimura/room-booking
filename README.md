# 会議室予約アプリ

## 概要

- フロントエンド
  - Streamlit
- バックエンド
  - FastAPI
- DB
  - SQLite3

## Web Page

🐧 下記の URL からサイトに遷移します。🐧

[room-booking](https://room-booking.streamlit.app/)

- フロントエンド

  - [Streamlit Sharing](https://room-booking.streamlit.app/)

- バックエンド
  - [Deta](https://booking-1-x3709405.deta.app/)

## ローカル実行手順

### FastAPI サーバー起動

1. root のディレクトリに移動。
2. 以下のコマンドを実行する。

   ```bash
   cd sql_app/ && uvicorn main:app --reload
   ```

3. http://127.0.0.1:8000 で起動確認。

### Streamlit 画面起動

1. root のディレクトリに移動。
2. 以下のコマンドを実行する。

   ```bash
   streamlit run app.py
   ```

3. http://localhost:8501/ で起動確認。
