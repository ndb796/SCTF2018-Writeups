import os
import cv2
import numpy as np


folder_names = list(range(ord('A'), ord('Z')))
train = []
train_labels = []
print(folder_names)


# A부터 Z 까지의 폴더를 하나씩 확인합니다.
for folder_name in folder_names:
    # 각 폴더에 있는 모든 파일명을 확인합니다.
    path = './images/' + chr(folder_name) + '/'
    file_names = next(os.walk(path))[2]
    for file_name in file_names:
        # 모든 파일을 하나씩 확인하며, 이미지와 라벨을 각각 넣습니다.
        img = cv2.imread(path + file_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        train.append(gray)
        train_labels.append(chr(folder_name))


# 이미지 크기가 (60 X 100)이므로 6,000으로 형태 변환
x = np.array(train)
train = x[:, :].reshape(-1, 6000).astype(np.float32)
train_labels = np.array(train_labels)[:, np.newaxis]
np.savez("trained.npz", train=train, train_labels=train_labels)
