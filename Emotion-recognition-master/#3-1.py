from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QImage, QPixmap
import cv2
import numpy as np

class ProfileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(530, 75, 30, 140)

        # Information Box 1
        widget1 = QGroupBox("Id", self)
        widget1.setFixedHeight(70)
        main_layout.addWidget(widget1)

        layout1 = QVBoxLayout(widget1)
        layout1.setContentsMargins(10, 0, 0, 0)
        label = QLabel("사용자 아이디")
        layout1.addWidget(label)

        # Information Box 2
        widget2 = QGroupBox("감정 분석", self)
        widget2.setFixedHeight(230)
        main_layout.addWidget(widget2)

        layout2 = QVBoxLayout(widget2)
        layout2.setContentsMargins(10, 0, 0, 0)

        # Create a QLabel to display the video stream
        self.video_label = QLabel()
        layout2.addWidget(self.video_label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRect(55, 80, 450, 300)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)

        font = painter.font()
        font.setPointSize(23)
        painter.setFont(font)
        text_rect = QRect(55, 35, 450, 30)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, "감정분석")

    def display_frame(self, frame):
        # Convert the OpenCV frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # Display the QImage in the QLabel
        self.video_label.setPixmap(QPixmap.fromImage(q_image))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("메인 화면")
        self.setFixedSize(800, 500)

        self.profile_widget = ProfileWidget()
        self.setCentralWidget(self.profile_widget)

        # Initialize the OpenCV camera
        self.camera = cv2.VideoCapture(0)

        # Start the video stream
        self.start_video_stream()

    def start_video_stream(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)  # Flip horizontally for mirror effect

            # Resize the frame to fit the QLabel
            frame = cv2.resize(frame, (450, 300))

            # Display the frame in the ProfileWidget
            self.profile_widget.display_frame(frame)

        # Call this method again after a delay (e.g., 30 milliseconds)
        # to continuously update the video stream
        QTimer.singleShot(30, self.start_video_stream)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()