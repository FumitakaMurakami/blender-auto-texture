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

```
docker exec blender-auto-texture python create_texture.py
docker exec blender-auto-texture blender --background --python set_texture.py
```

## ローカルでスクリプトを実行する場合

blender コマンドを有効化させるために blender.exe ファイルのある場所にパスを通す

inputディレクトリにキャンバスに貼り付けたい画像舗を保存し、input.pngに名前を変更

以下のスクリプトで実行

`cd projects`

`python create_texture_script.py` //テクスチャ作成

`blender --background --python set_texture.py` //テクスチャ貼り付け、glb生成
