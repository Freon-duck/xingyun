from ctypes import windll
from PIL import Image
import numpy as np
import os
import random
import time
import cv2
import win32ui
import win32gui
import win32con
import win32api
import sys

from PyQt5.QtWidgets import QApplication


def get_WindowPoint():
    """
    获取窗口句柄
    :return 返回该句柄
    """
    time.sleep(2)
    # point = win32api.GetCursorPos()
    # print("cur_point:", point)
    # 通过坐标获取坐标下的【窗口句柄】
    # fd = win32gui.WindowFromPoint(point)
    # print("fd:", fd)
    # window_title = win32gui.GetWindowText(fd)
    # print(f"Window title: {window_title}")
    # class_name = win32gui.GetClassName(fd)
    # print(f"Class name: {class_name}")
    #hwnd_again = win32gui.FindWindow(class_name, window_title)

    fd = win32gui.FindWindow("Qt5156QWindowIcon", "MuMu模拟器12")#父
    #fd = win32gui.FindWindow("Qt5156QWindowIcon", "MuMu模拟器12-1")  # 父
    fd = win32gui.FindWindowEx(fd, None, "Qt5156QWindowIcon", "MuMuPlayer")#子
    print(f"Found window handle: {fd}")
    # hwnd_again = win32gui.FindWindow("Qt5156QWindowIcon", "MuMuPlayer")#直接用搜出来的句柄是0，初步怀疑是该函数是只能用于最外层的
    # print(f"Found window handle: {hwnd_again}")
    # hwnd_again = win32gui.FindWindow("nemuwin", "nemudisplay")
    # print(f"Found window handle: {hwnd_again}")
    return fd

def myClick(fd, cx, cy, click_num=1):  # 第四种，可后台
    #print("myclick")
    long_position = win32api.MAKELONG(int(cx), int(cy))  # 模拟鼠标指针 传送到指定坐标
    for _ in range(click_num):
        win32api.SendMessage(fd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
        win32api.SendMessage(fd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
        # 随机间隔0.1到0.5秒
        time.sleep(random.uniform(0.1, 0.2))


def drag_mouse(fd, start_pos, end_pos):
    # 将起始坐标转换为 LONG 值
    long_start_pos = win32api.MAKELONG(int(start_pos[0]), int(start_pos[1]))
    # 模拟鼠标左键按下
    win32api.SendMessage(fd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_start_pos)
    # 移动到起始位置
    #win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, 0, long_start_pos)
    time.sleep(1)  # 等待一段时间以保证起始位置被正确触发
    # 计算拖动路径
    steps = 20  # 设置拖动步数
    x_step = (end_pos[0] - start_pos[0]) / steps
    y_step = (end_pos[1] - start_pos[1]) / steps
    # 逐步移动鼠标
    for i in range(steps):
        x = start_pos[0] + x_step * (i + 1)
        y = start_pos[1] + y_step * (i + 1)
        long_pos = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_pos)
        time.sleep(0.05)  # 控制拖动速度
    # 将目标坐标转换为 LONG 值，模拟拖动到新位置
    long_end_pos = win32api.MAKELONG(int(end_pos[0]), int(end_pos[1]))
    win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_end_pos)
    # 模拟鼠标左键释放
    win32api.SendMessage(fd, win32con.WM_LBUTTONUP, 0, long_end_pos)

def click_button(fd, button, click_num=1):
    '''
    :param button:根据传入的功能在button里选择合适的click位置，具体做法是根据百分比，适应窗口大小
    :param click_num: 点击次数
    :return:
    '''
    # 获取窗口的矩形（左上角固定（0，0）和右下角的坐标）
    rect = win32gui.GetClientRect(fd)
    #计算点击位置
    click_pos = (rect[2] * button[0], rect[3] * button[1])
    # pyautogui.moveTo(true_pos, duration=2)
    #双击
    for _ in range(click_num):
        myClick(fd, click_pos[0], click_pos[1])
        # 随机间隔0.1到0.5秒
        time.sleep(random.uniform(0.1, 0.2))

def click_button_test(fd, button_name):
    #time.sleep(5)
    rect = win32gui.GetWindowRect(fd)
    print(rect)
    while(1):
        time.sleep(5)
        point = win32api.GetCursorPos()
        print("cur_point:", point)

# def myscreenshoot(fd):
#     '''
#     :return:
#     '''
#     # 创建应用程序对象
#     app = QApplication(sys.argv)
#     # 获取主屏幕对象
#     screen = QApplication.primaryScreen()
#     # 截取指定窗口的图像
#     img = screen.grabWindow(fd).toImage()
#     # 调整图像大小到1600x900
#     img = img.scaled(1600, 900)
#     # img = QScreen.grabWindow(fd)
#     # 保存截图为图像文件
#     # 构建保存路径
#     save_dir = "figs"
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#     save_path = os.path.join(save_dir, "screenshot.jpg")
#     img.save(save_path)

def myscreenshoot(fd, tmp_path="figs/screenshot.jpg"):
    '''
    截取后台窗口的截图，并保存到指定大小的图像文件
    可以最小化窗口
    '''
    # 获取窗口的设备上下文
    # 获取窗口设备上下文
    hwndDC = None
    # 创建一个兼容的设备上下文
    mfcDC = None
    saveDC = None
    try:
        # 获取窗口设备上下文
        hwndDC = win32gui.GetWindowDC(fd)
        # 创建一个兼容的设备上下文
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        left, top, right, bot = win32gui.GetWindowRect(fd)
        width = right - left
        height = bot - top

        # 创建一个位图对象
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # 使用 BitBlt 函数将窗口的内容复制到位图对象
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        # 保存位图到文件
        #tmp_path = "figs/screenshot.jpg"
        saveBitMap.SaveBitmapFile(saveDC, tmp_path)

        with Image.open(tmp_path) as img:
            #调整截图大小
            resized_img = img.resize((1600, 900), Image.LANCZOS)
            resized_img.save(tmp_path)
    finally:
        # 释放设备上下文和位图对象
        if hwndDC is not None:
            win32gui.ReleaseDC(fd, hwndDC)
        if saveDC is not None:
            saveDC.DeleteDC()
        # if mfcDC is not None:
        #     mfcDC.DeleteDC()
        if saveBitMap is not None:
            win32gui.DeleteObject(saveBitMap.GetHandle())

def reconnect(fd, Buttons):
    """
    :param fd:
    :return:
    """
    myscreenshoot(fd, "figs/reconnect_screenshot.jpg")
    image = cv2.imread('./figs/reconnect_screenshot.jpg', cv2.IMREAD_COLOR)
    template = cv2.imread('./figs/reconnect.png', cv2.IMREAD_COLOR)
    # 进行模板匹配
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 找到匹配度最高的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("断网匹配度：", max_val)
    # 设置匹配度阈值
    # 匹配2是0.87
    threshold = 0.88
    if max_val >= threshold:
        print("断网重连")
        time.sleep(1)
        click_button(fd, Buttons["reconnect"], 1)
        time.sleep(1)





