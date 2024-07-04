import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget

class ResizableImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_paths = ['art/bird_closed_mouth.png', 'art/bird_open_mouth.png']
        self.current_image_index = 0
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel()
        self.pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        
        layout.addWidget(self.label)
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(100, 100)
        self.resize(self.pixmap.width(), self.pixmap.height())

        # Set up a timer to switch images every 1000 ms (1 second)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.switch_image)
        self.timer.start(1000)

    def resizeEvent(self, event):
        self.label.setPixmap(self.pixmap.scaled(
            self.width(), self.height(), 
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        super().resizeEvent(event)

    def switch_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(self.pixmap.scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

app = QApplication(sys.argv)
window = ResizableImageWindow()
window.show()
sys.exit(app.exec_())