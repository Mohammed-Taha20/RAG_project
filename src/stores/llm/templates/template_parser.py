import os
import logging
from typing import Self

class template_parser:
    def __init__(self, language : str , Default_lang:str = "en"):

        self.language = None
        self.Default_lang=Default_lang
        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.set_language(language)
        
        self.logger = logging.getLogger(__name__)

    def set_language(self, language: str):
        self.language = language
        if not language:
            self.language = self.Default_lang

        

        lang_folder = os.path.join(self.current_folder, "locales", self.language)

        if not os.path.exists(lang_folder):
            lang_folder = os.join(self.current_folder,"locales", self.Default_lang)
            if not os.path.exists(lang_folder):
                Self.logger.error(f"Language folder not found for {self.language} or {self.Default_lang}")

    
    def get(self, group :str , key:str , vars:dict = {}):
        try:
            file_path = os.path.join(self.current_folder, "locales", self.language, f"{group}.py")
            targeted_lang  = self.language
            if not os.path.exists(file_path):
                file_path = os.path.join(self.current_folder, "locales", self.Default_lang, f"{group}.py")
                targeted_lang = self.Default_lang
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Template file not found for group '{group}' in language '{self.language}' or default '{self.Default_lang}'.")

            module = __import__(f"stores.llm.templates.locales.{self.language}.{group}", fromlist=[group])
            template = getattr(module, key)
            return template.substitute(vars)
        except Exception as e:
            self.logger.error(f"Error retrieving template: {e}")
            return None

    