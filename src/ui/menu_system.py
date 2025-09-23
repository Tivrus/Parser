import os
from typing import Dict, Callable, List
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QIcon, QAction

from ..core.config_loader import load_menu_config, load_localization
from ..core.theme_manager import _THEME
from ..core.project_manager import _PROJECT_MANAGER


class MenuSystem:
    
    def __init__(self, parent, language: str = "ru"):
        self.parent = parent
        self.language = language
        
        self.menus: Dict[str, QMenu] = {}
        self.actions: Dict[str, QAction] = {}
        self.checkboxes: Dict[str, QAction] = {}
        
        self._load_configurations()
        self._tr_fn: Callable[[str], str] = self._create_translator()
    
    def _load_configurations(self) -> None:
        self.menu_config = load_menu_config()
        self.localization = load_localization()
    
    def _create_translator(self) -> Callable[[str], str]:
        return lambda key: self.localization.get(self.language, {}).get(key, key)
    
    def create_menus(self, menubar: QMenuBar) -> None:
        for menu_config in self.menu_config["menus"]:
            menu_name = menu_config["name"]
            menu_id = menu_config["id"]
            
            menu = menubar.addMenu(self._tr(menu_id))
            menu.setObjectName(menu_id)
            self.menus[menu_id] = menu
            self._create_menu_items(menu, menu_config["items"], menu_name)
    
    def _create_menu_items(self, menu: QMenu, items_config: List[dict], menu_name: str) -> None:
        for item_config in items_config:
            item_type = item_config.get("type", "button")
            
            if item_type == "button":
                self._create_button_item(menu, item_config, menu_name)
            elif item_type == "checkbox":
                self._create_checkbox_item(menu, item_config, menu_name)
            elif item_type == "separator":
                menu.addSeparator()
            elif item_type == "menu":
                self._create_submenu_item(menu, item_config, menu_name)
    
    def _create_button_item(self, menu: QMenu, item_config: dict, menu_name: str) -> None:
        item_id = item_config["id"]
        action = QAction(self._tr(item_id), self.parent)
        action.setObjectName(item_id)
        
        icon_file = item_config.get("icon", "")
        if icon_file:
            icon_path = self._get_icon_path(icon_file)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                pixmap = icon.pixmap(18, 18)
                action.setIcon(QIcon(pixmap))
        
        action.triggered.connect(lambda: self._on_menu_action(item_id))
        
        menu.addAction(action)
        self.actions[item_id] = action
    
    def _create_checkbox_item(self, menu: QMenu, item_config: dict, menu_name: str) -> None:
        item_id = item_config["id"]
        default_checked = item_config.get("default", False)
        
        action = QAction(self._tr(item_id), self.parent)
        action.setObjectName(item_id)
        action.setCheckable(True)
        action.setChecked(default_checked)
        action.triggered.connect(lambda: self._on_menu_action(item_id))
        
        menu.addAction(action)
        self.checkboxes[item_id] = action
    
    def _create_submenu_item(self, menu: QMenu, item_config: dict, menu_name: str) -> None:
        item_id = item_config["id"]
        submenu_items = item_config.get("items", [])
        
        submenu = menu.addMenu(self._tr(item_id))
        submenu.setObjectName(item_id)
        
        icon_file = item_config.get("icon", "")
        if icon_file:
            icon_path = self._get_icon_path(icon_file)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                pixmap = icon.pixmap(18, 18)
                submenu.setIcon(QIcon(pixmap))
        
        self.menus[item_id] = submenu
        self._create_menu_items(submenu, submenu_items, item_id)
        
        if item_id == "top_bar_submenu_OpenRecent":
            self._populate_recent_projects_menu(submenu)
    
    def _on_menu_action(self, action_id: str) -> None:
        if action_id == "top_bar_submenu_Save":
            self._handle_save()
        elif action_id == "top_bar_submenu_SaveAs":
            self._handle_save_as()
        elif action_id == "top_bar_submenu_Open":
            self._handle_open_project()
        elif action_id == "top_bar_submenu_New":
            self._handle_new_project()
        elif action_id == "top_bar_submenu_Exit":
            self.parent.close()
        elif action_id == "top_bar_submenu_Light_Theme":
            checkbox = self.checkboxes.get(action_id)
            if checkbox:
                _THEME.set_theme(checkbox.isChecked())
                self._update_theme()
        elif action_id in ["top_bar_submenu_AutoSave", "top_bar_submenu_ShowGrid", "top_bar_submenu_SnapToGrid"]:
            self._handle_checkbox_toggle(action_id)
        else:
            self._handle_general_action(action_id)
    
    def _handle_save(self) -> None:
        from ..core.title_manager import _TITLE_MANAGER
        
        if not _TITLE_MANAGER.is_project_saved():
            self._handle_save_as()
        else:
            _PROJECT_MANAGER.save_project(
                _TITLE_MANAGER.get_project_path(), 
                parent_widget=self.parent
            )
    
    def _handle_save_as(self) -> None:
        file_path = _PROJECT_MANAGER.get_save_file_path(self.parent)
        if file_path:
            _PROJECT_MANAGER.save_project(file_path, parent_widget=self.parent)
            self.refresh_recent_projects_menu()
    
    def _handle_open_project(self) -> None:
        if self._check_unsaved_changes():
            file_path = _PROJECT_MANAGER.get_open_file_path(self.parent)
            if file_path:
                _PROJECT_MANAGER.open_project(file_path, self.parent)
                self.refresh_recent_projects_menu()
    
    def _handle_new_project(self) -> None:
        if self._check_unsaved_changes():
            # Показываем окно создания нового проекта
            if hasattr(self.parent, 'window_router'):
                self.parent.window_router.dispatch(self.parent, "top_bar_submenu_New")
    
    def _check_unsaved_changes(self) -> bool:
        """Проверяет наличие несохраненных изменений и показывает диалог при необходимости"""
        from ..core.title_manager import _TITLE_MANAGER
        
        if _TITLE_MANAGER.has_unsaved_changes():
            from ..windows.save_discard_window import SaveDiscardWindow
            
            dialog = SaveDiscardWindow(self.parent)
            dialog.exec()
            
            choice = dialog.get_user_choice()
            
            if choice == 'cancel':
                return False  # Отменяем действие
            elif choice == 'save':
                # Сохранение уже обработано в диалоге
                return True
            elif choice == 'discard':
                return True  # Продолжаем действие
        
        return True  # Нет несохраненных изменений, продолжаем
    
    def _handle_checkbox_toggle(self, action_id: str) -> None:
        """Обрабатывает переключение чекбоксов в меню"""
        from ..core.app_settings_manager import _APP_SETTINGS
        
        checkbox = self.checkboxes.get(action_id)
        if not checkbox:
            return
        
        is_checked = checkbox.isChecked()
        
        # Обновляем настройки
        if action_id == "top_bar_submenu_AutoSave":
            _APP_SETTINGS.set_setting("auto_save", is_checked)
        elif action_id == "top_bar_submenu_ShowGrid":
            _APP_SETTINGS.set_setting("show_grid", is_checked)
        elif action_id == "top_bar_submenu_SnapToGrid":
            _APP_SETTINGS.set_setting("snap_to_grid", is_checked)
        
        # Синхронизируем с окном настроек если оно открыто
        self._sync_settings_window(action_id, is_checked)
    
    def _sync_settings_window(self, menu_id: str, is_checked: bool) -> None:
        """Синхронизирует состояние чекбокса с окном настроек"""
        if hasattr(self.parent, 'menu_system'):
            # Ищем открытые окна настроек
            for child in self.parent.findChildren(type(self.parent)):
                if hasattr(child, '_sync_from_menu'):
                    child._sync_from_menu(menu_id, is_checked)
    
    def _handle_general_action(self, action_id: str) -> None:
        if hasattr(self.parent, 'window_router'):
            self.parent.window_router.dispatch(self.parent, action_id)
    
    def _populate_recent_projects_menu(self, menu: QMenu) -> None:
        recent_projects = _PROJECT_MANAGER.get_recent_projects()
        
        if recent_projects:
            if menu.actions():
                menu.addSeparator()
            
            for project_info in recent_projects:
                self._add_recent_project_to_menu(menu, project_info)
        else:
            self._add_no_projects_placeholder(menu)
    
    def _add_recent_project_to_menu(self, menu: QMenu, project_info: Dict[str, str]) -> None:
        project_name = _PROJECT_MANAGER.get_recent_project_name(project_info)
        project_path = project_info.get("path", "")
        
        action = QAction(project_name, self.parent)
        action.setObjectName(f"recent_project_{project_path}")
        action.triggered.connect(
            lambda checked, path=project_path: self._on_open_recent_project(path)
        )
        
        menu.addAction(action)
    
    def _add_no_projects_placeholder(self, menu: QMenu) -> None:
        if menu.actions():
            menu.addSeparator()
        
        from ..core.text_manager import get_text
        no_projects_action = QAction(get_text("message_no_recent_projects"), self.parent)
        no_projects_action.setEnabled(False)
        menu.addAction(no_projects_action)
    
    def _on_open_recent_project(self, project_path: str) -> None:
        if self._check_unsaved_changes():
            _PROJECT_MANAGER.open_project(project_path, self.parent)
            self.refresh_recent_projects_menu()
    
    def refresh_recent_projects_menu(self) -> None:
        if "top_bar_submenu_OpenRecent" in self.menus:
            menu = self.menus["top_bar_submenu_OpenRecent"]
            self._clear_recent_projects_from_menu(menu)
            self._populate_recent_projects_menu(menu)
    
    def _clear_recent_projects_from_menu(self, menu: QMenu) -> None:
        actions_to_remove = []
        for action in menu.actions():
            if (action.objectName().startswith("recent_project_") or 
                not action.isEnabled()):
                actions_to_remove.append(action)
        
        for action in actions_to_remove:
            menu.removeAction(action)
    
    def _update_theme(self) -> None:
        self.parent.apply_theme()
        self._update_menu_colors()
        self._update_menu_icons()
    
    def _update_menu_colors(self) -> None:
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
    
    def _update_menu_icons(self) -> None:
        for item_id, action in self.actions.items():
            icon_file = self._find_icon_in_config(item_id, "button")
            if icon_file:
                icon_path = self._get_icon_path(icon_file)
                if os.path.exists(icon_path):
                    icon = QIcon(icon_path)
                    pixmap = icon.pixmap(18, 18)
                    action.setIcon(QIcon(pixmap))
        
        for item_id, submenu in self.menus.items():
            if hasattr(submenu, 'menuBar'):
                continue
            icon_file = self._find_icon_in_config(item_id, "menu")
            if icon_file:
                icon_path = self._get_icon_path(icon_file)
                if os.path.exists(icon_path):
                    icon = QIcon(icon_path)
                    pixmap = icon.pixmap(18, 18)
                    submenu.setIcon(QIcon(pixmap))
    
    def _tr(self, key: str) -> str:
        return self._tr_fn(key)
    
    def _get_icon_path(self, icon_file: str) -> str:
        theme_folder = os.path.join(_THEME.icons_base_path, "light_theme" if _THEME.is_light_theme() else "dark_theme")
        path = os.path.join(theme_folder, icon_file)
        if not os.path.exists(path):
            # Fallback на другую тему если иконка не найдена
            fallback_folder = os.path.join(_THEME.icons_base_path, "dark_theme" if _THEME.is_light_theme() else "light_theme")
            path = os.path.join(fallback_folder, icon_file)
        return path
    
    def _find_icon_in_config(self, item_id: str, item_type: str) -> str:
        for menu_config in self.menu_config["menus"]:
            for item_config in menu_config["items"]:
                if item_config.get("id") == item_id and item_config.get("type") == item_type:
                    return item_config.get("icon", "")
        return ""