"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

from dataclasses import dataclass, field


UNLOADING_TIME: int = 5 # in min
TRAVEL_TIME: int = 30 # in min
MIN_MINING_TIME: int = 1*60 # in min
MAX_MINING_TIME: int = 5*60 # in min

@dataclass
class TruckDataCollection:
    """
        Dataclass for truck data collection
    """
    # data collection
    truck_id: int
    completed_trips: int = 0
    traveling_time: int = 0
    unloading_time: int = 0
    mining_time: list[float] = field(default_factory=list)

class Truck:
    """
        Class for truck event driven behavior
    """

    def __init__(self, identification: int) -> None:
        # initialize truck
        self.id: int = identification
        self.loaded: bool = False
        self.travel_done: bool = False
        self.unloading_site: int = 0

        # initialize data gathering dataclass
        self.truck_data: TruckDataCollection = TruckDataCollection(truck_id=identification)

############################### Truck Actions ###############################

    def mine(self, mining_time: int) -> None:
        """
            Method to change to Mining state

        Args:
            mining_time (int): time taken to mine
        """

        self.loaded = True
        self.travel_done = False

        # include data for analysis
        self.truck_data.mining_time.append(mining_time)

    def travel(self) -> None:
        """
            Method to change to travel state
        """

        self.travel_done = True

        # include data for analysis
        self.truck_data.traveling_time += 30 # min

    def unload(self) -> None:
        """
            Method to change to unloading state
        """
        self.travel_done = False
        self.loaded = False
        self.unloading_site = 0

        # data collection
        self.truck_data.completed_trips += 1
        self.truck_data.unloading_time += UNLOADING_TIME

############################### get Truck states ###############################

    def ready_to_mine(self) -> bool:
        """
            Method to check if truck is ready for mine state

        Returns:
            bool: true to read, false for not ready
        """

        return (not self.loaded and self.travel_done)

    def ready_to_travel(self) -> bool:
        """
            Method to check if truck is ready for travel state

        Returns:
            bool: true to read, false for not ready
        """

        return not self.travel_done

    def arrived_at_unload_station(self) -> bool:
        """
            Method to check if truck arrived at mining unload state

        Returns:
            bool: true to read, false for not ready
        """

        return self.loaded and self.travel_done

    def done_unloading(self) -> bool:
        """
            Method to check if truck is done unloading

        Returns:
            bool: true to read, false for not ready
        """

        return (not self.loaded and not self.travel_done)
