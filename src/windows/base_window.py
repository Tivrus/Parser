"""
Базовое окно приложения
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from ..core.theme_manager import _THEME


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
        
        # Apply theme
        self.apply_theme()
        self.setup_ui()
    
    def apply_theme(self):
        """Применяет тему к окну"""
        colors = _THEME.get_all_colors("dialog")
        main_colors = _THEME.get_all_colors("main_window")
        bg_color = colors.get("background", main_colors.get("background", "#FFFFFF"))
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg_color};
                border: 1px solid {colors.get('border', '#CCCCCC')};
            }}
        """)
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with proper margins
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        # Create container for header and content
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("""
            QWidget#container {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                background-color: transparent;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Header
        header = self.create_header()
        container_layout.addWidget(header)

        # Content
        content = self.create_content()
        container_layout.addWidget(content)
        
        main_layout.addWidget(container)
    
    def create_header(self):
        """Создает заголовок окна"""
        header_widget = QWidget()
        header_widget.setObjectName("header")
        colors = _THEME.get_all_colors("dialog")
        main_colors = _THEME.get_all_colors("main_window")
        text_color = colors.get("text", main_colors.get("text", "#000000"))
        bg_color = colors.get("background", main_colors.get("background", "#FFFFFF"))
        
        header_widget.setStyleSheet(f"""
            QWidget#header {{
                background-color: {bg_color};
                border-bottom: 1px solid {colors.get('border', '#CCCCCC')};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 12, 12, 12)
        header_layout.setSpacing(8)
        
        title_label = QLabel(self.windowTitle())
        title_label.setStyleSheet(f"color: {text_color}; font-weight: bold; font-size: 14px;")
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        header_layout.addWidget(title_label)
        
        return header_widget
    
    def create_content(self):
        """Создает содержимое окна"""
        content_widget = QWidget()
        content_widget.setObjectName("content")
        
        colors = _THEME.get_all_colors("dialog")
        main_colors = _THEME.get_all_colors("main_window")
        bg_color = colors.get("background", main_colors.get("background", "#FFFFFF"))
        
        content_widget.setStyleSheet(f"""
            QWidget#content {{
                background-color: {bg_color};
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
        """)
        
        return content_widget
