# 会議室予約アプリ

## 概要

- フロントエンド
  - Streamlit
- バックエンド
  - FastAPI
- DB
  - SQLite3

## 実行手順

### FastAPI サーバー起動

1. root のディレクトリに移動。
2. 以下のコマンドを実行する。

   ```bash
   uvicorn sql_app.main:app --reload
   ```

3. http://127.0.0.1:8000 で起動確認。

### Streamlit 画面起動

1. root のディレクトリに移動。
2. 以下のコマンドを実行する。

   ```bash
   streamlit run app.py
   ```

3. http://localhost:8501/ で起動確認。
