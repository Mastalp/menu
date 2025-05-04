# core/__init__.py

# Expose the main interfaces and classes for easy imports
from .interfaces import IMenuTemplate, ITranslator, IProgressBar
from .template   import ConfiguredMenuTemplate, TemplateFactory
from .translator import GoogleTranslator

__all__ = [
    "IMenuTemplate", "ITranslator", "IProgressBar",
    "ConfiguredMenuTemplate", "TemplateFactory",
    "GoogleTranslator"
]

from .menuFiller import MenuFiller

__all__ += ["MenuFiller"]
