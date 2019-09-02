from tkinter import *
from tkinter import ttk

class InputPanel:
    """A multi-page frame for sim parameter inputs"""

    def __init__(self, root, sim):
        # The base Notebook
        self.input_panel = ttk.Notebook(root)
        self.input_panel.grid(row=0, column=1)

        # The sim to reference values from
        self.sim = sim

        # A dictionary with keys as parameter names and values as the corresponding input field
        self.inputs = {}

        # Adding the propellant parameter frame
        self.prop_panel = Frame(self.input_panel)
        self.input_panel.add(self.prop_panel, text='Propellant')

        # Adding the propellant density input, and setting the value to 1
        Label(self.prop_panel, text="Propellant Density").grid(row=0)
        self.rhop_input = Entry(self.prop_panel)
        self.rhop_input.grid(row=0, column=1)
        self.rhop_input.delete(0, END)
        self.rhop_input.insert(0, 1)
        self.inputs["rhop"] = self.rhop_input

        Label(self.prop_panel, text="Specific Heat Ratio").grid(row=1)
        self.k_input = Entry(self.prop_panel)
        self.k_input.grid(row=1, column=1)
        self.k_input.delete(0, END)
        self.k_input.insert(0, 1)
        self.inputs["k"] = self.k_input

        Label(self.prop_panel, text="Molar Mass").grid(row=2)
        self.MM_input = Entry(self.prop_panel)
        self.MM_input.grid(row=2, column=1)
        self.MM_input.delete(0, END)
        self.MM_input.insert(0, 1)
        self.inputs["MM"] = self.MM_input

        Label(self.prop_panel, text="Saint Roberts (a)").grid(row=3)
        self.a_input = Entry(self.prop_panel)
        self.a_input.grid(row=3, column=1)
        self.a_input.delete(0, END)
        self.a_input.insert(0, 1)
        self.inputs["a"] = self.a_input

        Label(self.prop_panel, text="Saint Roberts (n)").grid(row=4)
        self.n_input = Entry(self.prop_panel)
        self.n_input.grid(row=4, column=1)
        self.n_input.delete(0, END)
        self.n_input.insert(0, 1)
        self.inputs["n"] = self.n_input

        Label(self.prop_panel, text="Combust. Temp.").grid(row=5)
        self.T_input = Entry(self.prop_panel)
        self.T_input.grid(row=5, column=1)
        self.T_input.delete(0, END)
        self.T_input.insert(0, 1)
        self.inputs["T"] = self.T_input

        Label(self.prop_panel, text="Ambient Pressure").grid(row=6)
        self.patm_input = Entry(self.prop_panel)
        self.patm_input.grid(row=6, column=1)
        self.patm_input.delete(0, END)
        self.patm_input.insert(0, 1)
        self.inputs["patm"] = self.patm_input

        # Adding the engine parameter panel
        self.engine_panel = Frame(self.input_panel)
        self.input_panel.add(self.engine_panel, text='Nozzle')

        Label(self.engine_panel, text="Inner Radius").grid(row=0)
        self.ri_input = Entry(self.engine_panel)
        self.ri_input.grid(row=0, column=1)
        self.ri_input.delete(0, END)
        self.ri_input.insert(0, 1)
        self.inputs["ri"] = self.ri_input

        Label(self.engine_panel, text="Outer Radius").grid(row=1)
        self.ro_input = Entry(self.engine_panel)
        self.ro_input.grid(row=1, column=1)
        self.ro_input.delete(0, END)
        self.ro_input.insert(0, 1)
        self.inputs["ro"] = self.ro_input

        Label(self.engine_panel, text="Casing Length").grid(row=2)
        self.l_input = Entry(self.engine_panel)
        self.l_input.grid(row=2, column=1)
        self.l_input.delete(0, END)
        self.l_input.insert(0, 1)
        self.inputs["l"] = self.l_input

        Label(self.engine_panel, text="Throat Radius").grid(row=3)
        self.rt_input = Entry(self.engine_panel)
        self.rt_input.grid(row=3, column=1)
        self.rt_input.delete(0, END)
        self.rt_input.insert(0, 1)
        self.inputs["rt"] = self.rt_input

        Label(self.engine_panel, text="Exit Radius").grid(row=4)
        self.re_input = Entry(self.engine_panel)
        self.re_input.grid(row=4, column=1)
        self.re_input.delete(0, END)
        self.re_input.insert(0, 1)
        self.inputs["re"] = self.re_input

        # Adding the rocket parameter panel. Functionality TBD
        self.rocket_panel = Frame(self.input_panel)
        self.input_panel.add(self.rocket_panel, text='Rocket')

        # Adding the simulation parameter panel
        self.sim_panel = Frame(self.input_panel)
        self.input_panel.add(self.sim_panel, text='Sim')

        Label(self.sim_panel, text="Sim Runtime").grid(row=0)
        self.runtime_input = Entry(self.sim_panel)
        self.runtime_input.grid(row=0, column=1)
        self.runtime_input.delete(0, END)
        self.runtime_input.insert(0, 1)
        self.inputs["tspan"] = self.runtime_input

        Label(self.sim_panel, text="Step Count").grid(row=1)
        self.tstep_input = Entry(self.sim_panel)
        self.tstep_input.grid(row=1, column=1)
        self.tstep_input.delete(0, END)
        self.tstep_input.insert(0, 1)
        self.inputs["tstepnum"] = self.tstep_input

    def update_inputs(self):
        """Updates the displayed value in the input fields from the current simulation parameters"""
        for key, value in self.inputs.items():
            value.delete(0, END)
            value.insert(0, self.sim.values[key])