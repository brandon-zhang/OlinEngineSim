import math
from Grain import Grain


class Engine:
    """Class that represents an engine with grains"""

    def __init__(self, ri, ro, l, rt, re):
        self.ri = ri
        self.ro = ro
        self.l = l
        self.grains = []
        self.rt = rt
        self.re = re

    def update(self, ri, ro, l, rt, re):
        """Update the engine parameters"""
        self.ri = ri
        self.ro = ro
        self.l = l
        self.rt = rt
        self.re = re

    def remaining_length(self):
        result = self.l
        for grain in self.grains:
            result -= grain.l
        return result

    def remaining_length_except(self, grain_num):
        result = self.l
        for i in range(0, len(self.grains)):
            if not i == grain_num:
                result -= self.grains[i].l
        return result

    def add_grain(self, ro, ri, l):
        """Add a propellant grain"""
        self.grains.append(Grain(ro, ri, l))

    def get_throat_area(self):
        """Calculates and returns the nozzle throat area"""
        return math.pi*math.pow(self.rt, 2)

    def get_exp_rat(self):
        """Calculates and returns the nozzle expansion ratio"""
        return math.pi*math.pow(self.re, 2)/(math.pi*math.pow(self.rt, 2))

    def get_exit_area(self):
        """Calculates and returns the nozzle exit area"""
        return math.pi * math.pow(self.re, 2)

    def get_prop_vol(self):
        """Calculates the total propellant volume in the engine"""
        result = 0
        for grain in self.grains:
            result += grain.calc_vol()
        return result

    def get_chamber_vol(self):
        """ Calculates the total chamber volume"""
        return math.pi*self.l*math.pow(self.ri, 2)