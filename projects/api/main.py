from fastapi import FastAPI
from pydantic import BaseModel
from .service import convert_service

class ImageModel(BaseModel):
    file_name: str
    image_body_b64: str
    ext_without_dot:str

app = FastAPI()

@app.get("/")
async def hello():
    return {"message" : "Hello,World1"}

@app.post("/images/to_canvas")
async def to_canvas(image:ImageModel):
    glb = "test"    
    glb = convert_service.convert_to_canvas_glb(image.file_name,image.ext_without_dot, image.image_body_b64)
    return {"fileName": image.file_name, "file":  image.image_body_b64 , "glb": glb}