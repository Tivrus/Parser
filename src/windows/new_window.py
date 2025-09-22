"""
Окно создания нового проекта
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .base_window import BaseWindow


class NewWindow(BaseWindow):
    """Окно создания нового проекта"""
    
    def __init__(self, parent=None, width=400, height=300):
        """Инициализация окна создания нового проекта"""
        super().__init__(parent, "Новый проект", width, height)
        self.project_created = False
    
    def create_content(self):
        """Создает содержимое окна создания нового проекта"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Заголовок
        title_label = QLabel("Создать новый проект")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title_label)
        
        # Поле для названия проекта
        name_label = QLabel("Название проекта:")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название проекта...")
        self.name_input.setText("Новый проект")
        layout.addWidget(self.name_input)
        
        # Описание
        desc_label = QLabel("Описание:")
        layout.addWidget(desc_label)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Описание проекта (необязательно)...")
        layout.addWidget(self.desc_input)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        create_button = QPushButton("Создать")
        create_button.clicked.connect(self._create_project)
        create_button.setDefault(True)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return content
    
    def _create_project(self):
        """Создает новый проект"""
        project_name = self.name_input.text().strip()
        if not project_name:
            project_name = "Новый проект"
        
        project_desc = self.desc_input.text().strip()
        
        # Создаем новый проект
        from ...core.title_manager import _TITLE_MANAGER
        _TITLE_MANAGER.new_project()
        
        # Устанавливаем название проекта если пользователь ввел его
        if project_name != "Новый проект":
            _TITLE_MANAGER.project_name = project_name
            _TITLE_MANAGER._update_title()
        
        print(f"Создан новый проект: {project_name}")
        if project_desc:
            print(f"Описание: {project_desc}")
        
        self.project_created = True
        self.close()