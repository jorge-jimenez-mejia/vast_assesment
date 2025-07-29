"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import random
import heapq
from libs.logger_lib import logger
from libs.unload_stations import UnloadStation
from libs.truck import Truck, MAX_MINING_TIME, MIN_MINING_TIME, TRAVEL_TIME, UNLOADING_TIME

class SimulationExecutor():
    """
        Simulation dataclass
    """
    def __init__(self, trucks: list[Truck], stations: list[UnloadStation], simulation_time: int):

        self.trucks: list[Truck] = trucks
        self.stations: list[UnloadStation] = stations
        self.simulation_time = simulation_time
        self.heap_queue = []

        # initialization variables
        self.current_time = 0

    def run_simulation(self) -> None:
        """
        Method to execute the simulation

        Args:
            trucks (list[Truck]): list of Truck objects
            stations (list[UnloadStation]): list of unload mining stations
            simulation_time (int): expected simulation
        """

        truck: Truck

        # initial travel from earth to mining station
        for truck in self.trucks:
            self.queue_push(truck=truck, time=TRAVEL_TIME)

        while True:
            self.current_time, truck = self.queue_pop()
            logger.info("%s min - Truck [%s]: current time: %s", self.current_time, truck.id, self.current_time)
            if self.current_time >= self.simulation_time:
                logger.info("Simulation 72 hours done current time is %s", self.current_time/60)
                break

            # mine for 1-5 hours
            if truck.ready_to_mine():
                self.mine(truck)

            # is truck is ready to travel
            elif truck.ready_to_travel():
                self.travel(truck)

            # ready to drop off
            elif truck.arrived_at_unload_station():
                self.arrive_and_unload(truck)

            elif truck.done_unloading():
                self.finish_unload_and_restart(truck)

    def mine(self, truck: Truck) -> None:
        """
            Method to handle mining state logic

        Args:
            truck (Truck): truck object to act on
        """
        mining_time: int = random.randint(MIN_MINING_TIME, MAX_MINING_TIME) # simulate in minutes for synchronization

        logger.info("%s min - Truck [%s]: is ready to mine for %s", self.current_time, truck.id, mining_time)
        truck.mine(mining_time=mining_time)
        self.queue_push(truck=truck, time=self.current_time + mining_time)

    def travel(self, truck: Truck) -> None:
        """
            Method to handle travel logic

        Args:
            truck (Truck): truck object to act on
        """

        logger.info("%s min - Truck [%s]: is ready to travel", self.current_time, truck.id)
        truck.travel()
        self.queue_push(truck=truck, time=self.current_time + TRAVEL_TIME)


    def arrive_and_unload(self, truck: Truck) -> None:
        """
            Method to handle arrival at unloading site logic

        Args:
            truck (Truck): truck object to act on
        """

        logger.info("%s min - Truck [%s]: arrived at unload station", self.current_time, truck.id)

        station: UnloadStation

        # check for available drop of stations
        available: list[UnloadStation] = [(station.free_at_time, station.identification, station) for station in self.stations if self.current_time >= station.free_at_time]

        if available:
            available.sort()
            # set station to busy and set time at which it will be free
            _, _, station = available[0]

            station.free_at_time += UNLOADING_TIME

            # unload truck
            truck.unload()
            station.total_unloads += 1
            truck.unloading_site = station.identification
            logger.info("%s min - Truck [%s]: unloading at station: %s", self.current_time, truck.id, station.identification)

            self.queue_push(truck=truck, time=self.current_time + UNLOADING_TIME)
        else:
            waits: list[tuple[int, UnloadStation]] = [(station.free_at_time, len(station.queue), station.identification, station) for station in self.stations]
            # station = min(self.stations, key=lambda s: len(s.queue))

            # sort based of when the station will be free
            waits.sort()
            _, _, _, station = waits[0]

            logger.info("%s min - Truck [%s]: Stations busy, getting in line at station %s, trucks in line %s",
                        self.current_time,
                        truck.id,
                        station.identification,
                        len(station.queue))

            # configure ids, queues, states and free until time
            truck.unloading_site = station.identification
            station.queue.append(truck)
            # station.free_at_time += UNLOADING_TIME

            # update max queue lengths
            [setattr(station, "max_queue_length", len(station.queue)) for station in self.stations if len(station.queue) > station.max_queue_length]


    def finish_unload_and_restart(self, truck: Truck) -> None:
        """
            Method to handle mining unloading and restarting cycle

        Args:
            truck (Truck): truck object to act on
        """

        logger.info("%s min - Truck [%s]: is done unloading at station %s, heading to mining site",
                    self.current_time,
                    truck.id,
                    truck.unloading_site)
        truck.travel()
        self.queue_push(truck=truck, time=self.current_time + TRAVEL_TIME)

        # if this truck is done unloading, take it out of the station
        for station in self.stations:
            if truck.unloading_site == station.identification:
                if station.queue and self.current_time >= station.free_at_time:
                    next_in_line: Truck = station.queue.pop(0)
                    next_in_line.unloading_site = station.identification
                    next_in_line.unload()
                    station.total_unloads += 1
                    logger.info("%s min - Truck [%s]: is done unloading at station %s, heading to mining site",
                                self.current_time,
                                next_in_line.id,
                                next_in_line.unloading_site)

                    # set the station to busy again
                    station.free_at_time += UNLOADING_TIME
                    self.queue_push(truck=next_in_line, time=self.current_time + UNLOADING_TIME)


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
