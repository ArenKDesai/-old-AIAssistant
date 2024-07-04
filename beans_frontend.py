import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
image_paths = []

class ResizableImageWindow(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = ['art/bird_closed_mouth.png', 'art/bird_open_mouth.png']
        self.current_image_index = 0
        self.image_paths = image_paths
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

def HelloBeans(image_paths):
    app = QApplication(sys.argv)
    window = ResizableImageWindow(image_paths)
    window.show()

image_thread = threading.Thread(target=HelloBeans, args=(image_paths,))
image_thread.start()

# sys.exit(app.exec_())
