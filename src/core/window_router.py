"""
Роутер для управления окнами приложения
"""
from typing import Dict, Any
from .config_loader import load_window_routes
from ..windows import SettingsWindow, DocumentationWindow, AboutWindow


class WindowRouter:
    """Класс для маршрутизации действий к соответствующим окнам"""
    
    def __init__(self, routes: Dict[str, Dict[str, Any]] = None):
        """
        Инициализация роутера
        
        Args:
            routes: Словарь с маршрутами. Если None, загружается из конфигурации
        """
        if routes is None:
            routes = load_window_routes()
        self.routes = routes
    
    def dispatch(self, parent, action_id: str) -> bool:
        """
        Выполняет действие по его идентификатору
        
        Args:
            parent: Родительское окно
            action_id: Идентификатор действия
            
        Returns:
            True если действие было выполнено, False в противном случае
        """
        route = self.routes.get(action_id)
        if not route:
            return False
            
        module = route.get("module")
        func = route.get("function")
        args = route.get("args", {})
        
        try:
            if module == "settings" and func == "open_settings_window":
                window = SettingsWindow(parent, **args)
                window.show()
            elif module == "documentation" and func == "open_documentation_window":
                window = DocumentationWindow(parent, **args)
                window.show()
            elif module == "about" and func == "open_about_window":
                window = AboutWindow(parent, **args)
                window.show()
            else:
                return False
            return True
        except Exception as e:
            print(f"Error opening window: {e}")
            return False
