# 星陨计划脚本

这是一个星陨计划脚本，实现挂机功能。



## 项目介绍

这是一个星陨计划脚本，实现挂机功能。完成的原因是上班没时间打游戏了。

使用OpenCV实现图像识别以及使用win32api模拟鼠标点击来实现游戏自动化。



## 项目结构

func.py：基础操作函数库，包括截图、鼠标点击、鼠标拖动、图像识别与比对等

shop.py：实现商店相关功能。

fight.py：实现战斗相关功能。

figs：图片库。



## 安装与使用

**请将模拟器调整成为1600*900**

直接下载，运行main.exe

**会自动尝试连接mumu模拟器。**

点击手动连接按钮后会在2s后判定鼠标所在的界面的fd，所以请在2s内将鼠标移动到游戏界面上等待连接。

添加任务后，点击开始任务按钮才会开始任务。

点击结束按钮后结束任务。

如果想增加/删除任务请重启脚本。



## 更新日志

### v1.0

实现了一个简单的脚本，实现了简单的连接、截图、点击功能。

### v1.1

优化了截图和按钮的操作。**无法最小化运行。**

### v1.2

实现了jjc、讨伐、收菜、商店功能。

商店会判断

### v1.3

实现了简单的前端。可以自己手动选择要挂机的功能。

实现了手动连接模拟器的功能。



## 问题

1. 无法最小化窗口截图，可以后台运行。
2. 触发点击时会自动跑最顶层运行。
3. 等比例放大缩小后的点击问题。



## 待实现/优化功能

1. 啥狗游戏网络不好容易断网。断网重连优化。
2. 购买物品可以手动选择。
3. 自动刷新商店功能。
4. 调教本
5. 扫荡增加自动吃体力
6. ....

