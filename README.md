# Truck Loading & Unloading Simulation

This project simulates a lunar Helium-3 space mining operation. This simulation will manage
and track efficiency of mining trucks and unloads stations over a continuous 72-hour operation

---

## Simulation Overview

- **n trucks** mine Helium-3
- **m Mining Unload Sites** Mining unloading sites, each can serve one truck at a time
- **Unlimited loading stations** — There are unlimited lunar station to mine from
- Each truck takes:
  - **30 minutes** to travel between sites
  - **5 minutes** to unload at a station
  - **1 to 5 hours (random)** to complete loading
- In case that all unloading sites are busy, mining trucks will be queued up to shortest wait time

---

## Generated Stats

### Per Truck:
- `completed trips`: Number of successful unloaded materials
- `average_trip_time`: average round trip time taken
- `utilization_percent`: Percent spent actively working (loading, unloading, traveling)
- `idle_time` truck down time at queues

### Per Drop-Off Location:
- `total_unloads`: Total number of trucks served
- `idle_time`: Time spent inactive
- `utilization_percent`: Percent spent actively unloading
- `max_queue_length`: Largest queue
- `final_queue_length`: Trucks left in queue at end of simulation


---

## How to Run

1. python3 main.py -n {number of mining trucks} -m {number of mining unload stations} [-v {print stats}]
