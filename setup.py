from setuptools import setup, find_packages

setup(
    name        = "ParkOccupancy",
    url         = "https://github.com/The-Quantum/parkOccupancy.git",
    author      = "Donald MOUAFO, donald.l.mouafo@gmail.com",
    description = """The module manages parking occupancy classification. 
        The gold is the automatic parking management that provides in real-time the number of availbale lots.""",
    version='1.0.0',
    packages = find_packages()  
)