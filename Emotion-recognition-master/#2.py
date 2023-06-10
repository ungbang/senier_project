import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, QProcess

class OptionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("옵션")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        button_layout.addStretch()

        next_button1 = QToolButton()
        next_button1.setText("표정 분석")
        next_button1.setIcon(QIcon("C:/Python/230518 senior project/icon.jpg"))
        next_button1.setIconSize(QSize(150, 150))
        next_button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        next_button1.setStyleSheet("QToolButton {"
                                   "border: 2px solid #8f8f91;"
                                   "border-radius: 20px;"
                                   "background-color: #f6f6f6;"
                                   "color: #333333;"
                                   "font-size: 20px;"
                                   "padding: 120px 70px;"
                                   "}"
                                   "QToolButton:hover {"
                                   "background-color: #c0c0c0;"
                                   "color: #ffffff;"
                                   "}")

        button_layout.addWidget(next_button1)

        next_button2 = QToolButton()
        next_button2.setText("표정 연습")
        next_button2.setIcon(QIcon("C:/Python/230518 senior project/icon.jpg"))
        next_button2.setIconSize(QSize(150, 150))
        next_button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        next_button2.setStyleSheet("QToolButton {"
                                   "border: 2px solid #8f8f91;"
                                   "border-radius: 20px;"
                                   "background-color: #f6f6f6;"
                                   "color: #333333;"
                                   "font-size: 20px;"
                                   "padding: 120px 70px;"
                                   "}"
                                   "QToolButton:hover {"
                                   "background-color: #c0c0c0;"
                                   "color: #ffffff;"
                                   "}")

        button_layout.addWidget(next_button2)

        button_layout.addStretch()

        # 버튼 클릭 이벤트 처리
        next_button1.clicked.connect(self.go_to_emotion_analysis)
        next_button2.clicked.connect(self.go_to_expression_practice)

    def go_to_emotion_analysis(self):
        self.execute_external_program("C:/Python/230518 senior project/#3-1.py")

    def go_to_expression_practice(self):
        self.execute_external_program("C:/Python/230518 senior project/#3-2.py")

    def execute_external_program(self, program_path):
        process = QProcess()
        process.startDetached("python", [program_path])
        process.waitForFinished()

app = QApplication([])

window = OptionsWindow()
window.setFixedSize(800, 500)
window.show()

sys.exit(app.exec())
