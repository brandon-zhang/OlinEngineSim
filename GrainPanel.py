from tkinter import *
from Grain import Grain
from GrainInput import GrainInput
from tkinter import messagebox

class GrainPanel:
    """A container for all the grain input fields. Can add, reorder, change, and delete fields"""

    def __init__(self, root, sim):
        # Create a panel as the base, and an input panel on the left side of the base
        self.grain_panel = Frame(root)
        self.grain_input_panel = Frame(self.grain_panel)
        self.grain_input_panel.grid(row=0)
        Label(self.grain_input_panel, text="Position").grid(row=0)
        Label(self.grain_input_panel, text="Inner Radius").grid(row=0, column=1)
        Label(self.grain_input_panel, text="Length").grid(row=0, column=2)
        # Add a drawable canvas to display grain dimensions. Functionality TBD
        self.grain_diagram = Canvas(self.grain_panel)
        self.grain_diagram.grid(row=0, column=1)
        self.grain_entries = []
        self.sim = sim

        # Add a set of fields to create a new grain
        self.new_grain_order = Entry(self.grain_input_panel)
        self.new_grain_order.grid(row=len(self.grain_entries)+1, column=0)
        self.new_grain_ri = Entry(self.grain_input_panel)
        self.new_grain_ri.grid(row=len(self.grain_entries)+1, column=1)
        self.new_grain_l = Entry(self.grain_input_panel)
        self.new_grain_l.grid(row=len(self.grain_entries)+1, column=2)
        self.new_grain_button = Button(self.grain_input_panel, text="Add", command=self.add_grain)
        self.new_grain_button.grid(row=len(self.grain_entries)+1, column=3)

    def add_grain(self):
        """Adds a new grain either at the specified location, or appended to the end. Updates the grain order after"""
        # Check if parameters are <= 0
        if float(self.new_grain_ri.get()) <= 0 or float(self.new_grain_l.get()) <= 0:
            messagebox.showerror("Error", "Grain dimensions must be greater than 0")
        # Check if inner grain radius is not smaller than casing radius
        elif float(self.new_grain_ri.get()) >= self.sim.engine.ri:
            messagebox.showerror("Error", "Inner radius must be smaller than casing inner radius")
            print(self.new_grain_ri.get())
            print(self.sim.engine.ri)
        # Check if grains protrude from casing
        elif float(self.new_grain_l.get()) > self.sim.engine.remaining_length():
            messagebox.showerror("Error", "Total grain length is longer than casing")
        else:
            # Check if new grain should be appended to the end
            if int(self.new_grain_order.get()) >= len(self.grain_entries):
                # Add a new grain input with current values from the new grain input fields
                self.grain_entries.append(GrainInput(self.grain_input_panel, int(self.new_grain_order.get()),
                                                     self.update_row, self.update_sim_vals, self.update_delete, float(self.new_grain_ri.get()),
                                                     float(self.new_grain_l.get())))
            else: # Otherwise, insert new grain into middle
                # Insert a new grain input with current values form the new grain input fields
                self.grain_entries.insert(int(self.new_grain_order.get())-1,
                                          GrainInput(self.grain_input_panel,
                                                     int(self.new_grain_order.get()),
                                                     self.update_row, self.update_sim_vals, self.update_delete,
                                                     float(self.new_grain_ri.get()), float(self.new_grain_l.get())))
            # Reorder grains after insertion
            for i2 in range(len(self.grain_entries)):
                self.grain_entries[i2].update_entry_row(i2)
            # Make sure new grain input fields are still at the bottom
            self.new_grain_order.grid(row=len(self.grain_entries)+1, column=0)
            self.new_grain_ri.grid(row=len(self.grain_entries) + 1, column=1)
            self.new_grain_l.grid(row=len(self.grain_entries) + 1, column=2)
            self.new_grain_button.grid(row=len(self.grain_entries) + 1, column=3)

    def update_row(self):
        """Updates the order of grains if the order field of one is edited"""
        row = 0
        # For each grain, if the position does not match the row input field, either insert it into new position or
        # move to end
        for i in range(len(self.grain_entries)):
            if i != self.grain_entries[i].get_row():
                row = self.grain_entries[i].get_row()
                if row < 0:  # If the row would be negative, push it to the front
                    row = 0
                copy = self.grain_entries.pop(i)
                # If desired position is larger than list of grains, move to end
                if row >= len(self.grain_entries):
                    self.grain_entries.append(copy)
                # Otherwise, insert the grain into the new position
                else:
                    self.grain_entries.insert(self.grain_entries[i].get_row(), copy)
        # Reorder grains after insertion
        for i2 in range(row+1, len(self.grain_entries)):
            self.grain_entries[i2].update_entry_row(i2)
        # Make sure new grain input fields are still at the bottom
        self.new_grain_order.grid(row=len(self.grain_entries) + 1, column=0)
        self.new_grain_ri.grid(row=len(self.grain_entries) + 1, column=1)
        self.new_grain_l.grid(row=len(self.grain_entries) + 1, column=2)
        self.new_grain_button.grid(row=len(self.grain_entries) + 1, column=3)

    def update_delete(self):
        """Checks delete flag and removes deleted grains"""
        # Check for deletion and remove grain if true
        for i in self.grain_entries:
            if i.delete_flag:
                self.grain_entries.pop(i.get_row())
        # Reorder grains after deletion
        for i2 in range(len(self.grain_entries)):
            self.grain_entries[i2].update_entry_row(i2)
        # Make sure new grain input fields are still at bottom
        self.new_grain_order.grid(row=len(self.grain_entries) + 1, column=0)
        self.new_grain_ri.grid(row=len(self.grain_entries) + 1, column=1)
        self.new_grain_l.grid(row=len(self.grain_entries) + 1, column=2)
        self.new_grain_button.grid(row=len(self.grain_entries) + 1, column=3)

    def update_sim_vals(self):
        """Updates sim grain parameters based on input fields"""
        # Ensure that order is correct and deleted grains are removed
        self.update_row()
        self.update_delete()
        # Check that the parameters are usable
        for i in self.grain_entries:
            row = i.get_row()
            if i.get_ri() <= 0 or i.get_l() <= 0:
                messagebox.showerror("Error", "Grain dimensions must be greater than 0")
            # Check if inner grain radius is not smaller than casing radius
            elif i.get_ri() >= self.sim.engine.ri:
                messagebox.showerror("Error", "Inner radius must be smaller than casing inner radius")
            # Check if grains protrude from casing
            elif i.get_l() > self.sim.engine.remaining_length_except(row)+0.01:
                print(self.sim.engine.remaining_length_except(row))
                print(i.get_l())
                messagebox.showerror("Error", "Total grain length is longer than casing")
            else:  # For each grain entry field, either update the corresponding grain with new parameters or create a new grain
                if row >= len(self.sim.engine.grains):
                    self.sim.engine.grain_list.append(Grain(self.sim.engine.ri, i.get_ri(), i.get_l()))
                else:
                    self.sim.engine.grains[row] = Grain(self.sim.engine.ri, i.get_ri(), i.get_l())

    def update_inputs(self):
        """Update displayed input fields based on sim grain parameters"""
        # Clear all grain entries in the panel
        for i in self.grain_entries:
            i.destroy()
        self.grain_entries = []
        # Remake the list based on current sim grains
        for i2 in range(len(self.sim.engine.grains)):
            self.grain_entries.append(GrainInput(self.grain_input_panel, i2, self.update_row, self.update_sim_vals, self.update_delete, self.sim.engine.grains[i2].ri, self.sim.engine.grains[i2].l))
