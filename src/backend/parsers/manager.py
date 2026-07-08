import os
from typing import Dict, Type, Optional
from src.backend.parsers.base import BaseParser

class ParserManager:
    """
    Factory class that routes document files to their respective BaseParser adapters.
    """
    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {}
