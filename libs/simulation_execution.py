"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import random
import heapq
from libs.truck import Truck, MAX_MINING_TIME, MIN_MINING_TIME, TRAVEL_TIME, UNLOADING_TIME
from libs.unload_stations import UnloadStation
from libs.logger_lib import logger

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
            trucks (list[Truck]): list of Truck objects
            stations (list[UnloadStation]): list of unload mining stations
            simulation_time (int): expected simulation
        """

        truck: Truck
        station: UnloadStation

        # initial travel from earth to mining station
        for truck in self.trucks:
            self.queue_push(truck=truck, time=TRAVEL_TIME)

        while True:
            current_time, truck = self.queue_pop()
            logger.info("%s min - Truck [%s]: current time: %s", current_time, truck.id, current_time)
            if current_time >= self.simulation_time:
                logger.info("Simulation 72 hours done current time is %s", current_time/60)
                break

            # mine for 1-5 hours
            if truck.ready_to_mine():
                mining_time: int = random.randint(MIN_MINING_TIME, MAX_MINING_TIME) # simulate in minutes for synchronization

                # if (current_time + mining_time) > self.simulation_time:
                #     break

                logger.info("%s min - Truck [%s]: is ready to mine for %s", current_time, truck.id, mining_time)
                truck.mine(mining_time=mining_time)
                self.queue_push(truck=truck, time=current_time + mining_time)

            # is truck is ready to travel
            elif truck.ready_to_travel():
                logger.info("%s min Truck [%s]: is ready to travel", current_time, truck.id)
                truck.travel()
                self.queue_push(truck=truck, time=current_time + TRAVEL_TIME)

            # ready to drop off
            elif truck.arrived_at_unload_station():
                logger.info("%s min - Truck [%s]: arrived at unload station", current_time, truck.id)

                # check for available drop of stations
                available: list[UnloadStation] = [(station.free_at_time, station.identification, station) for station in self.stations if current_time > station.free_at_time]
                if available:
                    available.sort()
                    # set station to busy and set time at which it will be free
                    _, _, station = available[0]
                    station.free_at_time = station.free_at_time + UNLOADING_TIME

                    # unload truck
                    truck.unload()
                    # truck.unloading_site = station.identification
                    logger.info("%s min - Truck [%s]: unloading at station: %s", current_time, truck.id, station.identification)

                    self.queue_push(truck=truck, time=current_time + UNLOADING_TIME)
                else:
                    waits: list[int, UnloadStation] = [(station.free_at_time, station.identification, station) for station in self.stations]
                    # sort based of when the station will be free
                    waits.sort()

                    _, _, station = waits[0]
                    truck.unloading_site = station.identification
                    logger.info("%s min - Truck [%s]: Stations busy, getting in line at station %s, trucks in line %s",
                                current_time,
                                truck.id,
                                station.identification,
                                len(station.queue))
                    station.queue.append(truck)

                    # # truck data collection
                    # truck.truck_data.idle_time += station.queue - current_time 

            elif truck.done_unloading():
                logger.info("%s min - Truck [%s]: is done unloading at station %s, heading to mining site",
                            current_time,
                            truck.id,
                            truck.unloading_site)
                truck.travel()
                self.queue_push(truck=truck, time=current_time + TRAVEL_TIME)

                # if this truck is done unloading, take it out of the station
                if truck.unloading_site:
                    for station in self.stations:
                        if station.identification != truck.unloading_site:
                            continue
                    # station = self.stations[truck.unloading_site]
                    next_in_line: Truck = station.queue.pop(0)
                    next_in_line.unload()
                    logger.info("%s min - Truck [%s]: is done unloading at station %s, heading to mining site",
                                current_time,
                                next_in_line.id,
                                next_in_line.unloading_site)

                    # set the station to busy again
                    station.free_at_time = current_time + UNLOADING_TIME
                    self.queue_push(truck=next_in_line, time=current_time + UNLOADING_TIME)


    def queue_push(self, truck: Truck,
                   time: int) -> None:
        """
            Method to push item onto queue

        Args:
            truck (Truck): truck object
            time (int): next available time
        """

        heapq.heappush(self.heap_queue, (time, truck.id, truck))


    def queue_pop(self) -> tuple[int, Truck]:
        """
            Method to pop a item from queue

        Returns:
            tuple[int, Truck]: current time and truck object
        """

        items = heapq.heappop(self.heap_queue)
        return items[0], items[2]
