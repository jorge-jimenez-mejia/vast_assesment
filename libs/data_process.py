"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import csv
from typing import Any
from libs.truck import TruckDataCollection
from libs.unload_stations import UnloadStation
from libs.simulation_execution import UNLOADING_TIME

class SimDataProcess():

    def __init__(self, truck_data_sets: list[TruckDataCollection],
                station_data_sets: list[UnloadStation],
                simulation_time: int) -> None:

        self.truck_data_sets: list[TruckDataCollection] = truck_data_sets
        self.station_data_sets: list[UnloadStation] = station_data_sets
        self.simulation_time: int = simulation_time

    def process_and_write_data(self, display_data: bool = False) -> None:
        """
            Method to write processed data to CSV
        """
        truck_data: list[dict[str, Any]] = self.compute_truck_stats()
        station_data: list[dict[str, Any]] = self.compute_station_stats()

        self.write_csv(truck_data, "sim_truck_stats.csv")
        self.write_csv(station_data, "sim_station_stats.csv")

        if display_data:
            self.print_summary(station_data=station_data,
                               truck_data=truck_data)

    def compute_truck_stats(self) -> list[dict[str, Any]]:
        """
        Method to calculate statistics about mining truck

        Returns:
            list[dict[str, Any]]: list of dictionaries for CVS write
        """

        results = []
        truck: TruckDataCollection
        for truck in self.truck_data_sets:

            # calculate total mining time
            total_mining = sum(truck.mining_time)

            # calculate total working time per truck
            total_work_time = truck.traveling_time + truck.unloading_time + total_mining

            # calculate average trip time
            avg_trip_time = (total_work_time / truck.completed_trips) if truck.completed_trips > 0 else 0

            # calculate total truck utilization
            utilization = (total_work_time / self.simulation_time * 100) if self.simulation_time > 0 else 0

            # calculate max idle time
            idle_time = max(0, self.simulation_time - total_work_time)

            # append to list
            results.append({
                "truck_id": truck.truck_id,
                "completed_trips": truck.completed_trips,
                "avg_trip_time [min]": round(avg_trip_time, 3),
                "utilization_percent [%]": round(utilization, 3),
                "idle_time [min]": idle_time,
                "total_mining_time [min]": round(total_mining, 3),
            })

        return results

    def compute_station_stats(self) -> list[dict[str, Any]]:
        """
        Method to calculate statistics about mining unloads stations

        Returns:
            list[dict[str, Any]]: list of dictionaries for CVS write
        """
        results = []
        station: UnloadStation
        for station in self.station_data_sets:

            # calculate total time station busy
            busy_time = station.total_unloads * UNLOADING_TIME
            
            # calculate % utilization
            utilization = (busy_time / self.simulation_time * 100) if self.simulation_time > 0 else 0

            # calculate idle time
            idle_time = self.simulation_time - station.total_unloads*UNLOADING_TIME

            # append to list
            results.append({
                "station_id": station.identification,
                "total_unloads": station.total_unloads,
                "idle_time [min]": idle_time,
                "utilization_percent [%]": round(utilization, 3),
                "max_queue_length": station.max_queue_length,
                "final_queue_length": len(station.queue),
            })

        return results

    def write_csv(self, data: list[dict[str, Any]], filename: str) -> None:
        """
            Method to write data to CSV

        Args:
            data (list[dict[str, Any]]): data to write
            filename (str): CSV filename
        """

        with open(filename, "w", newline="", encoding="utf-8") as f_station:
            writer = csv.DictWriter(f_station, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def print_summary(self, truck_data: list[dict[str, Any]],
                      station_data: list[dict[str, Any]]):
        """
            Method to display data and log to file
        """

        print("==============================\tTruck Stats\t==============================")
        data: dict[str, Any]
        for data in truck_data:
            print(data)

        print("\n==============================\tStation Stats\t==============================")
        for data in station_data:
            print(data)