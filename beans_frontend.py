import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import QSize

class ResizableImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_paths = ['art/bird_closed_mouth.png', 'art/bird_open_mouth.png']
        self.current_image_index = 0
        self.initUI()
        self.setWindowFlags(Qt.FramelessWindowHint)

    # def initUI(self):
    #     self.central_widget = QWidget()
    #     self.setCentralWidget(self.central_widget)
        
    #     layout = QVBoxLayout(self.central_widget)
        
    #     self.label = QLabel()
    #     self.pixmap = QPixmap(self.image_paths[self.current_image_index])
    #     self.label.setPixmap(self.pixmap)
    #     self.label.setScaledContents(True)
        
    #     layout.addWidget(self.label)
        
    #     self.setAttribute(Qt.WA_TranslucentBackground, True)
    #     self.setMinimumSize(100, 100)
    #     self.resize(self.pixmap.width(), self.pixmap.height())

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove layout margins

        self.label = QLabel()
        self.pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        layout.addWidget(self.label)

        # Add size grip for resizing
        size_grip = QSizeGrip(self)
        layout.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

app = QApplication(sys.argv)
window = ResizableImageWindow()
window.show()
sys.exit(app.exec_())