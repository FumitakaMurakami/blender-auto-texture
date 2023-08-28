import cv2
import sys

def trimImg(img):
    height, width = img.shape[:2]

    top = 0
    bottom = height
    left = 0
    right = width

    if (height > 946):
        top = int((height / 2) - (946 / 2))
        bottom = top + 946
        print('テクスチャの高さをトリミングしました')

    if (width > 985):
        left = int((width / 2) - (985 / 2))
        right = left + 985
        print('テクスチャの幅をトリミングしました')

    return img[top:bottom, left:right]


def set_texture(img1_path, img2_path, output_path):

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img1 = trimImg(img1)
    img1 = cv2.resize(img1, (985, 946))
    img1 = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

    height, width = img1.shape[:2]
    img2[19:height+19, 12:width+12] = img1

    cv2.imwrite(output_path, img2)

    print('テクスチャを適用しました')

def main():
    if (len(sys.argv) == 1):
        print('ファイル名を指定してください')
        return 0
    # パス
    img1_path = './input/' + sys.argv[1]
    img2_path = './input/canvas_tex.jpg'
    texture_path = "./output/texture.png"

    set_texture(img1_path, img2_path, texture_path)

if __name__ == '__main__':
    main()