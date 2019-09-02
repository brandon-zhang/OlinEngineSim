from tkinter import *
from tkinter import filedialog
from Sim import Sim
from InputPanel import InputPanel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GrainPanel import GrainPanel
from ResultsPanel import ResultsPanel
import os
from tkinter import messagebox


class Main:
    """The main window for the program"""
    def __init__(self):
        root = Tk()

        # Creating the simulation
        self.sim = Sim()

        # Creating the parameter input panel
        self.input_panel = InputPanel(root, self.sim)
        self.input_panel.input_panel.grid(row=0, column=1)

        # Creating the grain input panel
        self.grain_panel = GrainPanel(root, self.sim)
        self.grain_panel.grain_panel.grid(row=0)

        #Creating the results panel
        self.results_panel = ResultsPanel(self.sim, root)
        self.results_panel.results_panel.grid(row=1, column=1)

        # Configuring the menubar
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_file)
        self.filemenu.add_command(label="Open", command=self.open_file)
        # self.filemenu.add_command(label="Open Propellant", command=self.open_prop_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Creating the calculate button
        calc = Button(root, text="Calculate", command=self.plot_sim)
        calc.grid(row=2, column=1)

        # Creating the figure to plot pressure and force
        self.figure = plt.Figure(figsize=(10,5))
        self.chart = FigureCanvasTkAgg(self.figure, root)
        self.chart.show()
        self.chart.get_tk_widget().grid(row=1, column=0)

        root.iconbitmap('rocketry_icon.ico')
        root.title("Olin Rocketry Burn Simulator")
        self.is_saved = FALSE
        self.update_val()

        root.mainloop()

    def open_file(self):
        """Opens the selected file and updates the sim parameters and displayed parameters"""
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        # Update the sim parameters
        self.sim.open_file(filename)

        # Update the displayed values in the inputs
        self.input_panel.update_inputs()
        self.grain_panel.update_inputs()
        self.is_saved = TRUE

    def open_prop_file(self):
        """Opens the selected .bsx file and updates the sim parameters. Unused due to inconsistencies with how ProPep3 saves .bsx files"""
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                              filetypes=(("ProPep3 Files", "*.bsx"), ("all files", "*.*")))
        # Update the sim parameters
        self.sim.open_bsx_file(filename)

        # Update the displayed values in the inputs
        self.input_panel.update_inputs()
        self.grain_panel.update_inputs()

    def update_val(self):
        """Updates the sim parameters from the inputs"""
        # Get and update the sim values
        for key, value in self.input_panel.inputs.items():
            if float(value.get()) <= 0:  # Check if any of the inputs are <= 0. If so, send error popup
                messagebox.showerror("Error", "Values must be greater than 0")
                value.delete(0, END)
                value.insert(0, 1)
                self.sim.values[key] = 1
            else:
                self.sim.values[key] = float(value.get())
        # Update the engine parameters
        self.sim.engine.update(self.sim.values["ri"], self.sim.values["ro"], self.sim.values["l"], self.sim.values["rt"], self.sim.values["re"])
        # Get and update the propellant grains
        self.grain_panel.update_sim_vals()
        self.is_saved = FALSE

    def plot_sim(self):
        """Runs the simulation, calculates engine attributes, and plots the result"""
        # Updates sim parameters before running sim
        self.update_val()

        # Runs simulation and calculates thrust
        self.sim.run_sim_grains()
        self.sim.calc_thrust()

        # Clears figure and plots pressure and force
        self.figure.clf()
        pres_plot = self.figure.add_subplot(121)
        pres_plot.plot(self.sim.tspan, self.sim.p)
        force_plot = self.figure.add_subplot(122)
        force_plot.plot(self.sim.tspan, self.sim.F)
        self.chart.show()

        # Displays results (total impulse, specific impulse, etc)
        self.results_panel.update_vals()

    def save_file(self):
        """Saves the current simulation file"""
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        if filename != '':
            f = open(filename, 'w')
            # Save the sim parameters
            for key, value in self.sim.values.items():
                f.write(str(key) + " = " + str(value) + "\n")

            # Save the propellant grain dimensions
            f.write("grain\n")
            for grain in self.sim.engine.grains:
                f.write(str(grain.ri) + "," + str(grain.l) + "\n")
            f.close()
        self.is_saved = TRUE

    def new_file(self):
        """Resets all parameters"""
        if not self.is_saved:
            if messagebox.askyesno("Unsaved simulation!" "Would you like to save?"):
                self.save_file()
        for i in self.input_panel.inputs:
            self.input_panel.inputs[i].delete(0, END)
            self.input_panel.inputs[i].insert(0, 1)
        self.update_val()
        self.is_saved = FALSE


if __name__ == '__main__':
    main = Main()
