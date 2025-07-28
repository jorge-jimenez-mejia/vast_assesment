"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

from dataclasses import dataclass, field
from truck import Truck

@dataclass
class UnloadStation:
    """
        unloading station object
    """
    id: int
    busy: bool = False
    free_at_time: int = 0
    queue: list[Truck] = field(default_factory=list)
