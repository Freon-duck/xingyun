import os
import sys
import time

import cv2
import win32gui
import win32con
import win32api
import func
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication

items = ["lvpiao", "huangpiao"]

def buy(fd, Buttons, items):
    '''
    :param fd:
    :param Buttons:
    :param items:
    :return:
    '''
    func.click_button(fd, "shenmishangdian")
    time.sleep(1)

    func.myscreenshoot(fd)
    image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
    for item in items:
        fullpath = 'figs/'+ item +'.png'
        template = cv2.imread(fullpath, cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("max_val=", max_val)
        # 设置匹配度阈值
        # 匹配到0.999
        # 匹配到买完的0.726
        # 未匹配到0.5
        threshold = 0.95
        if max_val >= threshold:
            # 获取匹配结果的位置
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # #计算中心点
            # center = ((bottom_right[0]+top_left[0])/2, (bottom_right[1]+top_left[1])/2)
            # print(center)
            # 获取窗口的矩形（左上角和右下角的坐标）
            rect = win32gui.GetClientRect(fd)
            # 点击购买
            click_pos = (rect[2] * Buttons["shenmi_buy"], (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1])

    # 拖动屏幕购买最下的
    rect = win32gui.GetClientRect(fd)
    # 计算拖拽起始位置, 固定的
    start_pos = (0.5 * rect[2], 0.6 * rect[3])
    end_pos = (0.5 * rect[2], 0.6 * rect[3] / 5)
    func.drag_mouse(fd, start_pos, end_pos)  # 前台拖拽没问题

    func.myscreenshoot()
    image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
    for item in items:
        fullpath = 'figs/' + item + '.png'
        template = cv2.imread(fullpath, cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("max_val=", max_val)
        # 设置匹配度阈值
        # 匹配到0.999
        # 匹配到买完的0.726
        # 未匹配到0.5
        threshold = 0.95
        if max_val >= threshold:
            # 获取匹配结果的位置
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # #计算中心点
            # center = ((bottom_right[0]+top_left[0])/2, (bottom_right[1]+top_left[1])/2)
            # print(center)
            # 获取窗口的矩形（左上角和右下角的坐标）
            rect = win32gui.GetClientRect(fd)
            # 点击购买
            click_pos = (rect[2] * Buttons["shenmi_buy"], (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1])


def buy_lvpiao(fd, Buttons):
    print("这是绿票购买")
    func.click_button(fd, Buttons["returndating"])#主界面唤醒
    time.sleep(1)
    func.click_button(fd, Buttons["shop_button"])
    time.sleep(1)
    func.click_button(fd, Buttons["shenmishangdian"])
    time.sleep(1)

    itemlist = ["lvpiao", "huangpiao"]
    for item in itemlist:
        # 读取输入图像和模板图像
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template_path = f'figs/{item}.png'
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("max_val=", max_val)
        # 设置匹配度阈值
        #匹配到0.999
        #匹配到买完的0.726
        #未匹配到0.5
        threshold = 0.88
        if max_val >= threshold:
            # 获取匹配结果的位置
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # 获取窗口的矩形（左上角和右下角的坐标）
            rect = win32gui.GetClientRect(fd)
            #点击购买
            click_pos = (rect[2]*Buttons["shenmi_buy"][0], (bottom_right[1]+top_left[1])/2)
            func.myClick(fd, click_pos[0], click_pos[1])
            time.sleep(1)
            func.myClick(fd, rect[2] * Buttons["queren_buy"][0], rect[3] * Buttons["queren_buy"][1])
    time.sleep(2)
    #拖动屏幕购买最下的
    rect = win32gui.GetClientRect(fd)
    # 计算拖拽起始位置, 固定的
    start_pos = (0.5 * rect[2], 0.6 * rect[3])
    end_pos = (0.5 * rect[2], 0.6 * rect[3] / 5)
    func.drag_mouse(fd, start_pos, end_pos)  # 前台拖拽没问题
    time.sleep(1)#这里不睡一下后面点击不了，很奇怪

    for item in itemlist:
        # 读取输入图像和模板图像
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template_path = f'figs/{item}.png'
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("max_val=", max_val)
        # 设置匹配度阈值
        # 匹配到0.999
        # 匹配到买完的0.726
        # 未匹配到0.5
        threshold = 0.88
        if max_val >= threshold:
            # 获取匹配结果的位置
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # 获取窗口的矩形（左上角和右下角的坐标）
            rect = win32gui.GetClientRect(fd)
            # 点击购买
            click_pos = (rect[2] * Buttons["shenmi_buy"][0], (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1], 1)
            time.sleep(1)
            func.myClick(fd, rect[2] * Buttons["queren_buy"][0], rect[3] * Buttons["queren_buy"][1])
    time.sleep(1)
    func.click_button(fd, Buttons["returndating"], 2)
