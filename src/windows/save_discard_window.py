from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from ..core.text_manager import get_text


class SaveDiscardWindow(QDialog):
    
    def __init__(self, parent=None, width=370, height=100):
        super().__init__(parent)
        self.setWindowTitle(get_text("window_save_discard_message"))
        self.setFixedSize(width, height)
        self.setModal(True)
        self.user_choice = None  # None, 'save', 'discard', 'cancel'
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        question_label = QLabel(get_text("window_save_discard_question"))
        question_label.setWordWrap(True)
        question_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(question_label)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        save_button = QPushButton(get_text("button_save"))
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
        
        discard_button = QPushButton(get_text("button_discard"))
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
        
        cancel_button = QPushButton(get_text("button_cancel"))
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
    
    def _save_project(self):
        self.user_choice = 'save'
        
        from ..core.project_manager import _PROJECT_MANAGER
        file_path = _PROJECT_MANAGER.get_save_file_path(self)
        
        if file_path:
            _PROJECT_MANAGER.save_project(file_path, parent_widget=self)
            print("Проект сохранен")
        else:
            print("Сохранение отменено")
            self.user_choice = 'cancel'
        
        self.close()
    
    def _discard_project(self):
        self.user_choice = 'discard'
        print("Изменения отброшены")
        self.close()
    
    def _cancel_action(self):
        self.user_choice = 'cancel'
        print("Действие отменено")
        self.close()
    
    def get_user_choice(self):
        return self.user_choice