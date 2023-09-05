from fastapi import FastAPI
from pydantic import BaseModel
from .service import convert_service
from starlette.middleware.cors import CORSMiddleware # 追加
from fastapi.responses import HTMLResponse,Response


from exec import execute_image_to_canvas_glb
import replicate


import os
os.environ["REPLICATE_API_TOKEN"] = "r8_DBLUcNEuA84rf9OsfxlIyDMdss1wSff2prgrv"

class ImageModel(BaseModel):
    file_name: str
    image_body_b64: str
    ext_without_dot:str

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/")
async def hello():
    return {"message" : "Hello,World1"}


# アップローダのHTMLを返却
@app.get("/app/{file}", response_class=HTMLResponse)
async def web_ui(file:str):
    print("file"+ file)
    with open(f"/projects/webapp/{file}") as f:
        text = f.read()
    return text


# イメージをキャンバスに貼る
@app.post("/images/to_canvas")
async def to_canvas(image:ImageModel):
    print("to_canvas",image.file_name,image.ext_without_dot)
    image_file_name_without_ext = convert_service.write_image_file(image.file_name,image.ext_without_dot, image.image_body_b64)
    execute_image_to_canvas_glb(image_file_name_without_ext,image.ext_without_dot)

    glb_file_name =image_file_name_without_ext + ".glb"
    return { "get_model_url":  f"/models/{glb_file_name}" , "glb":glb_file_name}


# モデルをダウンロードするURL
@app.get("/models/{file_with_ext}",responses = {
        200: {
            "content": {"model/gltf-binary": {}}
        }, 
    },response_class=Response)

async def get_model(file_with_ext):
    print("get model",file_with_ext)
    glb_file = f"/projects/output/{file_with_ext}"
    with open(glb_file, 'rb') as file:
        model_bytes: bytes =  file.read()
    return Response(content=model_bytes, media_type="model/gltf-binary")


# openJourneyでイメージを生成する
@app.get("/images/create_oj")
async def get_midj_image_oj(prompt:str):
    # replicate.Client(api_token="r8_7V5KC1ltomyUpRE1LB5MaZpugEmEFhK0xSkDV")
    output = replicate.run(
        "prompthero/openjourney:ad59ca21177f9e217b9075e7300cf6e14f7e5b4505b87b9689dbd866e9768969",
        input={
            "prompt": f"mdjrny-v4 style {prompt}",
            "num_outputs" : 4 
        }
    )
    # The prompthero/openjourney model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    return output
    # for item in output:
    #     # https://replicate.com/prompthero/openjourney/versions/ad59ca21177f9e217b9075e7300cf6e14f7e5b4505b87b9689dbd866e9768969/api#output-schema
    #     print(item)


