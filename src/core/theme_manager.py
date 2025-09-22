"""
Менеджер тем приложения
"""
from typing import Dict
from pathlib import Path
from .config_loader import load_color_schemes


class ThemeManager:
    """Класс для управления темами приложения"""
    
    def __init__(self):
        """Инициализация менеджера тем"""
        self.current_theme = "dark"
        self.color_schemes = load_color_schemes()
        self.icons_base_path = Path(__file__).parent.parent.parent / "utils" / "sub_menu_icons"
    
    def is_light_theme(self) -> bool:
        """Проверяет, является ли текущая тема светлой"""
        return self.current_theme == "light"
    
    def set_theme(self, is_light: bool) -> None:
        """
        Устанавливает тему приложения
        
        Args:
            is_light: True для светлой темы, False для темной
        """
        self.current_theme = "light" if is_light else "dark"
    
    def get_all_colors(self, element_id: str) -> Dict[str, str]:
        """
        Получает все цвета для элемента
        
        Args:
            element_id: Идентификатор элемента
            
        Returns:
            Словарь с цветами элемента
        """
        return self.color_schemes.get(self.current_theme, {}).get(element_id, {})
    
    def get_color(self, element_id: str, color_key: str) -> str:
        """
        Получает конкретный цвет для элемента
        
        Args:
            element_id: Идентификатор элемента
            color_key: Ключ цвета
            
        Returns:
            Значение цвета
        """
        colors = self.get_all_colors(element_id)
        return colors.get(color_key, "")


# Глобальный экземпляр менеджера тем
_THEME = ThemeManager()
