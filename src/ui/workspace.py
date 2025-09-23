from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from .workspace_panel import WorkspacePanel
from .web_browser import WebBrowser
from ..core.theme_manager import _THEME


class Workspace(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем разделитель
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.apply_splitter_theme(splitter)
        
        # Левая панель
        self.left_panel = WorkspacePanel("Левая панель")
        
        # Правая панель с веб-браузером
        self.right_panel = WebBrowser()
        
        # Добавляем панели в разделитель
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.right_panel)
        
        # Устанавливаем равные размеры (50/50)
        splitter.setSizes([1, 1])
        
        layout.addWidget(splitter)
    
    def apply_splitter_theme(self, splitter):
        """Применяет тему к разделителю"""
        colors = _THEME.get_all_colors("splitter")
        
        splitter_style = f"""
            QSplitter::handle {{
                background-color: {colors.get('handle', '#ddd')};
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {colors.get('handle_hover', '#007ACC')};
            }}
        """
        splitter.setStyleSheet(splitter_style)
    
    def get_web_browser(self):
        """Возвращает ссылку на веб-браузер"""
        return self.right_panel
    
    def get_left_panel(self):
        """Возвращает ссылку на левую панель"""
        return self.left_panel
