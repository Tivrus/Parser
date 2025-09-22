"""
Система меню приложения
"""
import os
from typing import Dict, Callable, Optional
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QIcon, QAction
from ..core.config_loader import load_menu_config, load_localization
from ..core.theme_manager import _THEME


class MenuSystem:
    """Класс для управления системой меню"""
    
    def __init__(self, parent, language: str = "ru"):
        """
        Инициализация системы меню
        
        Args:
            parent: Родительское окно
            language: Язык интерфейса
        """
        self.parent = parent
        self.language = language
        self.menus: Dict[str, QMenu] = {}
        self.actions: Dict[str, QAction] = {}
        self.checkboxes: Dict[str, QAction] = {}
        
        # Загружаем конфигурации
        self.menu_config = load_menu_config()
        self.localization = load_localization()
        
        # Translator function
        self._tr_fn: Callable[[str], str] = lambda key: self.localization.get(self.language, {}).get(key, key)
    
    def create_menus(self, menubar: QMenuBar):
        """Создает меню в меню-баре"""
        for menu_config in self.menu_config["menus"]:
            menu_name = menu_config["name"]
            menu_id = menu_config["id"]
            
            menu = menubar.addMenu(self._tr(menu_id))
            self.menus[menu_name] = menu
            
            self._create_menu_items(menu, menu_config["items"], menu_name)
    
    def _create_menu_items(self, menu: QMenu, items_config: list, menu_name: str):
        """Создает элементы меню"""
        for item_config in items_config:
            item_type = item_config.get("type", "button")
            
            if item_type == "separator":
                menu.addSeparator()
            elif item_type == "button":
                self._create_button_item(menu, item_config, menu_name)
            elif item_type == "checkbox":
                self._create_checkbox_item(menu, item_config, menu_name)
    
    def _create_button_item(self, menu: QMenu, item_config: dict, menu_name: str):
        """Создает кнопочный элемент меню"""
        item_id = item_config["id"]
        action = QAction(self._tr(item_id), self.parent)
        action.setObjectName(item_id)
        
        # Add icon if exists
        icon_file = item_config.get("icon", "")
        if icon_file:
            icon_path = self._get_icon_path(icon_file)
            if os.path.exists(icon_path):
                # Load and scale icon to 16x16 pixels
                icon = QIcon(icon_path)
                pixmap = icon.pixmap(16, 16)
                action.setIcon(QIcon(pixmap))
        
        action.triggered.connect(lambda checked, m=menu_name, i=item_id: self._on_menu_action(m, i, "button"))
        menu.addAction(action)
        self.actions[item_id] = action
    
    def _create_checkbox_item(self, menu: QMenu, item_config: dict, menu_name: str):
        """Создает чекбокс элемент меню"""
        item_id = item_config["id"]
        default_value = item_config.get("default", False)
        
        action = QAction(self._tr(item_id), self.parent)
        action.setCheckable(True)
        action.setChecked(default_value)
        action.setObjectName(item_id)
        
        action.triggered.connect(lambda checked, m=menu_name, i=item_id: self._on_menu_action(m, i, "checkbox", checked))
        menu.addAction(action)
        self.checkboxes[item_id] = action
    
    def _get_icon_path(self, icon_filename: str) -> str:
        """Получает путь к иконке в зависимости от текущей темы"""
        theme_folder = os.path.join(_THEME.icons_base_path, "light_theme" if _THEME.is_light_theme() else "dark_theme")
        path = os.path.join(theme_folder, icon_filename)
        if _THEME.is_light_theme() and not os.path.exists(path):
            path = os.path.join(_THEME.icons_base_path, "dark_theme", icon_filename)
        return path
    
    def _on_menu_action(self, menu_name: str, item_id: str, item_type: str, value=None):
        """Обрабатывает действия меню"""
        if item_type == "button":
            # Route window actions
            if hasattr(self.parent, 'window_router'):
                if not self.parent.window_router.dispatch(self.parent, item_id):
                    if item_id == "top_bar_submenu_Exit":
                        self.parent.close()
        elif item_type == "checkbox":
            if item_id == "top_bar_submenu_Light_Theme":
                _THEME.set_theme(value)
                self._update_theme()
    
    def _update_theme(self):
        """Обновляет тему приложения"""
        # Update application theme
        self.parent.apply_theme()
        
        # Update menu colors
        self._update_menu_colors()
        
        # Update icons
        self._update_menu_icons()
    
    def _update_menu_colors(self):
        """Обновляет цвета меню"""
        # Apply theme to menu bar
        colors = _THEME.get_all_colors("top_menu_bar")
        bg_color = colors.get("background", "#F0F0F0")
        text_color = colors.get("text", "#000000")
        
        self.parent.menuBar().setStyleSheet(f"""
            QMenuBar {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 4px 8px;
            }}
            QMenuBar::item:selected {{
                background: {colors.get('hover', '#E5F3FF')};
            }}
            QMenuBar::item:pressed {{
                background: {colors.get('click', '#CCE8FF')};
            }}
            QMenu {{
                background-color: {_THEME.get_all_colors('submenu_container').get('background', '#FFFFFF')};
                color: {_THEME.get_all_colors('submenu_button').get('text', '#000000')};
                border: 1px solid {_THEME.get_all_colors('submenu_container').get('border', '#CCCCCC')};
                padding: 4px;
            }}
            QMenu::item {{
                background-color: transparent;
                padding: 6px 8px 6px 12px;
                margin: 1px 0px;
                border-radius: 4px;
                min-height: 18px;
            }}
            QMenu::item:selected {{
                background-color: {_THEME.get_all_colors('submenu_button').get('hover', '#E5F3FF')};
            }}
            QMenu::item:pressed {{
                background-color: {_THEME.get_all_colors('submenu_button').get('click', '#CCE8FF')};
            }}
            QMenu::icon {{
                margin-left: 0px;
                margin-right: 8px;
                width: 16px;
                height: 16px;
            }}
            QMenu::indicator {{
                width: 16px;
                height: 16px;
                margin-left: 0px;
                margin-right: 8px;
            }}
        """)
    
    def _update_menu_icons(self):
        """Обновляет иконки меню"""
        # Update icons for all actions
        for item_id, action in self.actions.items():
            # Find the item config to get icon filename
            for menu_config in self.menu_config["menus"]:
                for item_config in menu_config["items"]:
                    if item_config.get("id") == item_id and item_config.get("type") == "button":
                        icon_file = item_config.get("icon", "")
                        if icon_file:
                            icon_path = self._get_icon_path(icon_file)
                            if os.path.exists(icon_path):
                                # Load and scale icon to 16x16 pixels
                                icon = QIcon(icon_path)
                                pixmap = icon.pixmap(16, 16)
                                action.setIcon(QIcon(pixmap))
                        break
    
    def _tr(self, key: str) -> str:
        """Переводит ключ на текущий язык"""
        return self._tr_fn(key)
