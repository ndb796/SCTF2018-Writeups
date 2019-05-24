import os
import cv2


def png_to_black_in_folder(path):
    file_list = os.listdir(path)
    file_list.sort()

    png_file_list = []
    for file in file_list:
        if file.find('.png') is not -1:
            png_file_list.append(file)

    for png_file in png_file_list:
        image = cv2.imread(path + png_file)

        # 검은색이 아닌 색상은 모두 하얀색으로 변경
        c = image[:, :, 0] != 0
        image[c] = [255, 255, 255]
        cv2.imwrite(path + png_file, image)


# images 안에 있는 A ~ Z 폴더 안에 있는 모든 이미지 하얀색으로 변경
folder_list = os.listdir('./images')
folder_list.sort()
for folder in folder_list:
    png_to_black_in_folder('./images/' + folder + '/')
