import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Simple PyQt5 App')
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

        # 创建布局
        layout = QVBoxLayout()

        # 创建按钮并添加到布局中
        self.btn1 = QPushButton('Button 1', self)
        self.btn2 = QPushButton('Button 2', self)
        self.btn3 = QPushButton('Button 3', self)
        self.btn4 = QPushButton('Button 4', self)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)

        # 将布局设置到窗口中
        self.setLayout(layout)

        # 连接按钮点击事件到相应的函数
        self.btn1.clicked.connect(self.prompt_input)
        self.btn2.clicked.connect(self.func2)
        self.btn3.clicked.connect(self.func3)
        self.btn4.clicked.connect(self.func4)

    def prompt_input(self):
        num, ok = QInputDialog.getInt(self, 'Input Dialog', 'Enter a number:')
        if ok:
            self.func1(num)

    def func1(self, num):
        print(f"func1: {num}")

    def func2(self):
        print("func2")

    def func3(self):
        print("func3")

    def func4(self):
        print("func4")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
    print("aaa")