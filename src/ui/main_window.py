"""
Главное окно приложения
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from ..core.theme_manager import _THEME
from ..core.window_router import WindowRouter
from ..core.title_manager import _TITLE_MANAGER
from ..core.text_manager import get_text, set_language, get_current_language
from .menu_system import MenuSystem


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализируем компоненты
        self.menu_system = MenuSystem(self, language="ru")
        self.window_router = WindowRouter()
        
        # Устанавливаем TitleManager
        _TITLE_MANAGER.set_main_window(self)
        _TITLE_MANAGER.new_project()  # Создаем новый проект по умолчанию
        
        self.setup_ui()
        self.apply_theme()
        
        # Разворачиваем окно на весь экран
        self.showMaximized()
    
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Create language toggle button
        self.create_language_toggle(layout)
        
        # Add your main content here
        content_label = QLabel("Основная рабочая область")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setStyleSheet("font-size: 16px; color: #666666;")
        layout.addWidget(content_label)
        
        # Add stretch to push content to top
        layout.addStretch()
    
    def create_language_toggle(self, parent_layout):
        """Создает кнопку переключения языка"""
        # Create horizontal layout for language toggle
        lang_layout = QHBoxLayout()
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Create language toggle button
        self.language_button = QPushButton()
        self.language_button.setFixedSize(100, 35)
        self.language_button.clicked.connect(self.toggle_language)
        
        # Set initial language
        self.update_language_button()
        
        # Style the button
        self.language_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        
        lang_layout.addWidget(self.language_button)
        parent_layout.addLayout(lang_layout)
    
    def toggle_language(self):
        """Переключает язык интерфейса"""
        current_lang = get_current_language()
        new_lang = "en" if current_lang == "ru" else "ru"
        
        # Set new language
        set_language(new_lang)
        
        # Update language button text
        self.update_language_button()
        
        # Update menu system language
        self.menu_system.language = new_lang
        self.menu_system._load_configurations()
        
        # Refresh menus to apply new language
        self.refresh_menus()
    
    def update_language_button(self):
        """Обновляет текст кнопки языка"""
        current_lang = get_current_language()
        if current_lang == "ru":
            self.language_button.setText(get_text("button_language_en"))
        else:
            self.language_button.setText(get_text("button_language_ru"))
    
    def refresh_menus(self):
        """Обновляет меню для применения нового языка"""
        # Clear existing menu bar
        menubar = self.menuBar()
        menubar.clear()
        
        # Recreate menus with new language
        self.menu_system.create_menus(menubar)
    
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
