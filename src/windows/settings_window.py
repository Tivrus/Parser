"""
Окно настроек
"""
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from .base_window import BaseWindow


class SettingsWindow(BaseWindow):
    """Окно настроек приложения"""
    
    def __init__(self, parent=None, width=600, height=500):
        """Инициализация окна настроек"""
        super().__init__(parent, "Настройки приложения", width, height)
    
    def create_content(self):
        """Создает содержимое окна настроек"""
        content = super().create_content()
        layout = QVBoxLayout(content)
        
        
        layout.addStretch()
        return content
