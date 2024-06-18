import cv2 as cv
import numpy as np
import os
from datetime import datetime
import time

def face_detect_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    face_detector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(gray, 1.2, 6)
    has_faces = len(faces) > 0
    face_images = []  # 存储裁剪后的人脸
    for i, (x, y, w, h) in enumerate(faces):
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        face_images.append(image[y:y+h, x:x+w])  # 裁剪人脸
    return has_faces, image, face_images  # 返回是否检测到人脸、标记的图像和裁剪后的人脸

print("------------------")

# 创建以当前日期命名的文件夹
folder_name = datetime.now().strftime("%Y-%m-%d")
os.makedirs(folder_name, exist_ok=True)

# 创建一个文件夹来存储没有红框的截图
no_face_folder_name = f"no_face_{folder_name}"
os.makedirs(no_face_folder_name, exist_ok=True)

# 创建一个文件夹来存储提取的人脸
face_folder_name = "face"
os.makedirs(face_folder_name, exist_ok=True)

capture = cv.VideoCapture(0)
cv.namedWindow("result", cv.WINDOW_NORMAL)  # 设置窗口大小可调整
cv.resizeWindow("result", 640, 480)

# 初始化上一个截图的时间戳
last_screenshot_time = time.time()

while True:
    ret, frame = capture.read()
    if not ret:
        print("无法获取视频帧，退出循环")
        break

    frame = cv.flip(frame, 1)  # 左右翻转
    has_faces, frame_with_detection, face_images = face_detect_demo(frame)

    # 显示带有检测结果的帧
    cv.imshow('result', frame_with_detection)

    if has_faces:
        face_folder_path = folder_name
    else:
        face_folder_path = no_face_folder_name

    # 控制截图间隔
    current_time = time.time()
    if current_time - last_screenshot_time >= 5:  # 修改为每5秒保存一次
        screenshot_path = os.path.join(face_folder_path,
                                       f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
        cv.imwrite(screenshot_path, frame)
        print(f"截图已保存为：{screenshot_path}")
        last_screenshot_time = current_time  # 更新上一个截图的时间戳

        # 保存提取的人脸
        for i, face_image in enumerate(face_images):
            face_path = os.path.join(face_folder_name, f"face_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{i}.jpg")
            cv.imwrite(face_path, face_image)
            print(f"人脸已保存为：{face_path}")

    # 检查是否按下ESC键
    key = cv.waitKey(1)
    if key == 27:  # ESC键的ASCII码为27
        break

capture.release()
cv.destroyAllWindows()
