"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

from dataclasses import dataclass, field

@dataclass
class TruckDataCollection:
    """
        Dataclass for truck data collection
    """
    # data collection
    completed_trips: int = 0
    traveling_time: int = 0
    mining_time: list[float] = field(default_factory=list)
    time_waiting_to_drop_off: list[float] = field(default_factory=list)

class Truck:
    """
        Class for truck event driven behavior
    """

    def __init__(self, identification: int) -> None:
        # initialize truck
        self.id: int = identification
        self.travel_done: bool = False
        self.loaded: bool = False
        self.waiting_for_station: bool = False

        # initialize data gathering dataclass
        self.truck_data: TruckDataCollection = TruckDataCollection()

############################### Truck Actions ###############################

    def mine(self, mining_time: int) -> None:

        self.loaded = True
        self.travel_done = False

        # include data for analysis
        self.truck_data.mining_time.append(mining_time)

    def travel(self) -> None:

        self.travel_done = True

        # include data for analysis
        self.truck_data.traveling_time += 30 # min

    def wait_for_open_station(self, waiting_time: int) -> None:

        self.waiting_for_station = True

        # include data for analysis
        self.truck_data.time_waiting_to_drop_off.append(waiting_time)

    def unload(self) -> None:

        self.travel_done = False
        self.loaded = False

        # include data for analysis
        self.truck_data.completed_trips += 1

############################### get Truck states ###############################

    def is_ready_to_mine(self) -> bool:

        return (not self.loaded and self.travel_done)

    def is_ready_to_travel(self) -> bool:

        return not self.travel_done

    def is_arrived_at_unload_station(self) -> bool:

        return self.loaded and self.travel_done

    def is_done_unloading(self) -> bool:

        return (not self.loaded and not self.travel_done)

############################### generic functions ###############################

    def get_data(self) -> TruckDataCollection:
        """
            Method to get truck data

        Returns:
            TruckDataCollection: truck data collections object
        """

        return self.truck_data