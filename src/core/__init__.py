"""
Ядро приложения - основные компоненты
"""
from .theme_manager import ThemeManager, _THEME
from .config_loader import ConfigLoader
from .project_manager import ProjectManager, _PROJECT_MANAGER
from .title_manager import TitleManager, _TITLE_MANAGER
from .window_router import WindowRouter
from .text_manager import TextManager, get_text, set_language, get_current_language, has_text

__all__ = ['ThemeManager', '_THEME', 'ConfigLoader', 'ProjectManager', '_PROJECT_MANAGER', 'TitleManager', '_TITLE_MANAGER', 'WindowRouter', 'TextManager', 'get_text', 'set_language', 'get_current_language', 'has_text']
