from typing import Dict, Any
from .config_loader import load_localization


class TextManager:
    
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
        language_data = self.localization.get(self.current_language, {})
        translated_text = language_data.get(text_id)
        
        if translated_text:
            return translated_text
        
        if self.current_language != "ru":
            ru_data = self.localization.get("ru", {})
            translated_text = ru_data.get(text_id)
            if translated_text:
                return translated_text
        
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
        
        try:
            return text.format(**params)
        except (KeyError, ValueError):
            return text
    
    def has_text(self, text_id: str) -> bool:
        """
        Проверяет, есть ли текст с данным ID.
        
        Args:
            text_id: ID текста
            
        Returns:
            True если текст найден
        """
        language_data = self.localization.get(self.current_language, {})
        if text_id in language_data:
            return True
        
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
        self.localization = load_localization()


_TEXT_MANAGER = TextManager()
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
