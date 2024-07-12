import os
import random
import sys
import func
import pyautogui
import time
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
    func.click_button(fd, Buttons["kaishizhandou"], 2)
    time.sleep(1)
    func.click_button(fd, Buttons["kaishizhandou"], 2)
    time.sleep(3)
    func.click_button(fd, Buttons["autofight_button1"])
    func.click_button(fd, Buttons["autofight_button2"])




# 通过句柄获取【线程ID 进程ID】
# hread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
# print(hread_id)
# print(process_id)



