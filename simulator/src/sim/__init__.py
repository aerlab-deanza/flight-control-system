"""
Makes `src/sim` a Python package.
Re-exports the six simulation subsystem classes:
    Plant, FlightController, SensorSuite, MahonyFilter, Logger, Scheduler.
Importing from here ensures internal refactors don't break external call sites.
"""
 