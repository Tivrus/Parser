"""
Базовое окно приложения
"""
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt


class BaseWindow(QMainWindow):
    """Базовый класс для всех окон приложения"""
    
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
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
