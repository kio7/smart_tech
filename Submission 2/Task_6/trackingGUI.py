import cv2
import sys
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import QTimer  # Import QTimer from PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QInputDialog
from PyQt5.QtGui import QImage, QPixmap

class TrackingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.tracker_type = ""
        self.capture = None
        self.tracker = None
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Object Tracking App')
        self.setGeometry(100, 100, 800, 600)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)

        self.select_button = QPushButton('Select Video', self)
        self.select_button.clicked.connect(self.openVideo)

        self.start_button = QPushButton('Start Tracking', self)
        self.start_button.clicked.connect(self.startTracking)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)


    def openVideo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '', 'Video Files (*.mp4 *.avi);;All Files (*)', options=options)

        if video_path:
            self.capture = cv2.VideoCapture(video_path)

    def startTracking(self):
        if self.capture is None:
            return

        self.tracker_type, ok = QInputDialog.getItem(self, 'Select Tracker Type', 'Choose Tracker Type:', ['1. MIL', '2. KCF', '3. CSRT'])
        if ok:
            if self.tracker_type == '1. MIL':
                self.tracker = cv2.TrackerMIL_create()
            elif self.tracker_type == '2. KCF':
                self.tracker = cv2.TrackerKCF_create()
            elif self.tracker_type == '3. CSRT':
                self.tracker = cv2.TrackerCSRT_create()
            else:
                print("Invalid choice")
                return

            ret, frame = self.capture.read()
            bbox = cv2.selectROI("Select Object to Track", frame)
            self.tracker.init(frame, bbox)

            self.timer.timeout.connect(self.trackObject)
            self.timer.start(30)  # Update every 30 milliseconds

    def trackObject(self):
        ret, frame = self.capture.read()
        if not ret:
            self.timer.stop()
            return

        success, bbox = self.tracker.update(frame)

        if success:
            (x, y, w, h) = tuple(map(int, bbox))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert the OpenCV image to a QImage for displaying in the GUI
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        self.video_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trackingApp = TrackingApp()
    trackingApp.show()
    sys.exit(app.exec_())
