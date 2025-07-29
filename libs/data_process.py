"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import numpy as np
from libs.truck import TruckDataCollection

class SimDataProcess():

    def __init__(self, data_sets: list[TruckDataCollection]) -> None:
        
        self.data_sets = data_sets

    def process(self) -> None:
        pass

    def get_total_minutes_driving(self) -> tuple[int, int, int]:
        """
        Method to get overall min/max/average

        Returns:
            tuple[int, int, int]: min/max/average
        """

        min_time: int = min(data.traveling_time for data in self.data_sets)
        max_time: int = max(data.traveling_time for data in self.data_sets)
        ave_time: int = sum(data.traveling_time for data in self.data_sets)

        return min_time, max_time, ave_time


# numbers = np.array([10, 20, 30, 40, 50])
# average = np.mean(numbers)
# print(average)

    # completed_trips: int = 0
    # traveling_time: int = 0
    # mining_time: list[float] = field(default_factory=list)
    # time_waiting_to_drop_off: list[float] = field(default_factory=list)