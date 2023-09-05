import subprocess
import sys

def execute_image_to_canvas_glb(file_name_without_ext:str, ext_without_dot:str):
    subprocess.run(["python3", "create_texture.py", file_name_without_ext, ext_without_dot])
    subprocess.run(["blender", "--background", "--python", "set_texture.py", file_name_without_ext])

def main():
    if (len(sys.argv) == 1):
        print('ファイル名を指定してください')
        return 0
    if (len(sys.argv) == 2):
        print('ファイル拡張子（ドットなし）を指定してください')
        return 0
    
    execute_image_to_canvas_glb(sys.argv[1], sys.argv[2]);

# main()