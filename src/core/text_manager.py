"""
Менеджер текстов и локализации

Обеспечивает получение текстов по ID с поддержкой многоязычности.
Если текст не найден в файле локализации, возвращает сам ID.
"""
from typing import Dict, Optional
from .config_loader import load_localization


class TextManager:
    """
    Менеджер для управления текстами и локализацией.
    
    Основные функции:
    - Получение текстов по ID
    - Поддержка многоязычности
    - Автоматическое использование ID как fallback
    """
    
    def __init__(self, default_language: str = "ru"):
        """
        Инициализация менеджера текстов.
        
        Args:
            default_language: Язык по умолчанию
        """
        self.current_language = default_language
        self.localization_data = load_localization()
    
    def set_language(self, language: str) -> None:
        """
        Устанавливает текущий язык.
        
        Args:
            language: Код языка (ru, en, etc.)
        """
        self.current_language = language
    
    def get_text(self, text_id: str, language: Optional[str] = None) -> str:
        """
        Получает текст по ID для текущего языка.
        
        Args:
            text_id: Идентификатор текста
            language: Язык (если None, используется текущий)
            
        Returns:
            Текст на указанном языке или сам ID если не найден
        """
        if language is None:
            language = self.current_language
        
        # Получаем данные для указанного языка
        language_data = self.localization_data.get(language, {})
        
        # Ищем текст по ID
        text = language_data.get(text_id)
        
        # Если текст найден, возвращаем его
        if text is not None:
            return text
        
        # Если не найден, возвращаем сам ID
        return text_id
    
    def get_all_texts(self, language: Optional[str] = None) -> Dict[str, str]:
        """
        Получает все тексты для указанного языка.
        
        Args:
            language: Язык (если None, используется текущий)
            
        Returns:
            Словарь с текстами
        """
        if language is None:
            language = self.current_language
        
        return self.localization_data.get(language, {})
    
    def get_available_languages(self) -> list:
        """
        Получает список доступных языков.
        
        Returns:
            Список кодов языков
        """
        return list(self.localization_data.keys())
    
    def has_text(self, text_id: str, language: Optional[str] = None) -> bool:
        """
        Проверяет, существует ли текст с указанным ID.
        
        Args:
            text_id: Идентификатор текста
            language: Язык (если None, используется текущий)
            
        Returns:
            True если текст существует
        """
        if language is None:
            language = self.current_language
        
        language_data = self.localization_data.get(language, {})
        return text_id in language_data


# Глобальный экземпляр менеджера текстов
_TEXT_MANAGER = TextManager()


# Функции для удобного доступа
def get_text(text_id: str, language: Optional[str] = None) -> str:
    """
    Получает текст по ID.
    
    Args:
        text_id: Идентификатор текста
        language: Язык (если None, используется текущий)
        
    Returns:
        Текст на указанном языке или сам ID если не найден
    """
    return _TEXT_MANAGER.get_text(text_id, language)


def set_language(language: str) -> None:
    """
    Устанавливает текущий язык.
    
    Args:
        language: Код языка (ru, en, etc.)
    """
    _TEXT_MANAGER.set_language(language)


def get_current_language() -> str:
    """
    Получает текущий язык.
    
    Returns:
        Код текущего языка
    """
    return _TEXT_MANAGER.current_language


def get_available_languages() -> list:
    """
    Получает список доступных языков.
    
    Returns:
        Список кодов языков
    """
    return _TEXT_MANAGER.get_available_languages()
