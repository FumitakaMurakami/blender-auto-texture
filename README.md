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

```sh
docker exec blender-auto-texture python3 create_texture.py ファイル名
docker exec blender-auto-texture blender --background --python set_texture.py
```

# WebAPI インターフェイス

ユーザーに対して API アクセスを可能とする。
API インターフェイスは以下。

# WebAPI へのアクセス

Web ブラウザに「http://127.0.0.1:8000」と入力、以下のメッセージが出ていればOK

```
{"message":"Hello,World"}
```

本システムでの[FastAPI の設定](./docs/fastapi.md)を参照
