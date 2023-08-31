import cv2
import sys

def adjustImg(img, height, width):
    longest_edge = max(height, width)
    top = 0
    bottom = 0
    left = 0
    right = 0
    if (height < longest_edge):
        diff_h = longest_edge - height
        top = diff_h // 2
        bottom = diff_h - top
    elif (width < longest_edge):
        diff_w = longest_edge - width
        left = diff_w // 2
        right = diff_w - left
    else:
        pass
        
    img = cv2.copyMakeBorder(img, top, bottom, left, right,
                            cv2.BORDER_CONSTANT, value=[255, 255, 255])
    print('短編を延長しました')

    return img

def trimImg(img, setH, setW):
    height, width = img.shape[:2]

    top = 0
    bottom = height
    left = 0
    right = width

    if (height > setH and width > setW):
        top = int((height / 2) - (setH / 2))
        bottom = top + setH
        print('テクスチャの高さをトリミングしました')

        left = int((width / 2) - (setW / 2))
        right = left + setW
        print('テクスチャの幅をトリミングしました')

        return img[top:bottom, left:right]

    if (height > setH and width < setW):
        top = int((height / 2) - (setH / 2))
        bottom = top + setH
        print('テクスチャの高さをトリミングしました')

        img = adjustImg(img[top:bottom, left:right], bottom, right)
        height, width = img.shape[:2]
        left = int((width / 2) - (setW / 2))
        right = left + setW
        print('テクスチャの幅をトリミングしました')
        
        return img[0:height, left:right]

    if (height < setH and width > setW):
        left = int((width / 2) - (setW / 2))
        right = left + setW
        print('テクスチャの幅をトリミングしました')

        img = adjustImg(img[top:bottom, left:right], bottom, right)
        height, width = img.shape[:2]
        top = int((height / 2) - (setH / 2))
        bottom = top + setH
        print('テクスチャの高さをトリミングしました')

        return img[top:bottom,0:width]

    if (height < setH and width < setW):
        img = adjustImg(img, height, width)
        
        return img


def set_texture(img1_path, img2_path, output_path):

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img1 = trimImg(img1 ,946, 985)
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
    img1_path = './input/' + sys.argv[1] + '.' + sys.argv[2]
    img2_path = './input/canvas_tex.jpg'
    texture_path = './output/'+ sys.argv[1] + '.png'

    set_texture(img1_path, img2_path, texture_path)

if __name__ == '__main__':
    main()