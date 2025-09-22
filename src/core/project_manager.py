"""
Менеджер проектов для отслеживания последних файлов
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any


class ProjectManager:
    """Класс для управления проектами и последними файлами"""
    
    def __init__(self):
        """Инициализация менеджера проектов"""
        self.projects_dir = Path.home() / "Downloads"
        self.recent_projects_file = self.projects_dir / "recent_projects.json"
        self.max_recent_files = 5
        
        # Создаем директорию проектов если её нет
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def get_save_file_path(self, parent_widget=None) -> str:
        """
        Открывает диалог сохранения файла
        
        Args:
            parent_widget: Родительский виджет для диалога
            
        Returns:
            Путь к файлу для сохранения или пустая строка если отменено
        """
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            parent_widget,
            "Сохранить проект",
            str(self.projects_dir / "new_project.json"),
            "JSON файлы (*.json);;Все файлы (*)"
        )
        return file_path
    
    def get_open_file_path(self, parent_widget=None) -> str:
        """
        Открывает диалог открытия файла
        
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
    
    def add_recent_project(self, file_path: str):
        """
        Добавляет проект в список последних
        
        Args:
            file_path: Путь к файлу проекта
        """
        if not file_path or not os.path.exists(file_path):
            return
        
        recent_projects = self.get_recent_projects()
        
        # Создаем информацию о проекте
        project_info = {
            "name": Path(file_path).stem,  # Имя файла без расширения
            "path": file_path
        }
        
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
        Получает список последних проектов
        
        Returns:
            Список словарей с информацией о проектах
        """
        if not self.recent_projects_file.exists():
            return []
        
        try:
            with open(self.recent_projects_file, 'r', encoding='utf-8') as f:
                recent_projects = json.load(f)
            
            # Фильтруем только существующие файлы
            existing_projects = []
            for project_info in recent_projects:
                if isinstance(project_info, dict) and os.path.exists(project_info.get("path", "")):
                    existing_projects.append(project_info)
                elif isinstance(project_info, str) and os.path.exists(project_info):
                    # Совместимость со старым форматом
                    existing_projects.append({
                        "name": Path(project_info).stem,
                        "path": project_info
                    })
            
            return existing_projects
        except (json.JSONDecodeError, IOError):
            return []
    
    def get_recent_project_name(self, project_info: Dict[str, str]) -> str:
        """
        Получает отображаемое имя проекта
        
        Args:
            project_info: Словарь с информацией о проекте
            
        Returns:
            Отображаемое имя проекта
        """
        return project_info.get("name", Path(project_info.get("path", "")).stem)
    
    def _save_recent_projects(self, recent_projects: List[Dict[str, str]]):
        """
        Сохраняет список последних проектов
        
        Args:
            recent_projects: Список словарей с информацией о проектах
        """
        try:
            with open(self.recent_projects_file, 'w', encoding='utf-8') as f:
                json.dump(recent_projects, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения списка последних проектов: {e}")
    
    def clear_recent_projects(self):
        """Очищает список последних проектов"""
        if self.recent_projects_file.exists():
            self.recent_projects_file.unlink()
    
    def open_project(self, file_path: str, parent_widget=None) -> bool:
        """
        Открывает проект
        
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
            # Здесь можно добавить логику загрузки проекта
            self.add_recent_project(file_path)
            
            # Обновляем заголовок окна
            from .title_manager import _TITLE_MANAGER
            _TITLE_MANAGER.open_project(file_path)
            
            print(f"Проект открыт: {Path(file_path).name}")
            return True
        except Exception as e:
            print(f"Ошибка открытия проекта: {str(e)}")
            return False
    
    def save_project(self, file_path: str, project_data: Dict[str, Any] = None, parent_widget=None) -> bool:
        """
        Сохраняет проект
        
        Args:
            file_path: Путь к файлу проекта
            project_data: Данные проекта
            parent_widget: Родительский виджет
            
        Returns:
            True если проект успешно сохранен
        """
        if project_data is None:
            project_data = {
                "name": "New Project",
                "created": "2024-01-01",
                "version": "1.0.0",
                "data": {}
            }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            self.add_recent_project(file_path)
            
            # Обновляем заголовок окна
            from .title_manager import _TITLE_MANAGER
            _TITLE_MANAGER.save_project(file_path)
            
            print(f"Проект сохранен: {Path(file_path).name}")
            return True
        except Exception as e:
            print(f"Ошибка сохранения проекта: {str(e)}")
            return False


# Глобальный экземпляр менеджера проектов
_PROJECT_MANAGER = ProjectManager()
