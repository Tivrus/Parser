"""
Окно документации
"""
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTextEdit
from .base_window import BaseWindow


class DocumentationWindow(BaseWindow):
    """Окно документации приложения"""
    
    def __init__(self, parent=None, width=700, height=600):
        """Инициализация окна документации"""
        super().__init__(parent, "Документация", width, height)
    
    def create_content(self):
        """Создает содержимое окна документации"""
        content = super().create_content()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Add documentation content
        title_label = QLabel("Документация")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title_label)
        
        text_area = QTextEdit()
        text_area.setPlainText("Здесь будет размещена документация по использованию приложения...")
        text_area.setReadOnly(True)
        layout.addWidget(text_area)
        
        return content
