# 実行手順

## Streamlit 画面起動

1. root のディレクトリに移動。
1. 以下のコマンドを実行する。

   ```bash
   streamlit run app.py
   ```

1. http://localhost:8501/ で起動確認。

## FastAPI サーバー起動

1. root のディレクトリに移動。
1. 以下のコマンドを実行する。

   ```bash
   uvicorn sql_app.main:app --reload
   ```

1. http://127.0.0.1:8000 で起動確認。
