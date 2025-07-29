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

SIMULATION_TIME: int = 72*60 # hours
USE_STRING: str = """USAGE:
python3 main.py -n <number of mining trucks> -m <number of mining unload stations> [-v <print stats>]
            """

def main(number_trucks: int, number_stations: int, verbose: bool) -> None:
    """
    Method to execute mining simulation

    Args:
        number_trucks (int): number of mining trucks
        number_stations (int): number of mining unloading stations
        verbose (bool): verbose for printing stats at the end
    """

    print(f"Simulating {int(SIMULATION_TIME/60)} hours for {number_trucks} trucks and {number_stations} unloading stations")

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

    # get data onto list
    data_objects: list[TruckDataCollection] = [truck.truck_data for truck in trucks]

    # initialize object
    process_object: SimDataProcess = SimDataProcess(data_objects, stations, simulation_time=SIMULATION_TIME)

    # process and display/save data
    process_object.process_and_write_data(display_data=verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            epilog=textwrap.dedent(USE_STRING),)
    parser.add_argument("--trucks", "-n", type=int, help="number of mining trucks")
    parser.add_argument("--stations", "-m", type=int, help="number of mining unloading stations")
    parser.add_argument("--verbose", "-v", action="store_true", help="enable this flag when stats print wanted at end of simulation")


    args = parser.parse_args()
    # verify required parameters are passed to main file
    if not args.trucks or not args.stations:
        print("Ensure that -n and -m parameters are passed")
        sys.exit(-1)

    start_time = time.time()
    main(number_trucks=args.trucks, number_stations=args.stations, verbose=args.verbose)
    print(f"Simulation execution time: {time.time()-start_time}")
