import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QSizeGrip
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFileSystemWatcher

class ResizableImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_paths = ['art/bird_closed_mouth.png', 'art/bird_open_mouth.png']
        self.current_image_index = 0
        self.last_file_state = False
        self.initUI()
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Set up file watcher
        self.watcher = QFileSystemWatcher(self)
        self.watcher.addPath('beans_ear')
        self.watcher.fileChanged.connect(self.check_file)
        
        # Set up periodic timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_file)
        self.timer.start(100)  # Check every 100 ms
        
        # Initial check
        self.check_file()

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

    def read_beans_ear(self):
        try:
            with open('beans_ear', 'r') as file:
                return file.read().strip().lower() == 'true'
        except FileNotFoundError:
            print("File 'beans_ear' not found.")
            return False

    def check_file(self):
        new_state = self.read_beans_ear()
        if new_state != self.last_file_state:
            self.switch_image(new_state)
        self.last_file_state = new_state

    def switch_image(self, state):
        self.current_image_index = 1 if state else 0
        self.pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.label.setPixmap(self.pixmap.scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    def resizeEvent(self, event):
        self.label.setPixmap(self.pixmap.scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

def see_beans():
    app = QApplication(sys.argv)
    window = ResizableImageWindow()
    window.show()
    sys.exit(app.exec_())
