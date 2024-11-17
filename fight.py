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
    #队伍设置
    func.click_button(fd, Buttons["duiwushezhi"], 1)
    time.sleep(1)

    ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "repeatfight.png", 0.90)
    if ImgCmpRes is None:
        func.click_button(fd, Buttons["returndating"], 2)
        return
    else:
        #min_val, max_val, min_loc, max_loc, *res = ImgCmpRes
        func.click_button(fd, Buttons["repeatfight"])
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

    # # 读取主界面图像和模板图像
    # func.myscreenshoot(fd)
    # image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
    # template = cv2.imread('./figs/qizhinum.png', cv2.IMREAD_COLOR)
    # # 进行模板匹配
    # result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # # 找到匹配度最高的位置
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print("棋子数目0匹配度：", max_val)
    # # 设置匹配度阈值
    # # 匹配2是0.87
    # threshold = 0.86
    # if max_val >= threshold:
    #     print("棋子数目不足")
    #     return
    time.sleep(1)
    func.click_button(fd, Buttons["fight_button"], 1)
    time.sleep(1)
    func.click_button(fd, Buttons["jjc"], 1)

    while True:
        func.myscreenshoot(fd)
        ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "loading.png", 0.55)
        if ImgCmpRes is not None:
            print("--网络加载中")
            time.sleep(2)
        else:
            break

    while True:
        time.sleep(2)
        # #查看棋子数目够不够
        # func.myscreenshoot(fd)
        # image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        # template = cv2.imread('./figs/qizhinum.png', cv2.IMREAD_COLOR)
        # # 进行模板匹配
        # result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # # 找到匹配度最高的位置
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print("棋子数目0匹配度：", max_val)
        # # 设置匹配度阈值
        # # 匹配5是0.84
        # threshold = 0.86
        # if max_val >= threshold:
        #     print("棋子数目不足")
        #     time.sleep(2)
        #     func.click_button(fd, Buttons["returndating"])
        #     return
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
            #按比例修正点击位置
            scaled_num = func.get_scaled_width(fd)
            click_pos = (click_pos[0]*scaled_num, click_pos[1]*scaled_num)
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
        threshold = 0.86
        #未匹配到挑战按钮
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
            print("第1次拖拉后挑战按钮匹配度：", max_val)
            threshold = 0.86
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
            #按比例修正点击位置
            scaled_num = func.get_scaled_width(fd)
            click_pos = (click_pos[0]*scaled_num, click_pos[1]*scaled_num)
            func.myClick(fd, click_pos[0], click_pos[1])
            time.sleep(1)
        else:
            # 点击挑战
            top_left = max_loc  # 对于 cv2.TM_CCOEFF_NORMED 方法，使用 max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            click_pos = ((bottom_right[0] + top_left[0]) / 2, (bottom_right[1] + top_left[1]) / 2)
            #按比例修正点击位置
            scaled_num = func.get_scaled_width(fd)
            click_pos = (click_pos[0]*scaled_num, click_pos[1]*scaled_num)
            func.myClick(fd, click_pos[0], click_pos[1])
            time.sleep(1)

        func.click_button(fd, Buttons["kaishizhandou"], 2)

        # 匹配是否需要购买棋子
        func.myscreenshoot(fd)
        image = cv2.imread('./figs/screenshot.jpg', cv2.IMREAD_COLOR)
        template = cv2.imread('./figs/goumaiqizi.png', cv2.IMREAD_COLOR)
        # 进行模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # 找到匹配度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("购买棋子匹配度：", max_val)
        threshold = 0.80
        if max_val >= threshold:
            print("棋子数目不足")
            time.sleep(2)
            func.click_button(fd, Buttons["returndating"], 3)
            return
        # 确认后会进入一个点击任意屏幕位置的按钮
        # 挂机50s
        # while True:
        #     func.myscreenshoot(fd)
        #     ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "jjcheiping.png", 0.95)
        #     if ImgCmpRes is not None:
        #         continue
        #
        #     ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "jjcauto.png", 0.80)
        #     if ImgCmpRes is None:
        #         func.click_button(fd, Buttons["jjcauto"])
        #
        #     ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "jjcVictory.png", 0.80)
        #     if ImgCmpRes is not None:
        #         break
        #     else:
        #         time.sleep(10)

        #7s内持续检查
        check_num = 1
        while check_num < 30:
            func.myscreenshoot(fd)
            ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "jjcauto.png", 0.80)
            if ImgCmpRes is not None:
                break
            check_num += 1
            time.sleep(0.2)
        if check_num == 30:
            func.click_button(fd, Buttons["jjcauto"])

        while True:
            func.myscreenshoot(fd)
            ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "jjcVictory.png", 0.80)
            if ImgCmpRes is not None:
                break
            else:
                time.sleep(10)
        func.click_button(fd, Buttons["jieshu"], 2)

def choose_yuansu(fd, Buttons, boss_num):
    '''
    :param fd:
    :param button: Buttons[button_name]
    :param boss_num: boss序号
    :return:
    '''
    print("执行调教任务")
    func.click_button(fd, Buttons["returndating"], 2)  # 主界面唤醒
    func.click_button(fd, Buttons["fight_button"], 2)
    time.sleep(1)
    func.click_button(fd, Buttons["yuansu"], 1)
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
    #队伍设置
    func.click_button(fd, Buttons["duiwushezhi"], 1)
    time.sleep(1)

    ImgCmpRes = func.ImgCmp(fd, "screenshot.jpg", "repeatfight.png", 0.90)
    if ImgCmpRes is None:
        func.click_button(fd, Buttons["returndating"], 2)
        return
    else:
        #min_val, max_val, min_loc, max_loc, *res = ImgCmpRes
        func.click_button(fd, Buttons["repeatfight"])
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


