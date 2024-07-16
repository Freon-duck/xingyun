import os
import random
import sched
import sys
import threading
from queue import Queue
import pyautogui
import time
import win32gui
import win32con
import win32api
import psutil
import win32process
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication

import fight
import func
import shop

#字典，用于记录一系列按钮的相对于窗口的百分比位置
Buttons = {
    "center": (0.5, 0.5),
    "return": (0.08, 0.05555),
    "returndating": (0.17, 0.05555),
    "reconnect": (0.625, 0.5555),
    #主页
    "fight_button": (0.89411, 0.88751),
    "house_button": (0.89625, 0.79444),
    "shop_button": (0.08125, 0.8744),
    "jidi_button":(0.6987, 0.8633),
    #冒险主页
    "yuansu": (),
    "xulie": (),
    "jjc": (0.5, 0.9),
    "taofa": (0.8687, 0.9),
    #战斗
    ##讨伐
    "taofa_boss1": (0.76375, 0.23333),
    "taofa_boss2": (0.76375, 0.58),
    "taofa_boss3": (0.76375, 0.91111),
    "duiwushezhi": (),
    "kaishizhandou": (0.88125, 0.9),
    "autofight_button1": (0.9356, 0.1744),
    "autofight_button2": (0.6243, 0.57),
    "autofight_button3": (),
    ##jjc
    "NPCfight":(0.85625, 0.45444),
    "tiaozhan":(0.72125, -1),
    "jieshu":(0.88125, 0.9),
    #商店购买
    "shenmishangdian": (0.9056, 0.7055), #神秘商店栏目
    "shenmi_buy": (0.7411, 0),  #184000按钮
    "queren_buy": (0.5956, 0.6811),
    "quxiao_buy": (0.3981, 0.6811),#用不上
    #基地收菜
    "donglizhuanghuang":(0.5, 0.55),
    "lingqu":(0.88125, 0.9),
}

global fd
# 获取窗口句柄（假设 func.get_WindowPoint() 可以返回正确的句柄）
fd = func.get_WindowPoint()

# def myClick(cx, cy):  # 第四种，可后台
#     long_position = win32api.MAKELONG(int(cx), int(cy))  # 模拟鼠标指针 传送到指定坐标
#     win32api.SendMessage(fd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
#     win32api.SendMessage(fd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
#
# def drag_mouse(start_pos, end_pos):
#     # 将起始坐标转换为 LONG 值
#     long_start_pos = win32api.MAKELONG(int(start_pos[0]), int(start_pos[1]))
#     # 模拟鼠标左键按下
#     win32api.SendMessage(fd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_start_pos)
#     # 移动到起始位置
#     #win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, 0, long_start_pos)
#     time.sleep(1)  # 等待一段时间以保证起始位置被正确触发
#     # 计算拖动路径
#     steps = 20  # 设置拖动步数
#     x_step = (end_pos[0] - start_pos[0]) / steps
#     y_step = (end_pos[1] - start_pos[1]) / steps
#     # 逐步移动鼠标
#     for i in range(steps):
#         x = start_pos[0] + x_step * (i + 1)
#         y = start_pos[1] + y_step * (i + 1)
#         long_pos = win32api.MAKELONG(int(x), int(y))
#         win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_pos)
#         time.sleep(0.05)  # 控制拖动速度
#     # 将目标坐标转换为 LONG 值，模拟拖动到新位置
#     long_end_pos = win32api.MAKELONG(int(end_pos[0]), int(end_pos[1]))
#     win32api.SendMessage(fd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_end_pos)
#     # 模拟鼠标左键释放
#     win32api.SendMessage(fd, win32con.WM_LBUTTONUP, 0, long_end_pos)
#
# def click_button(button, click_num=1):
#     '''
#     :param buttons:按钮大全
#     :param button:根据传入的功能在button里选择合适的click位置，具体做法是根据百分比，适应窗口大小
#     :param click_num: 点击次数
#     :return:
#     '''
#     # 获取窗口的矩形（左上角和右下角的坐标）
#     rect = win32gui.GetClientRect(fd)
#     #计算点击位置
#     pos = Buttons[button]
#     click_pos = (rect[2] * pos[0], rect[3] * pos[1])
#     # pyautogui.moveTo(true_pos, duration=2)
#     #双击
#     for _ in range(click_num):
#         myClick(click_pos[0], click_pos[1])
#         # 随机间隔0.1到0.5秒
#         time.sleep(random.uniform(0.1, 0.2))
#
# def click_button_test(button_name):
#     #time.sleep(5)
#     rect = win32gui.GetWindowRect(fd)
#     print(rect)
#     while(1):
#         time.sleep(5)
#         point = win32api.GetCursorPos()
#         print("cur_point:", point)
#


# 定义任务队列
task_queue = Queue()

# 任务处理循环
def task_loop():
    time.sleep(3)
    while True:
        #print("进入循环")
        while not task_queue.empty():
            func.reconnect(fd, Buttons)
            task, task_name = task_queue.get()
            print(f"获取任务: {task_name}")
            task()  # 执行任务
            print(f"完成任务: {task_name}")
            task_queue.task_done()
        time.sleep(60)  # 等待一段时间再检查任务队列

#测试点位，补充Buttons
#func.click_button_test(fd,"autofight_button1")

#func.click_button(fd, "shenmishangdian")
#time.sleep(1)
#shop.buy_lvpiao(fd, Buttons)
#time.sleep(2)
#fight.choose_taofa(fd, Buttons, 5)
#func.myscreenshoot(fd)
# while True:
#     time.sleep(1)

# 任务添加函数
def task_add(scheduler, task, task_name, interval):
    task_queue.put([task, task_name])
    print(f"添加任务: {task_name}")
    # 重新调度任务添加
    scheduler.enter(interval, 1, task_add, (scheduler, task, task_name, interval))

# 初始化调度器
scheduler = sched.scheduler(time.time, time.sleep)

# 调度任务0，每隔6h执行一次
scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.jidishenchang(fd, Buttons), "jidishenchang", 3600*6))
# 调度任务1，每隔3600秒执行一次
scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.buy_lvpiao(fd, Buttons), "buy_lvpiao", 3600))
# 调度任务2，每隔3600秒执行一次
scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_jjc(fd, Buttons), "choose_jjc", 3600))
# 调度任务3，每隔5h秒执行一次
scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_taofa(fd, Buttons, 2), "choose_taofa", 3600*5))

# 启动任务处理线程
task_thread = threading.Thread(target=task_loop)
task_thread.daemon = True
task_thread.start()

# 启动调度器
scheduler.run()
print("bp2")

# 启动任务处理线程
# print("bp0")
# task_thread = threading.Thread(target=task_loop)
# task_thread.daemon = True
# task_thread.start()
#
# #主线程睡眠
# while True:
#     time.sleep(1)
# # 等待所有任务完成
# task_queue.join()  # 阻塞，直到所有任务都标记为完成




