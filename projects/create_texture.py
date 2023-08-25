import cv2

def set_texture(img1_path, img2_path, output_path):

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img1 = cv2.resize(img1, (985, 946))
    img1 = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

    height, width = img1.shape[:2]
    img2[19:height+19, 12:width+12] = img1

    cv2.imwrite(output_path, img2)

def main():
    # パス
    img1_path = './input/input.png'
    img2_path = './input/canvas_tex.jpg'
    texture_path = "./output/texture.png"

    set_texture(img1_path, img2_path, texture_path)

if __name__ == '__main__':
    main()