from pathlib import Path
from typing import Optional


class TitleManager:
    
    def __init__(self, app_name: str = "Parser"):
        """
        Инициализация менеджера заголовка.
        
        Args:
            app_name: Название приложения
        """
        self.app_name = app_name
        self.project_name = "untitled"
        self.project_path: Optional[str] = None
        self.is_modified = False
        self._main_window = None
    
    
    def set_main_window(self, main_window):
        """
        Устанавливает ссылку на главное окно.
        
        Args:
            main_window: Главное окно приложения
        """
        self._main_window = main_window
        self._update_title()
    
    
    def new_project(self):
        self.project_name = "untitled"
        self.project_path = None
        self.is_modified = False
        self._update_title()
    
    def open_project(self, file_path: str):
        """
        Открывает проект.
        
        Args:
            file_path: Путь к файлу проекта
        """
        self.project_path = file_path
        self.project_name = Path(file_path).stem  # Имя файла без расширения
        self.is_modified = False
        self._update_title()
    
    def save_project(self, file_path: str = None):
        """
        Сохраняет проект.
        
        Args:
            file_path: Путь для сохранения (если None, используется текущий путь)
        """
        if file_path:
            self.project_path = file_path
            self.project_name = Path(file_path).stem
        
        self.is_modified = False
        self._update_title()
    
    def set_modified(self, modified: bool = True):
        """
        Устанавливает флаг изменений.
        
        Args:
            modified: True если есть несохраненные изменения
        """
        self.is_modified = modified
        self._update_title()
    
    
    def get_project_path(self) -> Optional[str]:
        """
        Возвращает путь к текущему проекту.
        
        Returns:
            Путь к проекту или None
        """
        return self.project_path
    
    def get_project_name(self) -> str:
        """
        Возвращает название текущего проекта.
        
        Returns:
            Название проекта
        """
        return self.project_name
    
    def is_project_saved(self) -> bool:
        """
        Проверяет, сохранен ли проект.
        
        Returns:
            True если проект сохранен
        """
        return self.project_path is not None
    
    def has_unsaved_changes(self) -> bool:
        """
        Проверяет, есть ли несохраненные изменения.
        
        Returns:
            True если есть несохраненные изменения
        """
        return self.is_modified
    
    def get_full_title(self) -> str:
        """
        Возвращает полный заголовок окна.
        
        Returns:
            Полный заголовок
        """
        return self._format_title()
    
    
    def _update_title(self):
        if not self._main_window:
            return
        
        title = self._format_title()
        self._main_window.setWindowTitle(title)
    
    def _format_title(self) -> str:
        """
        Формирует заголовок окна в стиле Blender.
        
        Returns:
            Отформатированный заголовок
        """
        title_parts = []
        
        if self.is_modified:
            title_parts.append("*")
        
        title_parts.append(self.project_name)
        
        if self.project_path:
            project_dir = Path(self.project_path).parent
            title_parts.append(f"- {project_dir}")
        
        title_parts.append(f"- {self.app_name}")
        
        return " ".join(title_parts)


_TITLE_MANAGER = TitleManager()