from tkinter import *

class GrainInput:
    """A container for a grain input"""

    def __init__(self, root, row, update_grain_row, update_grain_val, update_delete, ri=0, l=0):
        # External methods for updating row, value, and deletion whenever the grain input is updated
        self.update_grain_row = update_grain_row
        self.update_grain_val = update_grain_val
        self.update_delete = update_delete

        # Create an entry field and call the update_row method whenever editing is done (i.e. focus shifts away)
        sv_order = StringVar()
        self.order_entry = Entry(root, textvariable=sv_order, validate='focusout', validatecommand=self.update_grain_row)
        # Remember that there is a label in row 0
        self.order_entry.grid(row=row+1, column=0)
        self.order_entry.delete(0, END)
        # Grain order indexing starts at 1, not 0
        self.order_entry.insert(0, row+1)

        sv_ri = StringVar()
        self.ri_entry = Entry(root, textvariable=sv_ri, validate='focusout', validatecommand=self.update_grain_val)
        self.ri_entry.grid(row=row+1, column=1)
        self.ri_entry.delete(0, END)
        self.ri_entry.insert(0, ri)

        sv_l = StringVar()
        self.l_entry = Entry(root, textvariable=sv_l, validate='focusout', validatecommand=self.update_grain_val)
        self.l_entry.grid(row=row+1, column=2)
        self.l_entry.delete(0, END)
        self.l_entry.insert(0, l)

        # Create a button to delete the field and release its entry fields
        self.delete_button = Button(root, text="Delete", command=self.destroy)
        self.delete_button.grid(row=row+1, column=3)

        # Flag for deletion for external methods to check
        self.delete_flag = FALSE

    def get_row(self):
        """Returns the row-1, due to zero-indexing"""
        return int(self.order_entry.get())-1

    def get_ri(self):
        """Returns the current value of ri"""
        return float(self.ri_entry.get())

    def get_l(self):
        """Returns the current value of l"""
        return float(self.l_entry.get())

    def update_entry_val(self, grain):
        """Updates the displayed values of ri and l from the given grain"""
        self.ri_entry.delete(0, END)
        self.ri_entry.insert(0, grain.ri)
        self.l_entry.delete(0, END)
        self.l_entry.insert(0, grain.l)

    def update_entry_row(self, row):
        """Repacks the entry fields to the given row"""
        self.order_entry.grid(row=row + 1, column=0)
        self.ri_entry.grid(row=row + 1, column=1)
        self.l_entry.grid(row=row + 1, column=2)
        self.delete_button.grid(row=row + 1, column=3)
        self.order_entry.delete(0, END)
        # Sets the displayed row value to the current position
        self.order_entry.insert(0, row+1)

    def destroy(self):
        """"Sets a delete flag for external methods and destroys all the attached entry fields"""
        self.delete_flag = TRUE
        self.update_delete()
        self.order_entry.destroy()
        self.l_entry.destroy()
        self.ri_entry.destroy()
        self.delete_button.destroy()
