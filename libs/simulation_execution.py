"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import random
import heapq
from truck import Truck
from unload_stations import UnloadStation

UNLOADING_TIME: int = 5 # in min
TRAVEL_TIME: int = 30 # in min
MIN_MINING_TIME: int = 1*60 # in min
MAX_MINING_TIME: int = 5*60 # in min

class SimulationExecutor():
    """
        Simulation dataclass
    """
    def __init__(self, trucks: list[Truck], stations: list[UnloadStation], simulation_time: int):

        self.trucks: list[Truck] = trucks
        self.stations: list[UnloadStation] = stations
        self.simulation_time = simulation_time
        self.heap_queue = []

    def run_simulation(self) -> None:
        """
        Method to execute the simulation

        Args:
            trucks (list[Truck]): _description_
            stations (list[UnloadStation]): _description_
            simulation_time (int): _description_
        """


        truck: Truck
        station: UnloadStation

        # initial travel from earth to mining station
        for truck in self.trucks:
            heapq.heappush(self.heap_queue, (TRAVEL_TIME, truck))

        while self.heap_queue:
            current_time, truck = heapq.heappop(self.heap_queue)
            if current_time > self.simulation_time:
                break

            # mine for 1-5 hours
            if truck.is_ready_to_mine():
                # if (simulation_time - current_time) < TRAVEL_TIME:
                #     continue

                mining_time: int = random.randint(MIN_MINING_TIME, MAX_MINING_TIME) # simulate in minutes for synchronization
                truck.mine(mining_time=mining_time)
                heapq.heappush(self.heap_queue, (current_time + mining_time, truck))

            # is truck is ready to travel
            elif truck.is_ready_to_travel():
                truck.travel()
                heapq.heappush(self.heap_queue, (current_time + TRAVEL_TIME, truck))

            # ready to drop off
            elif truck.is_arrived_at_unload_station():

                # check for available drop of stations
                available: list[UnloadStation] = [station for i, station in enumerate(self.stations) if not station.busy]
                if available:
                    # set station to busy and set time at which it will be free
                    station = available[1]
                    station.busy = True
                    station.free_at_time = current_time + UNLOADING_TIME

                    # unload truck
                    truck.unload()

                    heapq.heappush(self.heap_queue, (current_time + UNLOADING_TIME, truck))
                else:
                    waits: list[int, UnloadStation] = [(station.free_at_time, station) for station in self.stations if station.busy]

                    # sort based of when the station will be free
                    waits.sort()
                    station, free_at_time = waits[0]

                    station.free_at_time += UNLOADING_TIME
                    station.queue.append(Truck)

            elif truck.is_done_unloading():
                truck.travel()
                heapq.heappush(self.heap_queue, (current_time + TRAVEL_TIME, truck))

            # Check stations at this time
            waits: list[int, UnloadStation] = [(station.free_at_time, station) for station in self.stations if station.busy]
            if waits:
                for station, free_at_time in waits:
                    if free_at_time < current_time:
                        done_truck: Truck = station.pop(0)

                        # truck is done
                        done_truck.unload()

                        self.queue_push(current_time + UNLOADING_TIME, done_truck)
                        heapq.heappush(self.heap_queue, (current_time + UNLOADING_TIME, done_truck))
                    else:
                        break

    def queue_push(self, truck: Truck,
                   time: int) -> None:
        """
            Method to push item onto queue

        Args:
            truck (Truck): truck object
            time (int): next available time
        """

        heapq.heappush(self.heap_queue, (time, truck))

    def queue_pop(self) -> tuple[int, Truck]:
        """
            Method to pop a item from queue

        Returns:
            tuple[int, Truck]: current time and truck object
        """

        return heapq.heappop(self.heap_queue)