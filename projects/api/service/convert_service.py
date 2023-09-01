import base64
import uuid

def convert_to_canvas_glb(file_name:str,ext_without_dot:str, image_b64:str ) -> str:
    image = base64.b64decode(image_b64)
    tmp_file_name = uuid.uuid1()

    with open(f'{tmp_file_name}.{ext_without_dot}', 'wb') as f:
        f.write(image)
        f.close()
    print(f"GLBファイル書き出し DONE. original:{file_name} ,tmp:{tmp_file_name}")

    return "the glb"
