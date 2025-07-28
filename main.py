"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import sys
import os
import argparse
import textwrap
import random

from truck import Truck, TruckDataCollection
from unload_stations import UnloadStation
from simulation_execution import run_simulation

SIMULATION_TIME: int = 72 # hours
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
    stations: list[Truck] = [UnloadStation for _ in range(number_stations)]

    # run simulation
    run_simulation(trucks=trucks,
                   stations=stations,
                   simulation_time=SIMULATION_TIME)

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

    main(number_trucks=args.trucks, number_stations=args.stations)