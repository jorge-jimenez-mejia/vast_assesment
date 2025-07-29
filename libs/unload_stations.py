"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

from dataclasses import dataclass, field
from libs.truck import Truck

@dataclass
class UnloadStation:
    """
        unloading station object
    """
    identification: int = 0
    free_at_time: int = 0
    idle_time: int = 0
    total_unloads: int = 0
    max_queue_length: int = 0
    queue: list[Truck] = field(default_factory=list)
