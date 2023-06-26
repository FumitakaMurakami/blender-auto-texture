# docker_blender導入からベイクスクリプト実行まで

## プロジェクトをクローン
```
git clone https://github.com/FumitakaMurakami/blender_bake_script.git
```

## docker_blenderのイメージpull

```
docker pull linuxserver/blender
```

## imageビルド
```
docker compose up -d --build
```

## アクセス
[localhost:3000](localhost:3000)

## スクリプト用のフォルダを作成する
blenderGUIもしくはdocker-compse execから
```
/config/projects
/config/projects/output/
/config/projects/input/
```
のディレクトリを作成

プロジェクトのターミナルで以下のコマンドからベイクスクリプトをサーバーへ送信

```
docker cp bake_script.py  blender:/config/projects
```

同じくテスト用のglbファイルを送信
（もしくはblenderGUIでモデルを作成しexport）
```
docker cp input/input.glb  blender:/config/projects/input
```

## スクリプト実行
blenderコマンドを有効化するためにパスを通す
```
docker-compose exec alias blender='bin/Blender'
```

以下のコマンドでスクリプト実行
```
docker-compose exec blender blender --background --python /config/projects/bake_script.py
```

`/config/projects/output/`フォルダにベイク済みのoutput.glbが生成される

## ローカルでスクリプトを実行する場合
`/output`ディレクトリを作成

blenderコマンドを有効化させるためにblender.exeファイルのある場所にパスを通す

pythonファイルの各パスをローカル用の物に変更。（コメントアウトを解除する）
```bake_script.py
# ローカル環境のパス
model_path = './input/input.glb'
output_path = './output/output.glb'
texture_path = "./output/output.png"
```



以下のスクリプトで実行
`blender blender --background --python /config/projects/bake_script.py`
