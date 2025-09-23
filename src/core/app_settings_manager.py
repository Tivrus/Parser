import json
import os
from pathlib import Path
from typing import Dict, Any


class AppSettingsManager:
    
    def __init__(self):
        config_dir = Path(__file__).parent.parent / "config"
        self.settings_file = config_dir / "app_settings.json"
        self.settings = self._load_default_settings()
        self._load_settings()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        return {
            "language": "ru",
            "theme": "dark",
            "auto_save": True,
            "show_grid": True,
            "snap_to_grid": True
        }
    
    def _load_settings(self) -> None:
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except (json.JSONDecodeError, IOError):
                pass
    
    def save_settings(self) -> None:
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def get_setting(self, key: str, default=None):
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        self.settings[key] = value
    
    def get_all_settings(self) -> Dict[str, Any]:
        return self.settings.copy()


_APP_SETTINGS = AppSettingsManager()
