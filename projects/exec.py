import subprocess
import sys

def main():
    if (len(sys.argv) == 1):
        print('ファイル名を指定してください')
        return 0
    subprocess.run(["python3", "create_texture.py", sys.argv[1], sys.argv[2]])
    subprocess.run(["blender", "--background", "--python", "set_texture.py", sys.argv[1]])

main()