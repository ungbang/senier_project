import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QButtonGroup

from PySide6.QtCore import Qt, QCoreApplication

app = QApplication([])

window = QMainWindow()
window.setFixedSize(800, 500)
window.show()
window.setWindowTitle("감정알림이")

main_widget = QWidget(window)
window.setCentralWidget(main_widget)

layout = QVBoxLayout()
layout.setSpacing(10)
main_widget.setLayout(layout)

title_label = QLabel("감정알림이")
title_label.setAlignment(Qt.AlignCenter)
font = title_label.font()
font.setPointSize(70)
title_label.setFont(font)
layout.addWidget(title_label)

button_layout = QVBoxLayout()
layout.addLayout(button_layout)

button_group = QButtonGroup()

def start_button_clicked():
    start_button.setParent(None)  # 시작 버튼 제거
    exit_button.setParent(None)  # 종료 버튼 제거
    
    checkbox_layout = QVBoxLayout()
    checkbox_layout.setAlignment(Qt.AlignCenter)
    checkbox_label = QLabel("사용자 정보 제공 동의")
    checkbox_layout.addWidget(checkbox_label)
    
    # 체크박스 대신 버튼을 추가합니다
    button1 = QPushButton("예")
    button2 = QPushButton("아니오")
    checkbox_layout.addWidget(button1, alignment=Qt.AlignCenter)
    checkbox_layout.addWidget(button2, alignment=Qt.AlignCenter)
    
    button_group.addButton(button1)
    button_group.addButton(button2)
    
    layout.addLayout(checkbox_layout)
    
    # 버튼 클릭 시 처리하는 함수를 연결합니다
    button_group.buttonClicked.connect(button_clicked)

def button_clicked(button):
    if button.text() == "예":
        subprocess.Popen(["python", "C:/Python/230518 senior project/Emotion-recognition-master/#2.py"])
    print("선택한 버튼:", button.text())
    QCoreApplication.quit()

def exit_button_clicked():
    print("프로그램을 종료합니다.")
    QCoreApplication.quit()


start_button = QPushButton("시작")
start_button.setFixedWidth(200)
start_button.setFixedHeight(50)
button_layout.addWidget(start_button, alignment=Qt.AlignCenter)
start_button.clicked.connect(start_button_clicked)

exit_button = QPushButton("종료")
exit_button.setFixedWidth(200)
exit_button.setFixedHeight(50)
button_layout.addWidget(exit_button, alignment=Qt.AlignCenter)
exit_button.clicked.connect(exit_button_clicked)


sys.exit(app.exec())
