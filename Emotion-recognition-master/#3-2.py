from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QFont, QImage, QPixmap
from tensorflow.keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import sys


class ProfileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Info Box 1
        widget1 = QGroupBox("Emotion", self)
        widget1.setFixedHeight(70)
        main_layout.addWidget(widget1)

        # Content of Box 1
        layout1 = QVBoxLayout(widget1)
        layout1.setContentsMargins(10, 0, 0, 0)
        self.emotion_label = QLabel("Current Emotion")
        layout1.addWidget(self.emotion_label)

        # Create a horizontal layout for camera display and emotion graph
        layout2 = QHBoxLayout()
        main_layout.addLayout(layout2)

        # Camera display
        self.camera_label = QLabel()
        layout2.addWidget(self.camera_label)

        # Info Box 2
        widget2 = QGroupBox("Emotion Analysis", self)
        widget2.setFixedHeight(230)
        layout2.addWidget(widget2)

        # Content of Box 2
        layout3 = QVBoxLayout(widget2)
        layout3.setContentsMargins(10, 0, 0, 0)
        self.emotion_graph = QLabel()
        layout3.addWidget(self.emotion_graph)

        self.emotion_label.setText("Current Emotion")

    def update_emotion_result(self, emotion, preds):
        self.emotion_label.setText(f"현재 감정: {emotion}")
        self.update_emotion_graph(preds)

    def update_emotion_graph(self, preds):
        # Implement the logic to update the emotion graph here
        pass

    def convert_frame_to_pixmap(self, frame):
        # Convert OpenCV frame to QPixmap
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)


# Parameters for loading data and images
detection_model_path = 'C:/Python/230518 senior project/Emotion-recognition-master/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'C:/Python/230518 senior project/Emotion-recognition-master/models/_mini_XCEPTION.102-0.66.hdf5'

# Hyperparameters for bounding boxes shape
# Load models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setFixedSize(900, 500)

        profile_widget = ProfileWidget()
        self.setCentralWidget(profile_widget)

    def process_frame(self, frame):
        if frame is not None:
            frame = imutils.resize(frame, width=300)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)

            if len(faces) > 0:
                faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))
                (fX, fY, fW, fH) = faces[0]

                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                preds = emotion_classifier.predict(roi)[0]
                emotion_probability = np.max(preds)
                label = EMOTIONS[preds.argmax()]

                # Display emotion analysis result on the screen
                profile_widget = self.centralWidget()
                profile_widget.update_emotion_result(label, preds)

        if len(faces) > 0:
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces

            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]

            # Display emotion analysis result on the screen
            profile_widget = self.centralWidget()
            profile_widget.update_emotion_result(label, preds)

    def start_webcam(self):
        camera = cv2.VideoCapture(0)
        while True:
            ret, frame = camera.read()
            if ret:
                self.process_frame(frame)
                q_frame = self.convert_frame_to_pixmap(frame)
                self.centralWidget().camera_label.setPixmap(q_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        camera.release()

    def convert_frame_to_pixmap(self, frame):
        # Convert OpenCV frame to QPixmap
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)


app = QApplication([])
window = MainWindow()
window.show()
window.start_webcam()
sys.exit(app.exec())