import json
from typing import Dict, Any
from pathlib import Path


class ConfigLoader:
    
    def __init__(self, config_dir: str = None):
        """
        Инициализация загрузчика конфигураций
        
        Args:
            config_dir: Путь к директории с конфигурациями
        """
        if config_dir is None:
            current_dir = Path(__file__).parent
            config_dir = current_dir.parent / "config"
        
        self.config_dir = Path(config_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Загружает JSON файл из директории конфигураций
        
        Args:
            filename: Имя JSON файла
            
        Returns:
            Словарь с данными из JSON файла
            
        Raises:
            FileNotFoundError: Если файл не найден
            json.JSONDecodeError: Если файл содержит неверный JSON
        """
        file_path = self.config_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def load_menu_config(self) -> Dict[str, Any]:
        """Загружает конфигурацию меню"""
        return self.load_json("menu_config.json")
    
    def load_localization(self) -> Dict[str, Dict[str, str]]:
        """Загружает локализацию"""
        return self.load_json("localization.json")
    
    def load_color_schemes(self) -> Dict[str, Dict[str, Any]]:
        """Загружает цветовые схемы"""
        return self.load_json("color_schemes.json")
    


_config_loader = ConfigLoader()
def load_menu_config() -> Dict[str, Any]:
    """Загружает конфигурацию меню"""
    return _config_loader.load_menu_config()

def load_localization() -> Dict[str, Dict[str, str]]:
    """Загружает локализацию"""
    return _config_loader.load_localization()

def load_color_schemes() -> Dict[str, Dict[str, Any]]:
    """Загружает цветовые схемы"""
    return _config_loader.load_color_schemes()

