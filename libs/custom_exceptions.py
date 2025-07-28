"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

from typing import Any
import traceback
from colorama import Fore, Style

class DataProcessingIssue(Exception):
    """
        Custom exception for data processing issues
    """
    def __init__(self, arg: Any = ""):
        print(Fore.RED)
        traceback.print_stack(limit=5)
        print(Style.RESET_ALL)
        self.arg: Any = arg