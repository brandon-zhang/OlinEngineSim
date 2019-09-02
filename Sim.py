from Engine import Engine
import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from numpy import linspace
from numpy import array

class Sim:
    """Class that contains simulation parameters and runs the simulation"""

    def __init__(self, ri=0, ro=0, l=0, rt=0, re=0, rhop=0, k=0, MM=1, a=0, n=0, T=0, patm=0, tstepnum=0, tspan=1):
        # Create a dictionary of keys as parameter names and values as parameter values
        self.values = dict({'ri': ri, "ro": ro, "l": l, "rt": rt, "re": re, "rhop": rhop, "k": k, "MM": MM, "a": a, "n": n, "T": T, "patm": patm, "tstepnum": tstepnum, "tspan": tspan})
        # Create an Engine based off those values
        self.engine = Engine(ri, ro, l, rt, re)
        # Make a timespan to run the simulation for
        self.tspan = linspace(0, tspan, num=int(self.values["tstepnum"]))
        # Length units = mm
        # Density units = g/cm3
        # Pressure units = MPa
        # Molar mass units = g/mol
        # Temperature units = K
        # Force units = N
        self.p = []
        self.F = []
        self.R = 8314 # Gas constant, units J/K kmol
        self.R_specific = self.R / self.values["MM"] # Specific gas constant
        self.It = 0
        self.Isp = 0
        self.burn_time = 0
        self.burn_time_bool = True

    def open_file(self, filename):
        """Opens a saved file and imports the parameters"""
        if filename != '':
            f = open(filename, 'r')
            file = f.read()
            attr = file.split("grain")[0].splitlines()
            grains = file.split("grain")[1].splitlines()
            # Load the new parameters into the sim
            for i in attr:
                split = i.split(" = ")
                self.values[split[0]] = float(split[1])
            for i in grains:
                grain = i.split(',')
                if grain[0] != '':
                    self.add_grain(float(grain[0]), float(grain[1]))
            f.close()
        # Update the engine, tspan, and specific gas constant with the new parameters
        self.engine.update(self.values["ri"], self.values["ro"], self.values["l"], self.values["rt"], self.values["re"])
        self.tspan = linspace(0, 2, num=int(self.values["tstepnum"]))
        self.R_specific = self.R / self.values["MM"]

    def open_bsx_file(self, filename):
        """Opens a .bsx file and loads the values into the propellant parameters. Unused"""
        if filename != '':
            f = open(filename, 'r')
            file = f.read()
            attr = file.split('"')
            for i in range(0, len(attr)):
                if attr[i].find("Density") != -1:
                    self.values["rhop"] = float(attr[i+1])*27.6799
                if attr[i].find("BallisticA") != -1:
                    self.values["a"] = float(attr[i+1])
                if attr[i].find("BallisticN") != -1:
                    self.values["n"] = float(attr[i+1])
                if attr[i].find("SpecificHeatRatio") != -1:
                    self.values["k"] = float(attr[i+1])
                if attr[i].find("MolarMass") != -1:
                    self.values["MM"] = float(attr[i+1])
            for i2 in range(0, len(attr)):
                if attr[i2].find("ISPStar") != -1:
                    print(self.values["k"])
                    print("\n")
                    print((2/(self.values["k"]+1))**((self.values["k"] + 1)/(self.values["k"]-1)))
                    print("\n")
                    print(self.values["k"] * (2/(self.values["k"]+1))**((self.values["k"] + 1)/(self.values["k"]-1)))
                    self.values["T"] = float(attr[i2+1])**2 * 9.81 * self.values["k"] * (2/(self.values["k"]+1))**((self.values["k"] + 1)/(self.values["k"]-1)) / self.R_specific
            f.close()
        self.engine.update(self.values["ri"], self.values["ro"], self.values["l"], self.values["rt"], self.values["re"])
        self.tspan = linspace(0, 2, num=int(self.values["tstepnum"]))
        self.R_specific = self.R / self.values["MM"]

    def add_grain(self, ri, l):
        """Adds a new grain"""
        self.engine.add_grain(self.engine.ri, ri, l)

    def add_grain_file(self, filename):
        """Sets engine grains based off a file. Unused"""
        f = open(filename, 'r')
        fin = f.read()
        grains = fin.split("grain,")
        for i in grains:
            grain = i.split(",")
            if grain[0] != '':
                self.add_grain(float(grain[0]), float(grain[1]))
        f.close()

    def run_sim_grains(self):
        """Runs the simulation and saves chamber pressure results"""
        # Clear all flags, pressure results, and recreate tspan
        self.burn_time_bool = True
        self.p = []
        self.tspan = linspace(0, self.values["tspan"], num=int(self.values["tstepnum"]))
        grain_num = len(self.engine.grains)
        def dzdt(z, t):
            At = self.engine.get_throat_area()
            result = [0] * (2*grain_num + 1)
            m_sto = z[0]
            V_chamber = self.engine.l * math.pi * self.engine.ri ** 2
            prop_V_total = 0
            Ab_total = 0
            ri_list = [0]*grain_num
            l_list = [0]*grain_num
            for i in range(1, grain_num+1):
                if z[i] > self.engine.ri or z[i+grain_num] < 0:
                    ri_list[i-1] = self.engine.ri
                    l_list[i-1] = 0
                else:
                    ri_list[i-1] = z[i]
                    l_list[i-1] = z[i+grain_num]
                prop_V_total += math.pi*l_list[i-1]*(self.engine.ri**2 - ri_list[i-1]**2)
                Ab_total += 2*math.pi*(ri_list[i-1] * l_list[i-1] + self.engine.ri**2 - ri_list[i-1]**2)
            V_free = V_chamber - prop_V_total
            P = (m_sto * self.R_specific * self.values["T"]) / (V_free / 1000)
            r = 25.4 * self.values["a"] * (P * 145)**self.values["n"]
            d_m_gen = Ab_total*self.values["rhop"]*r/1000**2
            d_m_noz = (P-self.values["patm"])*At*math.sqrt(self.values["k"]/(self.R_specific*self.values["T"]))*math.pow((2/(self.values["k"] + 1)), (self.values["k"] + 1)/(2*self.values["k"] - 2))
            result[0] = d_m_gen - d_m_noz
            for i in range(1, grain_num+1):
                result[i] = r
                result[i+grain_num] = -2*r
                if z[i] > self.engine.ri or z[i+grain_num] < 0:
                    result[i] = 0
                    result[i+grain_num] = 0
            if P < self.values["patm"] + 0.1 and t > 1:
                result = [0] * (2*grain_num+1)
                if self.burn_time_bool:
                    self.burn_time = t
                    self.burn_time_bool = False
            return result
        z0 = [0.0000035] * (2*grain_num + 1)
        for i in range(1, grain_num+1):
            z0[i] = self.engine.grains[i-1].ri
            z0[i+grain_num] = self.engine.grains[i-1].l
        sol = odeint(dzdt, z0, self.tspan)
        sol_array = array(sol)
        tspancopy = []
        for i in range(0, len(sol_array)):
            if self.tspan[i] < self.burn_time:
                m_sto = sol_array[i, 0]
                V = self.engine.get_chamber_vol()
                for b in range(1, grain_num + 1):
                    ri = sol_array[i, b]
                    l = sol_array[i, b + grain_num]
                    V -= math.pi * l * (self.engine.ri ** 2 - ri ** 2)
                self.p.append((m_sto * self.R_specific * self.values["T"]) / (V / 1000))
                tspancopy.append(self.tspan[i])
        self.tspan = tspancopy

    def plot_pres_odeint(self):
        plt.plot(self.tspan, self.p)
        plt.show()

    def calc_thrust(self):
        self.It = 0
        self.F = []
        At = self.engine.get_throat_area()
        Ae = self.engine.get_exit_area()

        def fun(pe, *args):
            p = args[0]
            return abs(((self.values["k"]+1)/2)**(1/(self.values["k"]-1)) * (pe/p)**(1/self.values["k"]) * math.sqrt(((self.values["k"]+1)/(self.values["k"]-1))*(1 - (pe/p)**((self.values["k"]-1)/self.values["k"]))) - At/Ae)
        for pres in self.p:
            if pres < self.values["patm"]:
                pres = self.values["patm"]
            pe = minimize(fun, [0], args=pres, method='TNC', bounds=((0,pres-0.001),)).x
            if pe < self.values["patm"]:
                pe = self.values["patm"]
            F_new = At * pres * math.sqrt((2*self.values["k"]**2)/(self.values["k"]-1) * (2/(self.values["k"]+1))**((self.values["k"]+1)/(self.values["k"]-1)) * (1 - (pe/pres)**((self.values["k"]-1)/self.values["k"]))) + (pe - self.values["patm"])*Ae
            self.F.append(F_new)
            self.It += F_new * 2/(self.values["tstepnum"]-1)
        prop_mass = self.engine.get_prop_vol() * self.values["rhop"]/1000**2
        self.Isp = self.It/prop_mass

    def plot_thrust(self):
        plt.plot(self.tspan, self.F)
        plt.show()

    def calc_imp(self):
        self.It = 0
        for force in range(1, len(self.F)):
            self.It += self.F[force]*(self.tspan[force] - self.tspan[force-1])
        self.Isp = 0
