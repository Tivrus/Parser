from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from ..core.theme_manager import _THEME
from ..core.window_router import WindowRouter
from ..core.title_manager import _TITLE_MANAGER
from ..core.text_manager import get_text, set_language, get_current_language
from ..core.app_settings_manager import _APP_SETTINGS
from .menu_system import MenuSystem


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1200, 800)
        
        # Загружаем настройки приложения
        self._load_app_settings()
        
        # Инициализируем компоненты с настройками
        language = _APP_SETTINGS.get_setting("language", "ru")
        self.menu_system = MenuSystem(self, language=language)
        self.window_router = WindowRouter()
        
        _TITLE_MANAGER.set_main_window(self)
        _TITLE_MANAGER.new_project()
        
        self.setup_ui()
        self.apply_theme()
        self._sync_menu_checkboxes()
        self.showMaximized()
    
    def setup_ui(self):
        menubar = self.menuBar()
        self.menu_system.create_menus(menubar)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        content_label = QLabel("Основная рабочая область")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setStyleSheet("font-size: 16px; color: #666666;")
        layout.addWidget(content_label)
        
        # Кнопка для тестирования изменений
        test_button = QPushButton("Симулировать изменения")
        test_button.clicked.connect(self._simulate_changes)
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(test_button)
        
        layout.addStretch()
    
    def refresh_menus(self):
        menubar = self.menuBar()
        menubar.clear()
        self.menu_system.create_menus(menubar)
    
    def apply_theme(self):
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
        
        self.menu_system._update_menu_colors()
    
    def _load_app_settings(self):
        """Загружает настройки приложения"""
        # Загружаем язык
        language = _APP_SETTINGS.get_setting("language", "ru")
        set_language(language)
        
        # Загружаем тему
        theme = _APP_SETTINGS.get_setting("theme", "dark")
        is_light = theme == "light"
        _THEME.set_theme(is_light)
    
    def _sync_menu_checkboxes(self):
        """Синхронизирует чекбоксы меню с настройками"""
        auto_save = _APP_SETTINGS.get_setting("auto_save", True)
        show_grid = _APP_SETTINGS.get_setting("show_grid", True)
        snap_to_grid = _APP_SETTINGS.get_setting("snap_to_grid", True)
        
        if "top_bar_submenu_AutoSave" in self.menu_system.checkboxes:
            self.menu_system.checkboxes["top_bar_submenu_AutoSave"].setChecked(auto_save)
        if "top_bar_submenu_ShowGrid" in self.menu_system.checkboxes:
            self.menu_system.checkboxes["top_bar_submenu_ShowGrid"].setChecked(show_grid)
        if "top_bar_submenu_SnapToGrid" in self.menu_system.checkboxes:
            self.menu_system.checkboxes["top_bar_submenu_SnapToGrid"].setChecked(snap_to_grid)
    
    def closeEvent(self, event: QCloseEvent):
        """Обрабатывает событие закрытия окна"""
        if _TITLE_MANAGER.has_unsaved_changes():
            from ..windows.save_discard_window import SaveDiscardWindow
            
            dialog = SaveDiscardWindow(self)
            dialog.exec()
            
            choice = dialog.get_user_choice()
            
            if choice == 'cancel':
                event.ignore()
                return
            elif choice == 'discard':
                pass  # Просто закрываем
            elif choice == 'save':
                # Сохранение уже обработано в диалоге
                pass
        
        event.accept()
    
    def _simulate_changes(self):
        """Симулирует изменения в проекте для тестирования"""
        _TITLE_MANAGER.set_modified(True)
        print("Проект помечен как измененный")
