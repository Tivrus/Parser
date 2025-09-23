from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent


class BaseWindow(QMainWindow):
    
    def __init__(self, parent=None, title="", width=400, height=300):
        """
        Инициализация базового окна
        
        Args:
            parent: Родительское окно
            title: Заголовок окна
            width: Ширина окна
            height: Высота окна
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.setWindowFlags(Qt.WindowType.Window)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        content = self.create_content()
        if content:
            main_layout.addWidget(content)
    
    def create_content(self):
        return None
