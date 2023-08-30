# docker_blender 導入からベイクスクリプト実行まで

## docker_blender のイメージ pull

```
docker pull linuxserver/blender
```

## ビルド

```
docker compose up -d --build
```

## WebGUI アクセス

[localhost:13010](localhost:13010)

## 自動テクスチャ加工実行

以下のコマンドで実行

inputディレクトリにキャンバスに貼り付けたい画像舗を保存しファイル名をコマンドオプションに入力

```
docker exec blender-auto-texture python3 create_texture.py ファイル名
docker exec blender-auto-texture blender --background --python set_texture.py
```


