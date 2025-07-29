"""
Created on July 27th, 2026

@author: jorge-jimenez-mejia
"""

import logging

ENABLE_LIVE_DEBUGGING: bool = False

logger = logging.getLogger("sim logger")
logger.setLevel(logging.INFO)

if ENABLE_LIVE_DEBUGGING:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

file_handler = logging.FileHandler("sim.log")
file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

if not logger.handlers:
    if ENABLE_LIVE_DEBUGGING:
        logger.addHandler(console_handler)
    logger.addHandler(file_handler)
