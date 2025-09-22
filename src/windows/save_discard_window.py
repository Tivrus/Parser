"""
Окно диалога сохранения проекта
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .base_window import BaseWindow


class SaveDiscardWindow(BaseWindow):
    """Маленькое окно для выбора сохранения проекта"""
    
    def __init__(self, parent=None, width=350, height=200):
        """Инициализация окна диалога сохранения"""
        super().__init__(parent, "Сохранить проект?", width, height)
        self.user_choice = None  # None, 'save', 'discard', 'cancel'
    
    def create_content(self):
        """Создает содержимое окна диалога сохранения"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Сообщение
        message_label = QLabel("У вас есть несохраненные изменения.")
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(message_label)
        
        question_label = QLabel("Хотите сохранить текущий проект?")
        question_label.setWordWrap(True)
        question_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(question_label)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Кнопка "Сохранить"
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self._save_project)
        save_button.setDefault(True)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        
        # Кнопка "Не сохранять"
        discard_button = QPushButton("Не сохранять")
        discard_button.clicked.connect(self._discard_project)
        discard_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        
        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self._cancel_action)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5A6268;
            }
        """)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(discard_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return content
    
    def _save_project(self):
        """Обрабатывает сохранение проекта"""
        self.user_choice = 'save'
        
        # Показываем диалог сохранения
        from ...core.project_manager import _PROJECT_MANAGER
        file_path = _PROJECT_MANAGER.get_save_file_path(self)
        
        if file_path:
            _PROJECT_MANAGER.save_project(file_path, parent_widget=self)
            print("Проект сохранен")
        else:
            print("Сохранение отменено")
            self.user_choice = 'cancel'
        
        self.close()
    
    def _discard_project(self):
        """Обрабатывает отказ от сохранения"""
        self.user_choice = 'discard'
        print("Изменения отброшены")
        self.close()
    
    def _cancel_action(self):
        """Обрабатывает отмену действия"""
        self.user_choice = 'cancel'
        print("Действие отменено")
        self.close()
    
    def get_user_choice(self):
        """
        Возвращает выбор пользователя.
        
        Returns:
            'save', 'discard', 'cancel' или None
        """
        return self.user_choice