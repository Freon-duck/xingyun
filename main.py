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

import fight
import func
import shop

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox

class MyApp(QWidget):
    task_thread = None  # 声明一个类变量来存储任务处理线程对象
    stop_event = threading.Event()  # 事件对象用于停止线程

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Simple PyQt5 App')
        self.setGeometry(100, 100, 600, 600)  # (x, y, width, height)

        # 创建布局
        layout = QVBoxLayout()

        # 创建按钮并添加到布局中
        self.btn0 = QPushButton('手动连接模拟器', self)
        self.btn1 = QPushButton('讨伐', self)
        self.btn2 = QPushButton('jjc', self)
        self.btn3 = QPushButton('基地收菜', self)
        self.btn4 = QPushButton('商店够买', self)
        self.btn5 = QPushButton('一键添加', self)
        self.btn114 = QPushButton('启动任务处理', self)  # 重命名按钮为 "启动任务处理"
        self.btn514 = QPushButton('关闭程序', self)  # 新增按钮 "关闭程序"

        layout.addWidget(self.btn0)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn5)
        layout.addWidget(self.btn114)  # 添加 "启动任务处理" 按钮到布局中
        layout.addWidget(self.btn514)  # 添加 "关闭程序" 按钮到布局中

        # 将布局设置到窗口中
        self.setLayout(layout)

        # 连接按钮点击事件到相应的函数
        self.btn0.clicked.connect(self.connectMoniqi)
        self.btn1.clicked.connect(self.taofa)
        self.btn2.clicked.connect(self.jjc)
        self.btn3.clicked.connect(self.jidishoucai)
        self.btn4.clicked.connect(self.shop)
        self.btn5.clicked.connect(self.All)
        self.btn114.clicked.connect(self.start_task_processing)  # 连接 "启动任务处理" 按钮的点击事件
        self.btn514.clicked.connect(self.close_program)  # 连接 "关闭程序" 按钮的点击事件

    def connectMoniqi(self):
        print("连接模拟器中")
        global fd
        fd = func.get_WindowPoint_byhand()

    def taofa(self):
        num, ok = QInputDialog.getInt(self, 'Input Dialog', '输入讨伐Boss序号(1-5):')
        if num<1 | num>5:
            print("Boss序号不正确")
            return
        if ok:
            scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_taofa(fd, Buttons, num), "choose_taofa", 3600*5))
            print("添加讨伐任务成功")

    def jjc(self):
        scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_jjc(fd, Buttons), "choose_jjc", 3600))
        print("添加jjc任务成功")

    def jidishoucai(self):
        scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.jidishenchang(fd, Buttons), "jidishenchang", 3600 * 6))
        print("添加基地收菜任务成功")
    def shop(self):
        scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.buy_lvpiao(fd, Buttons), "buy_lvpiao", 3600))
        print("添加商店购买任务成功")

    def All(self):
        self.taofa()
        self.jjc()
        self.jidishoucai()
        self.shop()
        
    def start_task_processing(self):
        print("启动任务处理按钮点击")
        # 启动任务处理线程
        self.task_thread = threading.Thread(target=task_loop, args=(self.stop_event,))
        self.task_thread.daemon = True
        self.task_thread.start()
        # 启动调度器
        threading.Thread(target=scheduler.run).start()

    def close_program(self):
        print("关闭程序按钮点击")
        # 设置停止事件，让任务处理线程可以立即响应
        self.stop_event.set()
        scheduler.cancel_all()
        QApplication.quit()


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
    "duiwushezhi": (0.88125, 0.9),
    "kaishizhandou": (0.88125, 0.9),
    "repeatfight": (0.8318, 0.7511),
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

def task_loop(stop_event):
    time.sleep(3)
    while not stop_event.is_set():
        #print("进入循环")
        while not task_queue.empty():
            func.reconnect(fd, Buttons)
            task, task_name = task_queue.get()
            print(f"获取任务: {task_name}")
            task()  # 执行任务
            print(f"完成任务: {task_name}")
            task_queue.task_done()
        time.sleep(60)  # 等待一段时间再检查任务队列

# 任务添加函数
def task_add(scheduler, task, task_name, interval):
    task_queue.put([task, task_name])
    print(f"添加任务: {task_name}")
    # 重新调度任务添加
    scheduler.enter(interval, 1, task_add, (scheduler, task, task_name, interval))

# 初始化调度器
scheduler = sched.scheduler(time.time, time.sleep)

app = QApplication(sys.argv)
ex = MyApp()
ex.show()
sys.exit(app.exec_())

# 调度任务0，每隔6h执行一次
#scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.jidishenchang(fd, Buttons), "jidishenchang", 3600*6))
# 调度任务1，每隔3600秒执行一次
#scheduler.enter(0, 1, task_add, (scheduler, lambda: shop.buy_lvpiao(fd, Buttons), "buy_lvpiao", 3600))
# 调度任务2，每隔3600秒执行一次
#scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_jjc(fd, Buttons), "choose_jjc", 3600))
# 调度任务3，每隔5h秒执行一次
#scheduler.enter(0, 1, task_add, (scheduler, lambda: fight.choose_taofa(fd, Buttons, 2), "choose_taofa", 3600*5))


# # 启动任务处理线程
# task_thread = threading.Thread(target=task_loop)
# task_thread.daemon = True
# task_thread.start()
# # 启动调度器
# scheduler.run()





