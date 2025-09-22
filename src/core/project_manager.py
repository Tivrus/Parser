"""
Менеджер проектов приложения.

Обеспечивает управление проектами, сохранение в папку Downloads,
отслеживание последних проектов и интеграцию с заголовком окна.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any


class ProjectManager:
    """
    Менеджер проектов для управления файлами проектов.
    
    Основные функции:
    - Сохранение/открытие проектов в папке Downloads
    - Отслеживание последних 5 проектов
    - Интеграция с TitleManager для обновления заголовка окна
    """
    
    def __init__(self):
        """Инициализация менеджера проектов."""
        self.projects_dir = Path.home() / "Downloads"
        self.recent_projects_file = self.projects_dir / "recent_projects.json"
        self.max_recent_files = 5
        
        # Создаем директорию проектов если её нет
        self._ensure_projects_directory()
    
    def _ensure_projects_directory(self) -> None:
        """Создает директорию проектов если она не существует."""
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    # === ФАЙЛОВЫЕ ДИАЛОГИ ===
    
    def get_save_file_path(self, parent_widget=None) -> str:
        """
        Открывает диалог сохранения файла.
        
        Args:
            parent_widget: Родительский виджет для диалога
            
        Returns:
            Путь к файлу для сохранения или пустая строка если отменено
        """
        from PyQt6.QtWidgets import QFileDialog
        
        default_path = str(self.projects_dir / "new_project.json")
        file_path, _ = QFileDialog.getSaveFileName(
            parent_widget,
            "Сохранить проект",
            default_path,
            "JSON файлы (*.json);;Все файлы (*)"
        )
        return file_path
    
    def get_open_file_path(self, parent_widget=None) -> str:
        """
        Открывает диалог открытия файла.
        
        Args:
            parent_widget: Родительский виджет для диалога
            
        Returns:
            Путь к файлу для открытия или пустая строка если отменено
        """
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            parent_widget,
            "Открыть проект",
            str(self.projects_dir),
            "JSON файлы (*.json);;Все файлы (*)"
        )
        return file_path
    
    # === УПРАВЛЕНИЕ ПРОЕКТАМИ ===
    
    def save_project(self, file_path: str, project_data: Dict[str, Any] = None, 
                     parent_widget=None) -> bool:
        """
        Сохраняет проект в файл.
        
        Args:
            file_path: Путь к файлу проекта
            project_data: Данные проекта (если None, создается шаблон)
            parent_widget: Родительский виджет
            
        Returns:
            True если проект успешно сохранен
        """
        if project_data is None:
            project_data = self._create_default_project_data()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            self.add_recent_project(file_path)
            self._update_title_manager_save(file_path)
            
            print(f"Проект сохранен: {Path(file_path).name}")
            return True
            
        except Exception as e:
            print(f"Ошибка сохранения проекта: {str(e)}")
            return False
    
    def open_project(self, file_path: str, parent_widget=None) -> bool:
        """
        Открывает проект из файла.
        
        Args:
            file_path: Путь к файлу проекта
            parent_widget: Родительский виджет
            
        Returns:
            True если проект успешно открыт
        """
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл не найден: {file_path}")
            return False
        
        try:
            # Загружаем данные проекта
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            self.add_recent_project(file_path)
            self._update_title_manager_open(file_path)
            
            print(f"Проект открыт: {Path(file_path).name}")
            return True
            
        except Exception as e:
            print(f"Ошибка открытия проекта: {str(e)}")
            return False
    
    def _create_default_project_data(self) -> Dict[str, Any]:
        """
        Создает данные проекта по умолчанию.
        
        Returns:
            Словарь с данными проекта по умолчанию
        """
        return {
            "name": "New Project",
            "created": "2024-01-01",
            "version": "1.0.0",
            "data": {}
        }
    
    # === УПРАВЛЕНИЕ ПОСЛЕДНИМИ ПРОЕКТАМИ ===
    
    def add_recent_project(self, file_path: str) -> None:
        """
        Добавляет проект в список последних.
        
        Args:
            file_path: Путь к файлу проекта
        """
        if not file_path or not os.path.exists(file_path):
            return
        
        recent_projects = self.get_recent_projects()
        project_info = self._create_project_info(file_path)
        
        # Удаляем если уже есть (по пути)
        recent_projects = [p for p in recent_projects if p.get("path") != file_path]
        
        # Добавляем в начало списка
        recent_projects.insert(0, project_info)
        
        # Ограничиваем количество
        recent_projects = recent_projects[:self.max_recent_files]
        
        # Сохраняем
        self._save_recent_projects(recent_projects)
    
    def get_recent_projects(self) -> List[Dict[str, str]]:
        """
        Получает список последних проектов.
        
        Returns:
            Список словарей с информацией о проектах
        """
        if not self.recent_projects_file.exists():
            return []
        
        try:
            with open(self.recent_projects_file, 'r', encoding='utf-8') as f:
                recent_projects = json.load(f)
            
            return self._filter_existing_projects(recent_projects)
            
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_recent_project_name(self, project_info: Dict[str, str]) -> str:
        """
        Получает отображаемое имя проекта.
        
        Args:
            project_info: Словарь с информацией о проекте
            
        Returns:
            Отображаемое имя проекта
        """
        return project_info.get("name", Path(project_info.get("path", "")).stem)
    
    def clear_recent_projects(self) -> None:
        """Очищает список последних проектов."""
        if self.recent_projects_file.exists():
            self.recent_projects_file.unlink()
    
    def _create_project_info(self, file_path: str) -> Dict[str, str]:
        """
        Создает информацию о проекте.
        
        Args:
            file_path: Путь к файлу проекта
            
        Returns:
            Словарь с информацией о проекте
        """
        return {
            "name": Path(file_path).stem,  # Имя файла без расширения
            "path": file_path
        }
    
    def _filter_existing_projects(self, recent_projects: List) -> List[Dict[str, str]]:
        """
        Фильтрует список проектов, оставляя только существующие файлы.
        
        Args:
            recent_projects: Список проектов из JSON
            
        Returns:
            Отфильтрованный список существующих проектов
        """
        existing_projects = []
        
        for project_info in recent_projects:
            if isinstance(project_info, dict) and os.path.exists(project_info.get("path", "")):
                existing_projects.append(project_info)
            elif isinstance(project_info, str) and os.path.exists(project_info):
                # Совместимость со старым форматом
                existing_projects.append(self._create_project_info(project_info))
        
        return existing_projects
    
    def _save_recent_projects(self, recent_projects: List[Dict[str, str]]) -> None:
        """
        Сохраняет список последних проектов в JSON файл.
        
        Args:
            recent_projects: Список словарей с информацией о проектах
        """
        try:
            with open(self.recent_projects_file, 'w', encoding='utf-8') as f:
                json.dump(recent_projects, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения списка последних проектов: {e}")
    
    # === ИНТЕГРАЦИЯ С TITLE MANAGER ===
    
    def _update_title_manager_save(self, file_path: str) -> None:
        """
        Обновляет TitleManager после сохранения проекта.
        
        Args:
            file_path: Путь к сохраненному файлу
        """
        from .title_manager import _TITLE_MANAGER
        _TITLE_MANAGER.save_project(file_path)
    
    def _update_title_manager_open(self, file_path: str) -> None:
        """
        Обновляет TitleManager после открытия проекта.
        
        Args:
            file_path: Путь к открытому файлу
        """
        from .title_manager import _TITLE_MANAGER
        _TITLE_MANAGER.open_project(file_path)


# Глобальный экземпляр менеджера проектов
_PROJECT_MANAGER = ProjectManager()