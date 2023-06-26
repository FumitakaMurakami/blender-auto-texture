# docker_blender導入からベイクスクリプト実行まで

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
docker cp input/input.glb  blender:/config/projects
```

## スクリプト実行
```
docker-compose exec blender blender --background --python /config/projects/bake_script.py
```

`/config/projects/output/`フォルダにベイク済みのoutput.glbが生成される