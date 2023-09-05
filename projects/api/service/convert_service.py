import base64
import uuid

def write_image_file(file_name:str,ext_without_dot:str, image_b64:str ) -> str:
    image = base64.b64decode(image_b64.replace("data : ", ""))
    file_name = f"{uuid.uuid1()}";
    tmp_file_name = f"/projects/input/{ file_name }.{ext_without_dot}"
    print(tmp_file_name)

    with open(tmp_file_name, 'wb') as f:
        f.write(image)

    return file_name
