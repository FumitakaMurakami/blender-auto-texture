# docker_blender 導入からベイクスクリプト実行まで

## docker_blender のイメージ pull

```sh
docker pull linuxserver/blender
```

## ビルド

```sh
docker compose up -d --build
```

## WebGUI アクセス

[localhost:13010](localhost:13010)

## 自動テクスチャ加工実行

以下のコマンドで実行

input ディレクトリにキャンバスに貼り付けたい画像舗を保存しファイル名をコマンドオプションに入力

※第一オプションにファイル名、第二オプションにテクスチャ化したい画像の拡張子を指定してください

```sh
docker exec blender-auto-texture python3 exec.py ファイル名 拡張子
```

以下のコマンドが順に実行されます。

```sh
python3 create_texture.py ファイル名 拡張子
blender --background --python set_texture.py　ファイル名
```

# WebAPI インターフェイス

ユーザーに対して API アクセスを可能とする。
API インターフェイスは以下。

## WebAPI へのアクセス

Web ブラウザに「http://127.0.0.1:8000」と入力、以下のメッセージが出ていればOK

```
{"message":"Hello,World"}
```

## API Document

以下にアクセスすることで API ドキュメントが参照可能。

```
http://localhost:8000/docs
```

```
http://127.0.0.1:8000/redoc
```

## 注意

! 本番環境では、Dockerfile の--reload を外すこと。

本システムでの[FastAPI の設定](./docs/fastapi.md)を参照
