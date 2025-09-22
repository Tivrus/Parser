"""
Роутер для управления окнами приложения
"""
from ..windows import SettingsWindow, AboutWindow, NewWindow


class WindowRouter:
    """Класс для маршрутизации действий к соответствующим окнам"""
    
    def __init__(self):
        """Инициализация роутера"""
        pass
    
    def dispatch(self, parent, action_id: str) -> bool:
        """
        Выполняет действие по его идентификатору
        
        Args:
            parent: Родительское окно
            action_id: Идентификатор действия
            
        Returns:
            True если действие было выполнено, False в противном случае
        """
        try:
            if action_id == "top_bar_submenu_Preferences":
                window = SettingsWindow(parent, width=600, height=500)
                window.show()
                return True
                
            elif action_id == "top_bar_submenu_New":
                window = NewWindow(parent, width=400, height=300)
                window.show()
                return True
                                
            elif action_id == "top_bar_submenu_About_App":
                window = AboutWindow(parent, width=480, height=560)
                window.show()
                return True
                
            else:
                print(f"No handler found for action: {action_id}")
                return False
                
        except Exception as e:
            print(f"Error opening window for action '{action_id}': {e}")
            return False