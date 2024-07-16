import os
import random
import sys
import func
import pyautogui
import time
import cv2
import win32gui
import win32con
import win32api
import psutil
import win32process
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication

def choose_taofa(fd, Buttons, boss_num):
    '''
    :param fd:
    :param button: Buttons[button_name]
    :param boss_num: boss序号
    :return:
    '''
    print("执行讨伐任务")
    func.click_button(fd, Buttons["returndating"], 2)  # 主界面唤醒
    func.click_button(fd, Buttons["fight_button"], 2)
    time.sleep(1)
    func.click_button(fd, Buttons["taofa"], 1)
    time.sleep(1)
    if boss_num > 3:
        # 拖拽鼠标
        # 获取窗口的矩形（左上角和右下角的坐标）
        rect = win32gui.GetClientRect(fd)
        # 计算拖拽起始位置, 固定的
        start_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3])
        end_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3]/5)
        func.drag_mouse(fd, start_pos, end_pos)#前台拖拽没问题
        boss_num = boss_num - 3
    func.click_button(fd, Buttons["taofa_boss"+str(boss_num)], 1)
    time.sleep(1)
    #战斗设置
    func.click_button(fd, Buttons["kaishizhandou"], 2)
    time.sleep(1)
    #战斗开始
    func.click_button(fd, Buttons["kaishizhandou"], 2)
    time.sleep(3)
    #以下为返回大厅操作
    func.click_button(fd, Buttons["autofight_button1"])
    time.sleep(1)
    func.click_button(fd, Buttons["autofight_button2"])
    time.sleep(1)
    func.click_button(fd, Buttons["returndating"])

def choose_jjc(fd, Buttons):
    """
    :param fd:
    :param Buttons:
    :return:
    """
    print("执行jjc任务")
    func.click_button(fd, Buttons["returndating"], 2)  # 主界面唤醒

    # 读取主界面图像和模板图像
    func.myscreenshoot(fd)
    image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
    template = cv2.imread('./figs/qizhinum.png', cv2.IMREAD_COLOR)
    # 进行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 找到匹配度最高的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("棋子数目0匹配度：", max_val)
    # 设置匹配度阈值
    # 匹配2是0.87
    threshold = 0.88
    if max_val >= threshold:
        print("棋子数目不足")
        return

    func.click_button(fd, Buttons["fight_button"], 1)
    time.sleep(1)
    func.click_button(fd, Buttons["jjc"], 1)
    while True:
        time.sleep(4)
        #查看棋子数目够不够
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template = cv2.imread('./figs/qizhinum.png', cv2.IMREAD_COLOR)
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("棋子数目0匹配度：", max_val)
        # 设置匹配度阈值
        # 匹配5是0.84
        threshold = 0.88
        if max_val >= threshold:
            print("棋子数目不足")
            time.sleep(2)
            func.click_button(fd, Buttons["returndating"])
            return
        #棋子数目足够
        #匹配npc对战的小红点
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template = cv2.imread('./figs/npc.png', cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("NPC对战匹配度：", max_val)
        # 设置匹配度阈值
        # 匹配到0.85
        threshold = 0.83
        if max_val <= threshold:
            print("无人机关卡")
            time.sleep(2)
            func.click_button(fd, Buttons["returndating"])
            return
        else:
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # 点击NPC对战
            click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1])
            time.sleep(2)

        # 匹配挑战按钮
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template = cv2.imread('./figs/tiaozhan.png', cv2.IMREAD_COLOR)
        # 获取模板的宽度和高度
        template_height, template_width = template.shape[:2]
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("挑战按钮匹配度：", max_val)
        threshold = 0.9
        if max_val <= threshold:
            # 拖拽鼠标
            # 获取窗口的矩形（左上角和右下角的坐标）
            rect = win32gui.GetClientRect(fd)
            # 计算拖拽起始位置, 固定的
            start_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3])
            end_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3] / 2)
            func.drag_mouse(fd, start_pos, end_pos)  # 前台拖拽没问题
            time.sleep(1)

            # 重新匹配挑战按钮
            func.myscreenshoot(fd)
            image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
            template = cv2.imread('./figs/tiaozhan.png', cv2.IMREAD_COLOR)
            # 获取模板的宽度和高度
            template_height, template_width = template.shape[:2]
            # 进行模板匹配
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            # 找到匹配度最高的位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("第一次拖拉后挑战按钮匹配度：", max_val)
            threshold = 0.9
            if max_val <= threshold:
                # 拖拽鼠标
                # 获取窗口的矩形（左上角和右下角的坐标）
                rect = win32gui.GetClientRect(fd)
                # 计算拖拽起始位置, 固定的
                start_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3])
                end_pos = (Buttons["taofa_boss3"][0] * rect[2], Buttons["taofa_boss3"][1] * rect[3] / 2)
                func.drag_mouse(fd, start_pos, end_pos)  # 前台拖拽没问题
                time.sleep(1)
                # 重新匹配挑战按钮
                func.myscreenshoot(fd)
                image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
                template = cv2.imread('./figs/tiaozhan.png', cv2.IMREAD_COLOR)
                # 获取模板的宽度和高度
                template_height, template_width = template.shape[:2]
                # 进行模板匹配
                result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                # 找到匹配度最高的位置
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                print("第2次拖拉后挑战按钮匹配度：", max_val)

            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # 点击挑战
            click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1])
        else:
            # 点击挑战
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
            func.myClick(fd, click_pos[0], click_pos[1])

        func.click_button(fd, Buttons["kaishizhandou"], 2)
        # 确认后会进入一个点击任意屏幕位置的按钮
        # 挂机50s
        time.sleep(50)
        func.click_button(fd, Buttons["jieshu"], 2)





        # if max_val >= threshold:
        #     # 获取匹配结果的位置
        #     top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
        #     bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        #     # 点击NPC对战
        #     click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
        #     func.myClick(fd, click_pos[0], click_pos[1])
        #     time.sleep(2)
        #     #匹配挑战按钮
        #     func.myscreenshoot(fd)
        #     image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        #     template = cv2.imread('./figs/tiaozhan.png', cv2.IMREAD_COLOR)
        #     # 获取模板的宽度和高度
        #     template_height, template_width = template.shape[:2]
        #     # 进行模板匹配
        #     result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        #     # 找到匹配度最高的位置
        #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #     top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
        #     bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        #     # 点击挑战
        #     click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
        #     func.myClick(fd, click_pos[0], click_pos[1])
        #
        #     func.click_button(fd, Buttons["kaishizhandou"], 2)
        #     # 确认后会进入一个点击任意屏幕位置的按钮
        #     # 挂机50s
        #     time.sleep(50)
        #     func.click_button(fd, Buttons["jieshu"], 2)
        # #没有人机关卡打，返回主界面
        # else:
        #     time.sleep(2)
        #     func.click_button(fd, Buttons["returndating"])
        #     return

# 通过句柄获取【线程ID 进程ID】
# hread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
# print(hread_id)
# print(process_id)

def a(aa):
    if aa:
        print(1)
    else:
        return

