from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSplitter
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from ..core.theme_manager import _THEME
from ..core.text_manager import get_text


class WebBrowser(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dev_tools_visible = False
        self.dev_tools_view = None
        self.inspector_mode = False
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
        
        # Кнопка "Inspector Mode"
        self.inspector_button = QPushButton()
        self.inspector_button.setFixedSize(30, 30)
        self.inspector_button.setToolTip("Режим инспектора")
        self.inspector_button.setCheckable(True)
        self.inspector_button.clicked.connect(self.toggle_inspector_mode)
        
        # Устанавливаем иконку для кнопки инспектора
        self._set_inspector_icon()
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.url_input)
        nav_layout.addWidget(self.go_button)
        nav_layout.addWidget(self.inspector_button)
        
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
        self.inspector_button.setStyleSheet(button_style)
        
        # Обновляем текст кнопки и иконки
        self.update_button_texts()
        self._set_inspector_icon()
    
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
    
    def open_dev_tools(self):
        """Открывает инструменты разработчика"""
        try:
            # Отключаем Inspector Mode если он активен
            if hasattr(self, 'inspector_mode') and self.inspector_mode:
                self.disable_inspector_mode()
                self.inspector_mode = False
                self.inspector_button.setChecked(False)
            
            # Переключаем состояние DevTools
            if hasattr(self, 'dev_tools_visible') and self.dev_tools_visible:
                self.close_dev_tools()
            else:
                self.show_dev_tools()
        except Exception as e:
            print(f"Ошибка при работе с DevTools: {e}")
    
    def show_dev_tools(self):
        """Показывает DevTools в правой панели"""
        if not hasattr(self, 'dev_tools_visible') or not self.dev_tools_visible:
            from PyQt6.QtWidgets import QSplitter
            from PyQt6.QtCore import Qt
            
            # Создаем вертикальный разделитель для браузера
            main_splitter = QSplitter(Qt.Orientation.Vertical)
            
            # Верхняя часть - основной браузер
            main_splitter.addWidget(self.web_view)
            
            # Нижняя часть - DevTools
            self.dev_tools_view = QWebEngineView()
            main_splitter.addWidget(self.dev_tools_view)
            
            # Настраиваем DevTools
            self.web_view.page().setDevToolsPage(self.dev_tools_view.page())
            
            # Устанавливаем пропорции (браузер сверху больше, DevTools снизу меньше)
            main_splitter.setSizes([400, 200])
            
            # Заменяем основной виджет на разделитель
            layout = self.layout()
            # Удаляем старый web_view из layout
            layout.removeWidget(self.web_view)
            # Добавляем новый splitter
            layout.addWidget(main_splitter)
            
            self.dev_tools_visible = True
            
            # Отключаем JavaScript предупреждения
            self.web_view.page().runJavaScript("""
                // Отключаем предупреждения о deprecated свойствах
                const originalConsoleWarn = console.warn;
                console.warn = function(message) {
                    if (!message.includes('inset-area') && !message.includes('position-area')) {
                        originalConsoleWarn.apply(console, arguments);
                    }
                };
            """)
    
    def close_dev_tools(self):
        """Скрывает DevTools"""
        if hasattr(self, 'dev_tools_visible') and self.dev_tools_visible:
            # Возвращаем обычный браузер без DevTools
            layout = self.layout()
            
            # Находим и удаляем splitter
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QSplitter):
                    layout.removeWidget(widget)
                    widget.deleteLater()
                    break
            
            # Добавляем обратно основной браузер
            layout.addWidget(self.web_view)
            
            # Очищаем DevTools
            if hasattr(self, 'dev_tools_view'):
                self.dev_tools_view.deleteLater()
                delattr(self, 'dev_tools_view')
            
            # Отключаем связь с DevTools
            self.web_view.page().setDevToolsPage(None)
            
            self.dev_tools_visible = False
    
    def reload_page(self):
        """Перезагружает текущую страницу"""
        self.web_view.reload()
    
    def _set_inspector_icon(self):
        """Устанавливает иконку для кнопки инспектора"""
        import os
        from ..core.theme_manager import _THEME
        
        # Определяем папку с иконками в зависимости от темы
        theme_folder = "light_theme" if _THEME.is_light_theme() else "dark_theme"
        icon_path = os.path.join(_THEME.icons_base_path, theme_folder, "InspectorMode.png")
        
        # Если иконка не найдена, используем fallback
        if not os.path.exists(icon_path):
            fallback_folder = "dark_theme" if _THEME.is_light_theme() else "light_theme"
            icon_path = os.path.join(_THEME.icons_base_path, fallback_folder, "InspectorMode.png")
        
        # Устанавливаем иконку или текст, если иконка не найдена
        if os.path.exists(icon_path):
            self.inspector_button.setIcon(QIcon(icon_path))
            self.inspector_button.setText("")
        else:
            self.inspector_button.setText("🔍")
            self.inspector_button.setIcon(QIcon())
    
    def toggle_inspector_mode(self):
        """Переключает режим инспектора"""
        self.inspector_mode = not self.inspector_mode
        
        if self.inspector_mode:
            self.enable_inspector_mode()
        else:
            self.disable_inspector_mode()
        
        # Обновляем состояние кнопки
        self.inspector_button.setChecked(self.inspector_mode)
    
    def enable_inspector_mode(self):
        """Включает режим инспектора"""
        # Отключаем DevTools если они открыты
        if hasattr(self, 'dev_tools_visible') and self.dev_tools_visible:
            self.close_dev_tools()
        
        # Включаем режим инспектора
        self.web_view.page().setDevToolsPage(None)
        
        # Добавляем JavaScript для режима инспектора
        self.web_view.page().runJavaScript("""
            // Удаляем старые стили и обработчики если они есть
            const oldStyle = document.getElementById('inspector-mode-style');
            if (oldStyle) {
                oldStyle.remove();
            }
            
            // Добавляем CSS для подсветки элементов
            const style = document.createElement('style');
            style.id = 'inspector-mode-style';
            style.innerHTML = `
                .inspector-highlight {
                    outline: 2px solid #00a6ff !important;
                    outline-offset: 2px !important;
                    background-color: rgba(0, 166, 255, 0.1) !important;
                    cursor: crosshair !important;
                }
            `;
            document.head.appendChild(style);
            
            let highlightedElement = null;
            
            // Функция для получения информации об элементе
            function getElementInfo(element) {
                const rect = element.getBoundingClientRect();
                const computedStyle = window.getComputedStyle(element);
                
                return {
                    tagName: element.tagName,
                    id: element.id || 'none',
                    className: element.className || 'none',
                    text: element.textContent ? element.textContent.substring(0, 50) + '...' : 'none',
                    position: {
                        x: Math.round(rect.left),
                        y: Math.round(rect.top),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    },
                    styles: {
                        backgroundColor: computedStyle.backgroundColor,
                        color: computedStyle.color,
                        fontSize: computedStyle.fontSize,
                        fontFamily: computedStyle.fontFamily
                    }
                };
            }
            
            // Функция для подсветки элемента
            function highlightElement(element) {
                if (highlightedElement) {
                    highlightedElement.classList.remove('inspector-highlight');
                }
                
                element.classList.add('inspector-highlight');
                highlightedElement = element;
            }
            
            // Функция для скрытия подсветки
            function hideHighlight() {
                if (highlightedElement) {
                    highlightedElement.classList.remove('inspector-highlight');
                    highlightedElement = null;
                }
            }
            
            // Обработчик движения мыши
            document.addEventListener('mouseover', function(e) {
                if (e.target !== document.body && e.target !== document.documentElement) {
                    highlightElement(e.target);
                }
            });
            
            // Обработчик клика
            document.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const info = getElementInfo(e.target);
                
                // Отправляем информацию в Python консоль через специальный сигнал
                window.inspectorElementClicked = {
                    tagName: info.tagName,
                    id: info.id,
                    className: info.className,
                    text: e.target.textContent,
                    position: info.position,
                    styles: info.styles,
                    html: e.target.outerHTML
                };
                
                // Вызываем Python функцию для отключения режима инспектора
                window.inspectorModeDisable = true;
            });
            
            // Обработчик выхода из элемента
            document.addEventListener('mouseout', function(e) {
                // Небольшая задержка, чтобы подсветка не мигала
                setTimeout(() => {
                    if (!document.querySelector('.inspector-highlight:hover')) {
                        hideHighlight();
                    }
                }, 100);
            });
            
            console.log('Inspector Mode включен. Наведите мышь на элементы для их подсветки, кликните для получения информации.');
        """)
        
        print("Inspector Mode включен")
        
        # Запускаем проверку на клик
        self._start_inspector_click_check()
    
    def disable_inspector_mode(self):
        """Отключает режим инспектора"""
        # Удаляем JavaScript для режима инспектора
        self.web_view.page().runJavaScript("""
            // Удаляем стили
            const inspectorStyle = document.getElementById('inspector-mode-style');
            if (inspectorStyle) {
                inspectorStyle.remove();
            }
            
            // Убираем подсветку со всех элементов
            const highlightedElements = document.querySelectorAll('.inspector-highlight');
            highlightedElements.forEach(el => {
                el.classList.remove('inspector-highlight');
            });
            
            // Очищаем глобальные переменные
            window.inspectorElementClicked = null;
            window.inspectorModeDisable = false;
            
            console.log('Inspector Mode отключен');
        """)
        
        print("Inspector Mode отключен")
    
    def _start_inspector_click_check(self):
        """Запускает проверку на клик в режиме инспектора"""
        from PyQt6.QtCore import QTimer
        
        def check_click():
            if self.inspector_mode:
                # Проверяем, был ли клик
                self.web_view.page().runJavaScript("window.inspectorElementClicked", self._handle_inspector_click)
                # Проверяем, нужно ли отключить режим
                self.web_view.page().runJavaScript("window.inspectorModeDisable", self._handle_inspector_disable)
                
                # Продолжаем проверку
                QTimer.singleShot(100, check_click)
        
        # Запускаем проверку
        QTimer.singleShot(100, check_click)
    
    def _handle_inspector_click(self, result):
        """Обрабатывает клик в режиме инспектора"""
        if result and isinstance(result, dict):
            print("\n" + "="*50)
            print("ELEMENT INSPECTOR")
            print("="*50)
            print(f"Tag: {result.get('tagName', 'N/A')}")
            print(f"ID: {result.get('id', 'N/A')}")
            print(f"Class: {result.get('className', 'N/A')}")
            print(f"Text: {result.get('text', 'N/A')[:100]}...")
            print(f"Position: x={result.get('position', {}).get('x', 'N/A')}, y={result.get('position', {}).get('y', 'N/A')}")
            print(f"Size: {result.get('position', {}).get('width', 'N/A')}x{result.get('position', {}).get('height', 'N/A')}")
            print(f"HTML: {result.get('html', 'N/A')[:200]}...")
            print("="*50 + "\n")
            
            # Очищаем результат клика
            self.web_view.page().runJavaScript("window.inspectorElementClicked = null")
    
    def _handle_inspector_disable(self, result):
        """Обрабатывает команду отключения режима инспектора"""
        if result:
            # Отключаем режим инспектора
            self.inspector_mode = False
            self.inspector_button.setChecked(False)
            self.disable_inspector_mode()
            
            # Очищаем флаг отключения
            self.web_view.page().runJavaScript("window.inspectorModeDisable = false")
