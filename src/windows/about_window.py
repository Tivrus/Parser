from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .base_window import BaseWindow


class AboutWindow(BaseWindow):
    
    def __init__(self, parent=None, width=480, height=560):
        super().__init__(parent, "О приложении", width, height)
    
    def create_content(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
           
        info_text = QLabel("""
        <p><b>Parser Bot 1.0</b></p>
        <p>Версия: 1.0.0</p>
        <p>Разработчик: _tivrus</p>
        <p>Лицензия: MIT</p>
        """)
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        return content
