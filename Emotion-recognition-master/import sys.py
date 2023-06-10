import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QCheckBox, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QSpacerItem, QSizePolicy


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
        next_button1.setIcon(QIcon("icon.jpg"))  # 이미지 파일 경로를 지정해야 합니다.
        next_button1.setIconSize(QSize(150, 150))  # 아이콘의 크기를 조정할 수 있습니다.
        next_button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        next_button1.setStyleSheet("QToolButton {"
                                   "border: 2px solid #8f8f91;"
                                   "border-radius: 20px;"
                                   "background-color: #f6f6f6;"
                                   "color: #333333;"
                                   "font-size: 25px;"
                                   "padding: 120px 70px;"
                                   "}"
                                   "QToolButton:hover {"
                                   "background-color: #c0c0c0;"
                                   "color: #ffffff;"
                                   "}")

        button_layout.addWidget(next_button1)

        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer_item)

        next_button2 = QToolButton()
        next_button2.setText("표정 연습")
        next_button2.setIcon(QIcon("icon.jpg"))  # 이미지 파일 경로를 지정해야 합니다.
        next_button2.setIconSize(QSize(150, 150))  # 아이콘의 크기를 조정할 수 있습니다.
        next_button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        next_button2.setStyleSheet("QToolButton {"
                                   "border: 2px solid #8f8f91;"
                                   "border-radius: 20px;"
                                   "background-color: #f6f6f6;"
                                   "color: #333333;"
                                   "font-size: 25px;"
                                   "padding: 120px 70px;"
                                   "}"
                                   "QToolButton:hover {"
                                   "background-color: #c0c0c0;"
                                   "color: #ffffff;"
                                   "}")

        button_layout.addWidget(next_button2)

        button_layout.addStretch()

        # 버튼 클릭 이벤트 처리
        next_button1.clicked.connect(self.go_to_next_screen)
        next_button2.clicked.connect(self.go_to_next_screen)

    def go_to_next_screen(self):
        # 다음 화면으로 이동하는 로직을 구현하세요.
        print("다음 화면으로 이동")

app = QApplication([])

window = OptionsWindow()
window.setFixedSize(800, 500)  # 창 크기 고정
window.show()

sys.exit(app.exec())