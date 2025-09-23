from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .base_window import BaseWindow
from ..core.text_manager import get_text


class NewWindow(BaseWindow):
    
    def __init__(self, parent=None, width=400, height=300):
        super().__init__(parent, get_text("window_new_title"), width, height)
        self.project_created = False
    
    def create_content(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        title_label = QLabel(get_text("window_new_create_project"))
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(title_label)
        
        name_label = QLabel(get_text("window_new_project_name"))
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(get_text("window_new_project_name_placeholder"))
        self.name_input.setText(get_text("window_new_title"))
        layout.addWidget(self.name_input)
        
        desc_label = QLabel(get_text("window_new_project_desc"))
        layout.addWidget(desc_label)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText(get_text("window_new_project_desc_placeholder"))
        layout.addWidget(self.desc_input)
        
        button_layout = QHBoxLayout()
        
        create_button = QPushButton(get_text("button_create"))
        create_button.clicked.connect(self._create_project)
        create_button.setDefault(True)
        
        cancel_button = QPushButton(get_text("button_cancel"))
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return content
    
    def _create_project(self):
        project_name = self.name_input.text().strip()
        if not project_name:
            project_name = get_text("window_new_title")
        
        project_desc = self.desc_input.text().strip()
        
        from ..core.title_manager import _TITLE_MANAGER
        _TITLE_MANAGER.new_project()
        
        if project_name != get_text("window_new_title"):
            _TITLE_MANAGER.project_name = project_name
            _TITLE_MANAGER._update_title()
        
        print(f"Создан новый проект: {project_name}")
        if project_desc:
            print(f"Описание: {project_desc}")
        
        self.project_created = True
        self.close()