"""
Ядро приложения - основные компоненты
"""
from .theme_manager import ThemeManager, _THEME
from .config_loader import ConfigLoader

__all__ = ['ThemeManager', '_THEME', 'ConfigLoader']
