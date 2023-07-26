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

[localhost:13000](localhost:13000)

## ベイクスクリプト実行

以下のコマンドでスクリプト実行

```
docker-compose exec blender blender --background --python /projects/bake_script.py
```

1−2 分後 `/projects/output/`フォルダにベイク済みの output.glb が生成される

## ローカルでスクリプトを実行する場合

blender コマンドを有効化させるために blender.exe ファイルのある場所にパスを通す

以下のスクリプトで実行
`blender --background --python /config/projects/bake_script.py`
