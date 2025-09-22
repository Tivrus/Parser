"""
Главное окно приложения
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ..core.theme_manager import _THEME
from ..core.window_router import WindowRouter
from .menu_system import MenuSystem


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.setWindowTitle("Parser Bot 1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализируем компоненты
        self.menu_system = MenuSystem(self, language="ru")
        self.window_router = WindowRouter()
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Create menu bar
        menubar = self.menuBar()
        self.menu_system.create_menus(menubar)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add your main content here
        content_label = QLabel("Основная рабочая область")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content_label)
    
    def apply_theme(self):
        """Применяет тему к главному окну"""
        # Apply main window theme
        colors = _THEME.get_all_colors("main_window")
        bg_color = colors.get("background", "#FFFFFF")
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QWidget {{
                background-color: {bg_color};
                color: {colors.get('text', '#000000')};
            }}
        """)
        
        # Update menu colors
        self.menu_system._update_menu_colors()
