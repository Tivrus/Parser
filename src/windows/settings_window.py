"""
Окно настроек
"""
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from .base_window import BaseWindow


class SettingsWindow(BaseWindow):
    """Окно настроек приложения"""
    
    def __init__(self, parent=None, width=600, height=500):
        """Инициализация окна настроек"""
        super().__init__(parent, "Настройки", width, height)
    
    def create_content(self):
        """Создает содержимое окна настроек"""
        content = super().create_content()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Add some sample content
        title_label = QLabel("Настройки приложения")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title_label)
        
        # Add some sample settings
        for i in range(3):
            setting_layout = QHBoxLayout()
            label = QLabel(f"Настройка {i+1}:")
            label.setMinimumWidth(150)
            checkbox = QCheckBox(f"Включить настройку {i+1}")
            setting_layout.addWidget(label)
            setting_layout.addWidget(checkbox)
            setting_layout.addStretch()
            layout.addLayout(setting_layout)
        
        layout.addStretch()
        return content
