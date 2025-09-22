"""
Менеджер текстов приложения.

Обеспечивает централизованное управление текстами через ID,
автоматический перевод через файл локализации.
"""
from typing import Dict, Any
from .config_loader import load_localization


class TextManager:
    """
    Класс для управления текстами приложения через ID.
    
    Основные функции:
    - Получение текстов по ID из файла локализации
    - Автоматический перевод на текущий язык
    - Fallback на ID если перевод не найден
    """
    
    def __init__(self, language: str = "ru"):
        """
        Инициализация менеджера текстов.
        
        Args:
            language: Язык интерфейса по умолчанию
        """
        self.current_language = language
        self.localization = load_localization()
    
    def set_language(self, language: str):
        """
        Устанавливает текущий язык.
        
        Args:
            language: Код языка (ru, en)
        """
        self.current_language = language
    
    def get_current_language(self) -> str:
        """
        Возвращает текущий язык.
        
        Returns:
            Код текущего языка
        """
        return self.current_language
    
    def get_text(self, text_id: str) -> str:
        """
        Получает текст по ID из файла локализации.
        
        Args:
            text_id: ID текста
            
        Returns:
            Переведенный текст или сам ID если перевод не найден
        """
        # Получаем переводы для текущего языка
        language_data = self.localization.get(self.current_language, {})
        
        # Ищем текст по ID
        translated_text = language_data.get(text_id)
        
        if translated_text:
            return translated_text
        
        # Если перевод не найден, пробуем русский как fallback
        if self.current_language != "ru":
            ru_data = self.localization.get("ru", {})
            translated_text = ru_data.get(text_id)
            if translated_text:
                return translated_text
        
        # Если нигде не найден, возвращаем сам ID
        return text_id
    
    def get_text_with_params(self, text_id: str, **params) -> str:
        """
        Получает текст по ID и подставляет параметры.
        
        Args:
            text_id: ID текста
            **params: Параметры для подстановки в текст
            
        Returns:
            Переведенный текст с подставленными параметрами
        """
        text = self.get_text(text_id)
        
        # Подставляем параметры в текст
        try:
            return text.format(**params)
        except (KeyError, ValueError):
            # Если не удалось подставить параметры, возвращаем исходный текст
            return text
    
    def has_text(self, text_id: str) -> bool:
        """
        Проверяет, есть ли текст с данным ID.
        
        Args:
            text_id: ID текста
            
        Returns:
            True если текст найден
        """
        # Проверяем в текущем языке
        language_data = self.localization.get(self.current_language, {})
        if text_id in language_data:
            return True
        
        # Проверяем в русском как fallback
        if self.current_language != "ru":
            ru_data = self.localization.get("ru", {})
            if text_id in ru_data:
                return True
        
        return False
    
    def get_all_texts_for_language(self, language: str = None) -> Dict[str, str]:
        """
        Возвращает все тексты для указанного языка.
        
        Args:
            language: Код языка. Если None, используется текущий язык
            
        Returns:
            Словарь {ID: текст} для указанного языка
        """
        if language is None:
            language = self.current_language
        
        return self.localization.get(language, {})
    
    def reload_localization(self):
        """Перезагружает файл локализации."""
        self.localization = load_localization()


# Глобальный экземпляр менеджера текстов
_TEXT_MANAGER = TextManager()


# Функции для быстрого доступа
def get_text(text_id: str) -> str:
    """
    Получает текст по ID.
    
    Args:
        text_id: ID текста
        
    Returns:
        Переведенный текст или ID
    """
    return _TEXT_MANAGER.get_text(text_id)


def get_text_with_params(text_id: str, **params) -> str:
    """
    Получает текст по ID с параметрами.
    
    Args:
        text_id: ID текста
        **params: Параметры для подстановки
        
    Returns:
        Переведенный текст с параметрами
    """
    return _TEXT_MANAGER.get_text_with_params(text_id, **params)


def set_language(language: str):
    """
    Устанавливает текущий язык.
    
    Args:
        language: Код языка
    """
    _TEXT_MANAGER.set_language(language)


def get_current_language() -> str:
    """
    Возвращает текущий язык.
    
    Returns:
        Код текущего языка
    """
    return _TEXT_MANAGER.get_current_language()


def has_text(text_id: str) -> bool:
    """
    Проверяет наличие текста по ID.
    
    Args:
        text_id: ID текста
        
    Returns:
        True если текст найден
    """
    return _TEXT_MANAGER.has_text(text_id)
