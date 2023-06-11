import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QGroupBox, QLineEdit
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QImage, QPixmap, QColor, QFont
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model

# Parameters for loading data and images
detection_model_path = 'C:/Python/230518 senior project/Emotion-recognition-master/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'C:/Python/230518 senior project/Emotion-recognition-master/models/_mini_XCEPTION.102-0.66.hdf5'

# Loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

class ProfileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 메인 수직 레이아웃 생성
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # ID 상자
        id_layout = QHBoxLayout()
        id_label = QLabel("ID: ")
        self.id_edit = QLineEdit()
        self.id_edit.returnPressed.connect(self.save_id)
        self.id_display = QLabel()  # ID를 표시할 QLabel
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_edit)
        id_layout.addWidget(self.id_display)
        main_layout.addLayout(id_layout)

    @Slot()
    def save_id(self):
        id_text = self.id_edit.text()
        print(f"ID 저장됨: {id_text}")
        self.id_display.setText(id_text)  # ID를 표시할 QLabel로 설정

        # ID를 저장하는 추가적인 로직을 여기에 수행할 수 있습니다.

        # ID 입력 위젯 삭제
        self.id_edit.hide()
        self.id_display.show()

class EmotionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create camera label
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("border: 1px solid grey;")

        # Create emotion group box
        self.emotion_group_box = QGroupBox("감정")
        self.emotion_group_layout = QVBoxLayout(self.emotion_group_box)
        self.emotion_label = QLabel("")
        self.emotion_label.setAlignment(Qt.AlignCenter)
        self.emotion_label.setStyleSheet("color: black; font-size: 55px;")
        self.emotion_group_layout.addWidget(self.emotion_label)

        # Create top left label
        self.top_left_label = QLabel("감정 연습")
        self.top_left_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.top_left_label.setStyleSheet("color: black; font-size: 45px; margin-top: 25px; margin-left: 20px; " )


        # Add widgets to the main layout
        self.main_layout.addWidget(self.camera_label, 1, 0)
        self.main_layout.addWidget(self.top_left_label, 0, 0, Qt.AlignTop | Qt.AlignLeft)
        self.main_layout.addWidget(self.emotion_group_box, 0, 1)  # 감정 그룹 박스 추가

        # Initialize video streaming
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            return

        frame = imutils.resize(frame, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

        canvas = np.zeros((250, 300, 3), dtype="uint8")
        frame_clone = frame.copy()
        if len(faces) > 0:
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces

            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            label = EMOTIONS[preds.argmax()]

            self.emotion_label.setText(label)

        self.display_frame(frame, canvas)

    def display_frame(self, frame, canvas):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, channel = frame.shape
        bytes_per_line = channel * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.camera_label.setPixmap(pixmap.scaled(500, 380, Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.camera.release()
        
if __name__ == "__main__":
    app = QApplication([])
    emotion_widget = EmotionWidget()
    profile_widget = ProfileWidget()

    # 메인 수직 레이아웃 생성
    main_layout = QVBoxLayout()
    main_layout.addWidget(profile_widget)
    main_layout.addWidget(emotion_widget)

    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    main_widget.show()

    sys.exit(app.exec_())
