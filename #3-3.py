from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model


# Parameters for loading data and images
detection_model_path = 'C:/ABCDE/Jang/Emotion-recognition/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'C:/ABCDE/Jang/Emotion-recognition/models/_mini_XCEPTION.102-0.66.hdf5'

# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

class EmotionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Create QLabel for displaying camera feed
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)

        # Create QHBoxLayout for camera and emotion widgets
        camera_emotion_layout = QHBoxLayout()
        camera_emotion_layout.addWidget(self.camera_label)

        # Create frames for displaying emotion and probabilities
        self.emotion_frame = QFrame()
        self.emotion_frame.setFrameShape(QFrame.Box)
        self.emotion_frame.setLineWidth(2)

        self.probability_frame = QFrame()
        self.probability_frame.setFrameShape(QFrame.Box)
        self.probability_frame.setLineWidth(2)

        # Create labels for displaying emotion and probabilities
        self.emotion_label = QLabel()
        self.emotion_label.setAlignment(Qt.AlignCenter)
        self.probability_labels = []
        for _ in EMOTIONS:
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            self.probability_labels.append(label)

        # Set up the layout for the emotion frame
        emotion_layout = QHBoxLayout(self.emotion_frame)
        emotion_layout.setContentsMargins(0, 0, 0, 0)
        emotion_layout.addWidget(self.emotion_label)

        # Set up the layout for the probability frame
        probability_layout = QVBoxLayout(self.probability_frame)
        probability_layout.setContentsMargins(0, 0, 0, 0)
        for label in self.probability_labels:
            probability_layout.addWidget(label)

        # Add camera and emotion frames to the layout
        camera_emotion_layout.addWidget(self.emotion_frame)
        camera_emotion_layout.addWidget(self.probability_frame)

        # Add camera and emotion layout to the main layout
        self.main_layout.addLayout(camera_emotion_layout)

        # Set widget size
        self.setFixedSize(800, 500)

        # Initialize the video streaming
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 milliseconds

        # Initialize the emotion probabilities
        self.emotion_probabilities = [0.0] * len(EMOTIONS)



    def update_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            return

        frame = imutils.resize(frame, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

        canvas = np.zeros((300, 250, 3), dtype="uint8")
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
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]

            self.emotion_label.setText(label)

            for i, (emotion, prob) in enumerate(zip(EMOTIONS, preds)):
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                self.probability_labels[i].setText(text)

                # Update emotion probabilities
                self.emotion_probabilities[i] = prob

        self.display_frame(frame_clone, canvas)

    def display_frame(self, frame, canvas):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = channel * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.camera_label.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("메인 화면")
        self.setFixedSize(800, 500)

if __name__ == "__main__":
    app = QApplication([])
    emotion_widget = EmotionWidget()

    window = QMainWindow()
    window.setCentralWidget(emotion_widget)
    window.setWindowTitle("Emotion Recognition")
    window.show()

    app.exec()