import logging

def setup_logger(name="SimulationLogger"):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

