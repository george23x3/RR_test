from PIL import Image
import numpy as np
import argparse
import os

RMSE = lambda w1 ,w2: np.sqrt(((w1 - w2)**2).mean())
size = 100
corner_1 = lambda pic: np.array(pic)[:size, :size]
corner_2 = lambda pic: np.array(pic)[-size:, :size]
corner_3 = lambda pic: np.array(pic)[:size, -size:]
corner_4 = lambda pic: np.array(pic)[-size:, -size:]

def clasification(image11, image22):
    image1 = image11.resize((1024, 1024))
    image2 = image22.resize((1024, 1024))
    our_RMSE = RMSE(np.array(image1), np.array(image2))
    if our_RMSE == 0:
        conclusion = 'duplicate'
    elif our_RMSE < 9.5:
        RMSE_arr = [RMSE(corner_1(image1), corner_1(image2)),
                    RMSE(corner_2(image1), corner_2(image2)),
                    RMSE(corner_3(image1), corner_3(image2)),
                    RMSE(corner_4(image1), corner_4(image2))]
        print(RMSE_arr)
        if max(RMSE_arr) - min(RMSE_arr) < 2 or (image11.size != image22.size):
            conclusion = "modification"
        else:
            conclusion = "similar"
    else:
        conclusion = 0
    return conclusion

def main(path):
    image_list = [Image.open(os.path.join(path, img)) for img in os.listdir(path) if not os.path.isdir(img)]
    for i in image_list:
        for j in image_list:
            if i != j:
                a = clasification(i, j)
                if a != 0:
                    print(i.filename+" "+a+" "+j.filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', metavar='PATH', required=True, help='folder with images')
    args = parser.parse_args()
    main(args.path)
