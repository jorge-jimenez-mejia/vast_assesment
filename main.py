"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import sys
import os
import time
import argparse
import textwrap
from libs.truck import TruckDataCollection
from libs.truck import Truck
from libs.unload_stations import UnloadStation
from libs.simulation_execution import SimulationExecutor
from libs.data_process import SimDataProcess
from libs.logger_lib import logger

SIMULATION_TIME: int = 72*60 # hours
USE_STRING: str = """USAGE:
python3 main.py -n <number of mining trucks> -m <number of mining unload stations>
            """

# INPUTS:
# n is number of mining trucks
# m is number of mining unload stations
# gathering stations are unlimited

# NOTES:
# 5 minutes to unload
# 30 minutes to travel from mining site and unloading station
# 1 to 5 hours random for trucks to load at mining stations

# If all unloading stations, trucks are queued to the station with the shortest wait

def main(number_trucks: int, number_stations: int) -> None:
    """
        Method to execute mining simulation

    Args:
        number_trucks (int): number of mining trucks
        number_stations (int): number of mining unloading stations
    """

    print(f"Simulating {SIMULATION_TIME} hours for {number_trucks} trucks and {number_stations} unloading stations")

    # Initialize trucks
    trucks: list[Truck] = [Truck(i) for i in range(1, number_trucks+1)]

    # initialize unloading stations
    stations: list[UnloadStation] = [UnloadStation(identification=i+1) for i in range(number_stations)]

    for station in stations:
        station.queue = []

    # run simulation
    sim_obj: SimulationExecutor = SimulationExecutor(trucks=trucks,
                                                 stations=stations,
                                                 simulation_time=SIMULATION_TIME)
    sim_obj.run_simulation()

    print("simulation ended")


    # get data
    data_objects: list[TruckDataCollection] = [truck.truck_data for truck in trucks]
    process_object: SimDataProcess = SimDataProcess(data_objects)
    process_object.process()
    process_object.get_total_minutes_driving()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            epilog=textwrap.dedent(USE_STRING),)
    parser.add_argument("--trucks", "-n", type=int, help="number of mining trucks")
    parser.add_argument("--stations", "-m", type=int, help="number of mining unloading stations")

    args = parser.parse_args()
    # verify required parameters are passed to main file
    if not args.trucks or not args.stations:
        print("Ensure that -n and -m parameters are passed")
        sys.exit(-1)

    start_time = time.time()
    main(number_trucks=args.trucks, number_stations=args.stations)
    print(f"Execution time: {time.time()-start_time}")
    
