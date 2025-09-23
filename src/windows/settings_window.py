from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QCheckBox
from PyQt6.QtCore import Qt
from .base_window import BaseWindow
from ..core.app_settings_manager import _APP_SETTINGS
from ..core.text_manager import get_text, set_language, get_current_language
from ..core.theme_manager import _THEME


class SettingsWindow(BaseWindow):
    
    def __init__(self, parent=None, width=600, height=500):
        # Загружаем настройки перед инициализацией
        self.original_language = _APP_SETTINGS.get_setting("language", "ru")
        self.original_theme = _APP_SETTINGS.get_setting("theme", "dark")
        self.original_auto_save = _APP_SETTINGS.get_setting("auto_save", True)
        self.original_show_grid = _APP_SETTINGS.get_setting("show_grid", True)
        self.original_snap_to_grid = _APP_SETTINGS.get_setting("snap_to_grid", True)
        
        super().__init__(parent, "Настройки приложения", width, height)
    
    def create_content(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Заголовок
        title_label = QLabel("Настройки приложения")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title_label)
        
        # Язык
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Язык:")
        lang_label.setFixedWidth(120)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        self.language_combo.setCurrentText("Русский" if self.original_language == "ru" else "English")
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        layout.addLayout(lang_layout)
        
        # Тема
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Тема:")
        theme_label.setFixedWidth(120)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Темная", "Светлая"])
        self.theme_combo.setCurrentText("Светлая" if self.original_theme == "light" else "Темная")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        # Auto Save
        self.auto_save_checkbox = QCheckBox("Автосохранение")
        self.auto_save_checkbox.setChecked(self.original_auto_save)
        self.auto_save_checkbox.stateChanged.connect(self._on_auto_save_changed)
        layout.addWidget(self.auto_save_checkbox)
        
        # Show Grid
        self.show_grid_checkbox = QCheckBox("Показывать сетку")
        self.show_grid_checkbox.setChecked(self.original_show_grid)
        self.show_grid_checkbox.stateChanged.connect(self._on_show_grid_changed)
        layout.addWidget(self.show_grid_checkbox)
        
        # Snap to Grid
        self.snap_to_grid_checkbox = QCheckBox("Привязка к сетке")
        self.snap_to_grid_checkbox.setChecked(self.original_snap_to_grid)
        self.snap_to_grid_checkbox.stateChanged.connect(self._on_snap_to_grid_changed)
        layout.addWidget(self.snap_to_grid_checkbox)
        
        layout.addStretch()
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self._save_settings)
        save_button.setDefault(True)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)
        
        return content
    
    def _on_language_changed(self, text):
        new_language = "ru" if text == "Русский" else "en"
        set_language(new_language)
        _APP_SETTINGS.set_setting("language", new_language)
        
        # Обновляем родительское окно если есть
        if hasattr(self.parent(), 'menu_system'):
            self.parent().menu_system.language = new_language
            self.parent().menu_system._load_configurations()
            self.parent().refresh_menus()
    
    def _on_theme_changed(self, text):
        is_light = text == "Светлая"
        _THEME.set_theme(is_light)
        _APP_SETTINGS.set_setting("theme", "light" if is_light else "dark")
        
        # Обновляем тему родительского окна если есть
        if hasattr(self.parent(), 'apply_theme'):
            self.parent().apply_theme()
        
        # Обновляем иконки меню
        if hasattr(self.parent(), 'menu_system'):
            self.parent().menu_system._update_menu_icons()
    
    def _on_auto_save_changed(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        _APP_SETTINGS.set_setting("auto_save", is_checked)
        self._sync_menu_checkbox("top_bar_submenu_AutoSave", is_checked)
    
    def _on_show_grid_changed(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        _APP_SETTINGS.set_setting("show_grid", is_checked)
        self._sync_menu_checkbox("top_bar_submenu_ShowGrid", is_checked)
    
    def _on_snap_to_grid_changed(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        _APP_SETTINGS.set_setting("snap_to_grid", is_checked)
        self._sync_menu_checkbox("top_bar_submenu_SnapToGrid", is_checked)
    
    def _sync_menu_checkbox(self, menu_id, is_checked):
        """Синхронизирует состояние чекбокса в меню с настройками"""
        if hasattr(self.parent(), 'menu_system'):
            menu_system = self.parent().menu_system
            if menu_id in menu_system.checkboxes:
                menu_system.checkboxes[menu_id].setChecked(is_checked)
    
    def _sync_from_menu(self, menu_id, is_checked):
        """Синхронизирует состояние чекбокса из меню в настройки"""
        if menu_id == "top_bar_submenu_AutoSave":
            self.auto_save_checkbox.setChecked(is_checked)
        elif menu_id == "top_bar_submenu_ShowGrid":
            self.show_grid_checkbox.setChecked(is_checked)
        elif menu_id == "top_bar_submenu_SnapToGrid":
            self.snap_to_grid_checkbox.setChecked(is_checked)
    
    def _save_settings(self):
        _APP_SETTINGS.save_settings()
        self.close()
    
    def closeEvent(self, event):
        # Сохраняем настройки при закрытии окна
        _APP_SETTINGS.save_settings()
        event.accept()
