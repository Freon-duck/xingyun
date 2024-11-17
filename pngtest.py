#必须得有gui不然图片会出错
import os

import pyautogui

import time
import cv2
from PyQt5.QtWidgets import QApplication
import numpy as np
import win32gui
import func

def img(imgPath):
    return os.path.join("./figs/", imgPath)

# 读取输入图像和模板图像
fd = func.get_WindowPoint()
time.sleep(2)

#测试点位######################################################
#func.click_button_test(fd)


func.myscreenshoot(fd)
path = "./figs/"
image = cv2.imread("./figs/test/jjcheiping.png", cv2.IMREAD_COLOR)
image = cv2.imread(path+"screenshot.jpg", cv2.IMREAD_COLOR)
template = cv2.imread("./figs/qizhinum.png", cv2.IMREAD_COLOR)

# 获取模板的宽度和高度
template_height, template_width = template.shape[:2]

# 进行模板匹配
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# 找到匹配度最高的位置
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_val)
# 设置不同的匹配度阈值
thresholds = [0.3]

for threshold in thresholds:
    if max_val >= threshold:
        # 获取匹配结果的位置
        top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        center = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
        print(center)
        # 在原图上绘制矩形框标记出匹配区域
        image_copy = image.copy()
        cv2.rectangle(image_copy, top_left, bottom_right, (0, 255, 0), 2)

        # 显示结果图像
        cv2.imshow(f'Detected Template at threshold {threshold}', image_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"No match found or match confidence below threshold {threshold}")
