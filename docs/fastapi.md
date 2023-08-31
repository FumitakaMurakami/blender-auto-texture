# Fast API

ユーザーからのアクセスのための API を FAST API フレームワークにより実現する。

詳しくは、[チュートリアルドキュメント](https://fastapi.tiangolo.com/ja/tutorial/)を参照のこと

## インストール（ローカル）

`pip install fastapi uvicorn`

## サンプルコード

main.py

```python:main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def hello():
    return {"message" : "Hello,World"}
```

## 起動

(本システムでは起動コマンドは Dockerfile に記載されてるため無用)

```bash
uvicorn main:app --reload
```

Web ブラウザに「http://127.0.0.1:8000」と入力
