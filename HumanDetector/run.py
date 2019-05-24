import socket
import zlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


def recv_all(sock):
    BUF = 4096
    data = b''
    while True:
        part = sock.recv(BUF)
        data += part
        if len(part) < BUF:
            break
    return data


def get_image():
    # 소켓(Socket) 객체를 생성합니다.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 42424))

    received = recv_all(s)
    # print(received) 서버로부터 전달 받은 메시지를 확인
    received = recv_all(s)
    # print(received) 서버로부터 전달 받은 메시지를 확인
    file_size = str(received[56:])[2:].split(')')[0]
    file_size = int(file_size)
    print('파일 크기: ' + str(file_size))

    s.send(b'enter\n')
    image = recv_all(s)
    # print(image[file_size - 1000:]) 뒤에 멘트가 포함되어 있는지 확인
    image = image.split(b'[+]')[0]
    print('이미지 크기: ' + str(len(image)))
    image = zlib.decompress(image)
    print('압축 해제된 이미지 크기: ' + str(len(image)))
    return image


FILE_NAME = 'file.png'
image = get_image()
file = open(FILE_NAME, "wb")
file.write(image)
file.close()
print('파일 저장 완료: %s' %(FILE_NAME))

# 전체 이미지를 출력합니다.
img = imread(FILE_NAME)
plt.figure(figsize=(20, 4))
plt.imshow(img)
plt.show()

# 이미지를 100개로 나누어 하나를 출력합니다.
img2 = np.hsplit(img, 100)[0]
plt.figure(figsize=(20, 4))
plt.imshow(img2)
plt.show()

# 0. 먼저 이미지를 100개로 분할하여 하나씩 확인해 볼 수 있습니다.
'''
img = cv2.imread(FILE_NAME)
for i in range(0, 100):
    img2 = np.hsplit(img, 100)[i]
    cv2.imwrite('./images/' + str(i) + '.png', img2)
'''
# 1. 배경과 폰트가 있으므로, 이를 활용해 직접 캡차 트레이닝 이미지를 생성할 수 있습니다.
# 2. 하지만, 그냥 보았을 때는 그렇게 안 해도 풀 수 있을 것 같습니다. 한 번 시도해 봅시다.
# 이미지를 각각 A부터 Z까지 폴더에 직접 분류하여 담아봅시다.
# 담는 과정에서, 각 글자가 헷갈려 제대로 담지 못할 수 있습니다.
# 애초에 인간보다 더 글자를 잘 분류하도록 인공지능을 만들어야 합니다.
# 따라서 font.ttf 를 이용하여 실제로 해당 글씨를 써봐야 합니다.
# font.ttf 로 각 글씨를 써본 뒤에, 정확히 분류해서 폴더에 담아봅시다.
'''
from PIL import Image, ImageDraw, ImageFont

# 배경 이미지 생성
image = np.full((100, 60, 3), 255)
cv2.imwrite('made.png', image)

# 이미지 열어서 글자 그리기
image = Image.open('made.png')
font = ImageFont.truetype('font.ttf', size=100)
(x, y) = (0, 0)
message = "A"
color = "rgb(0, 0, 0)"
draw = ImageDraw.Draw(image)
draw.text((x, y), message, fill=color, font=font)
image.save('made.png')

# 만든 글자 이미지 확인
img = imread('made.png')
plt.figure(figsize=(20, 4))
plt.imshow(img)
plt.show()
'''
# 이제 대략적으로 분류가 되었습니다. 한 번, 검은색만 추출해서 글씨를 확인합시다.
# 그 이후에 잘못 판단한 글자가 있다면, 정확한 폴더로 재분류합니다.
# 이 때, 제대로 분류가 안 되고 판단이 안 서는 글자는 지워버립니다. (거의 90% 확신만 남깁니다.)
# 하나씩 이미지를 불러오는 방법은 다음과 같습니다.
'''
# 하나의 이미지 불러오기
image = cv2.imread('./images/0.png')

# 검은색이 아닌 색상은 모두 하얀색으로 변경
c = image[:, :, 0] != 0
image[c] = [255, 255, 255]
cv2.imwrite('temp.png', image)

# 만든 글자 이미지 확인
img = imread('temp.png')
plt.figure(figsize=(20, 4))
plt.imshow(img)
plt.show()
'''
# 폴더의 모든 .png 파일을 검은 색만 남기는 방법은 다음과 같습니다.
'''
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
'''
# 이미지를 확인해 보면 배경 이미지에서 특정 부분에 글자를 쓰고,
# (글자를 쓸 때는 약간의 회전 값을 주어, 크기도 약간씩 바꾸며 씁니다.)
# 그 글자를 기준으로 주변 이미지를 뽑아냅니다. (글자의 왼쪽 끝부터 60 X 100)
# 이후에 가장 많이 겹치는 색을 검은색으로 바꾸는 방식입니다.
# 따라서, 이렇게 이미지를 직접 추출해서 분류한 뒤에 이미지 분류 알고리즘을 쓸 수 있습니다.
# 간단히 KNN 알고리즘을 사용해보도록 합시다.

