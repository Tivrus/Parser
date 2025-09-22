"""
Окно "О программе"
"""
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from .base_window import BaseWindow


class AboutWindow(BaseWindow):
    """Окно информации о программе"""
    
    def __init__(self, parent=None, width=480, height=560):
        """Инициализация окна "О программе" """
        super().__init__(parent, "О приложении", width, height)
    
    def create_content(self):
        content = super().create_content()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
           
        info_text = QLabel("""
        <p><b>Parser Bot 1.0</b></p>
        <p>Версия: 1.0.0</p>
        <p>Разработчик: Ваше имя</p>
        <p>Описание: Мощный инструмент для парсинга данных</p>
        <p>Лицензия: MIT</p>
        """)
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return content
