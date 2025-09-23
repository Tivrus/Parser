from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from ..core.theme_manager import _THEME
from ..core.text_manager import get_text


class WebBrowser(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Панель навигации
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 5, 10, 5)
        nav_layout.setSpacing(10)
        
        # Кнопка "Назад"
        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(30, 30)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setToolTip("Назад")
        
        # Кнопка "Вперед"
        self.forward_button = QPushButton("→")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setToolTip("Вперед")
        
        # Кнопка "Обновить"
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedSize(30, 30)
        self.refresh_button.clicked.connect(self.refresh_page)
        self.refresh_button.setToolTip("Обновить")
        
        # Поле ввода URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL и нажмите Enter...")
        self.url_input.setText("https://www.google.com")
        self.url_input.returnPressed.connect(self.navigate_to_url)
        
        # Кнопка "Перейти"
        self.go_button = QPushButton(get_text("button_go"))
        self.go_button.setFixedSize(80, 30)
        self.go_button.clicked.connect(self.navigate_to_url)
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_input)
        nav_layout.addWidget(self.go_button)
        
        layout.addLayout(nav_layout)
        
        # Веб-виджет
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.on_url_changed)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        # Загружаем Google.com по умолчанию
        self.web_view.setUrl(QUrl("https://www.google.com"))
        
        layout.addWidget(self.web_view)
        
        # Применяем тему
        self.apply_theme()
    
    def apply_theme(self):
        """Применяет тему к компонентам веб-браузера"""
        colors = _THEME.get_all_colors("web_browser")
        
        # Стиль для поля ввода URL
        url_style = f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 2px solid {colors.get('input_border', '#ccc')};
                border-radius: 6px;
                font-size: 14px;
                background-color: {colors.get('input_background', '#fff')};
                color: {colors.get('text', '#333')};
            }}
            QLineEdit:focus {{
                border-color: {colors.get('input_focus', '#007ACC')};
            }}
        """
        self.url_input.setStyleSheet(url_style)
        
        # Стиль для кнопок
        button_style = f"""
            QPushButton {{
                background-color: {colors.get('button_background', '#f0f0f0')};
                border: 1px solid {colors.get('button_border', '#ccc')};
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                color: {colors.get('text', '#333')};
            }}
            QPushButton:hover {{
                background-color: {colors.get('button_hover', '#e0e0e0')};
            }}
            QPushButton:pressed {{
                background-color: {colors.get('button_pressed', '#d0d0d0')};
            }}
            QPushButton:disabled {{
                background-color: {colors.get('button_background', '#f8f8f8')};
                color: #999;
            }}
        """
        
        self.back_button.setStyleSheet(button_style)
        self.forward_button.setStyleSheet(button_style)
        self.refresh_button.setStyleSheet(button_style)
        self.go_button.setStyleSheet(button_style)
        
        # Обновляем текст кнопки
        self.update_button_texts()
    
    def update_button_texts(self):
        """Обновляет тексты кнопок при смене языка"""
        self.go_button.setText(get_text("button_go"))
    
    def navigate_to_url(self):
        """Переходит по указанному URL"""
        url_text = self.url_input.text().strip()
        
        if not url_text:
            return
        
        # Добавляем протокол если его нет
        if not url_text.startswith(('http://', 'https://')):
            url_text = 'https://' + url_text
        
        try:
            url = QUrl(url_text)
            self.web_view.load(url)
        except Exception as e:
            print(f"Ошибка загрузки URL: {e}")
    
    def go_back(self):
        """Переходит назад в истории"""
        if self.web_view.history().canGoBack():
            self.web_view.back()
    
    def go_forward(self):
        """Переходит вперед в истории"""
        if self.web_view.history().canGoForward():
            self.web_view.forward()
    
    def refresh_page(self):
        """Обновляет текущую страницу"""
        self.web_view.reload()
    
    def on_url_changed(self, url):
        """Вызывается при изменении URL"""
        self.url_input.setText(url.toString())
        self.update_navigation_buttons()
    
    def on_load_finished(self, success):
        """Вызывается при завершении загрузки страницы"""
        self.update_navigation_buttons()
        if not success:
            print("Ошибка загрузки страницы")
    
    def update_navigation_buttons(self):
        """Обновляет состояние кнопок навигации"""
        self.back_button.setEnabled(self.web_view.history().canGoBack())
        self.forward_button.setEnabled(self.web_view.history().canGoForward())
    
    def load_url(self, url):
        """Загружает указанный URL"""
        if isinstance(url, str):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            url = QUrl(url)
        self.web_view.load(url)
