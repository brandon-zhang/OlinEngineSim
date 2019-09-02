import math

class Grain:
    """Class that represents 1 propellant grain"""

    def __init__(self, ro, ri, l):
        self.ro = ro
        self.ri = ri
        self.l = l

    def calc_vol(self):
        """Calculates and returns propellant volume"""
        return self.l * math.pi * (self.ro**2 - self.ri**2)

