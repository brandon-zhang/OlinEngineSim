from tkinter import *

class ResultsPanel:
    """A container for the sim results on the right-hand side"""

    def __init__(self, sim, root):
        # Save sim
        self.sim = sim
        self.results_panel = Frame(root)

        # Create and pack labels
        self.time_label = Label(self.results_panel, text="Burn Time = ")
        self.time_label.grid(row=0)
        self.total_impulse_label = Label(self.results_panel, text="Total Impulse = ")
        self.total_impulse_label.grid(row=1)
        self.specific_impulse_label = Label(self.results_panel, text="Specific Impulse = ")
        self.specific_impulse_label.grid(row=2)
        self.p_label = Label(self.results_panel, text="Max Chamber Pressure = ")
        self.p_label.grid(row=3)


    def update_vals(self):
        """Updates labels with values from simulation"""
        self.time_label['text'] = "Burn Time = %.2f sec" %self.sim.burn_time
        self.total_impulse_label['text'] = "Total Impulse = %.2f Ns" %self.sim.It
        self.specific_impulse_label['text'] = "Total Impuse = %.2f Ns" %self.sim.Isp
        self.p_label['text'] = "Max Chamber Pressure = %.2f MPa" %max(self.sim.p)
