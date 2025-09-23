from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ..core.theme_manager import _THEME


class WorkspacePanel(QWidget):
    
    def __init__(self, title="Рабочая панель", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Заголовок панели
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Заглушка для будущего контента
        placeholder_label = QLabel("Здесь будет размещен контент панели")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder_label)
        
        # Применяем тему
        self.apply_theme(title_label, placeholder_label)
        
        # Добавляем растягивающийся элемент
        layout.addStretch()
    
    def apply_theme(self, title_label=None, placeholder_label=None):
        """Применяет тему к компонентам панели"""
        colors = _THEME.get_all_colors("panel")
        
        # Если параметры не переданы, ищем виджеты в layout
        if title_label is None or placeholder_label is None:
            layout = self.layout()
            if layout and layout.count() > 0:
                title_label = layout.itemAt(0).widget() if title_label is None else title_label
                placeholder_label = layout.itemAt(1).widget() if placeholder_label is None else placeholder_label
        
        if title_label:
            # Стиль для заголовка
            title_style = f"""
                QLabel {{
                    font-size: 18px;
                    font-weight: bold;
                    color: {colors.get('title_text', '#333')};
                    padding: 10px;
                    background-color: {colors.get('title_background', '#f8f8f8')};
                    border-bottom: 2px solid {colors.get('title_border', '#ccc')};
                    margin-bottom: 10px;
                    border-radius: 6px 6px 0 0;
                }}
            """
            title_label.setStyleSheet(title_style)
        
        if placeholder_label:
            # Стиль для заглушки
            placeholder_style = f"""
                QLabel {{
                    font-size: 14px;
                    color: {colors.get('text', '#666')};
                    padding: 20px;
                    background-color: {colors.get('placeholder_background', '#f8f8f8')};
                    border: 2px dashed {colors.get('placeholder_border', '#ccc')};
                    border-radius: 8px;
                }}
            """
            placeholder_label.setStyleSheet(placeholder_style)
