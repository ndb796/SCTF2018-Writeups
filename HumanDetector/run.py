import socket
import time
import zlib
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


# 서버로부터 이미지를 받아 파일로 저장합니다.
FILE_NAME = 'file.png'
image = get_image()
file = open(FILE_NAME, "wb")
file.write(image)
file.close()
print('파일 저장 완료: %s' %(FILE_NAME))

# 저장된 이미지를 화면에 출력합니다.
img = imread(FILE_NAME)
plt.figure(figsize=(20, 4))
plt.imshow(img)
plt.show()