"""
Базовое окно приложения
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
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
        
        # Создаем основной макет
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Создаем контент (переопределяется в наследниках)
        content = self.create_content()
        if content:
            main_layout.addWidget(content)
    
    def create_content(self):
        """
        Создает содержимое окна.
        Переопределяется в наследниках.
        
        Returns:
            QWidget с содержимым окна или None
        """
        return None
