import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
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


def start_button_clicked():
    subprocess.Popen(["python", "#2.py"])


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
