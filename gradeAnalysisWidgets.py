import tkinter as tk
from tkinter import ttk
from functools import partial
import sys
import platform
import subprocess


class ConfirmButton:
    def __init__(self):
        self.confirm_button = None

    def make_confirm_button(self, where, title="Confirm", command=None, row=int, column=int, helptip=""):
        self.confirm_button = tk.Button(where, text=title, command=command)
        self.confirm_button.grid(row=row, column=column)
        self.bind_tooltip_events(self.confirm_button, helptip)
    
    def bind_tooltip_events(self, widget, text):
        # Bind tooltip show and hide events to a widget
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())


class TableWidget:
    def __init__(self):
        self.table = None

    def generic_tableview_widget(self, where, row=int, column=int, title="", colHeading="", helptip=""):
        self.table = ttk.Treeview(where, columns = colHeading, show='headings', selectmode=tk.BROWSE) #Table view for all options
        self.table.grid(row=row, column=column) 
        self.table.heading(colHeading, text=title)
        self.bind_tooltip_events(self.table, helptip)
        return self.table
    
    def insert(self, parent, index, values=()):
        if self.table is not None:
            self.table.insert(parent=parent, index=index, values=values)

    def selection(self):
        if self.table is not None:
            selected = self.table.selection()
            if selected:
                return selected
            else:
                print(f"No selection found.")
        else:
            print("Table is not initialized.")

    def item(self, selected_item):
        if self.table is not None:
            item_info = self.table.item(selected_item)
            values = item_info.get('values', ())
            if values:
                return values[0]  # Return the first value, if it exists
            else:
                print(f"No values found for item: {selected_item}")
        else:
            print("Table is not initialized.")

    def destroy(self):
        if self.table is not None:
            self.table.destroy()

    def grid_forget(self):
        self.table.grid_forget()

    
    def bind_tooltip_events(self, widget, text):
        # Bind tooltip show and hide events to a widget
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())

class ThresholdWidget:
    def __init__(self):
        self.label = None
        self.entry = None
    
    def generic_thresholds_widget(self, where, state=str, text=str, row=int, column=int, help=str):
        self.label = tk.Label(where, text=text)
        self.label.grid(row=row, column=column, sticky=tk.W)
        self.entry = tk.Entry(where, width=3)
        self.entry.config(state=state)
        self.entry.grid(row=row, column=column+1, sticky=tk.W)
        self.bind_tooltip_events(self.entry, help)

    def get_entry_value(self):
        if self.entry.get()!="":
            return int(self.entry.get())
        else:
            return

    def destroy(self):
        if self.label is not None:
            self.label.destroy()
        if self.entry is not None:
            self.entry.destroy()


    def bind_tooltip_events(self, widget, text):
        # Bind tooltip show and hide events to a widget
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())

class CheckboxWidget:
    def __init__(self):
        self.checkboxes = {}

    def create_checkbox(self, text, help_text, state, where, row, column):
        checkbox_state = tk.BooleanVar()
        checkbox = tk.Checkbutton(where, state=state, text=text, variable=checkbox_state)
        checkbox.grid(row=row, column=column, sticky=tk.W)
        self.bind_tooltip_events(checkbox, help_text)
        self.checkboxes[text] = checkbox_state

    def create_multiple_checkboxes(self, options, state, where, row, column):
        for idx, (text, help_text) in enumerate(options.items(), start=row):
            self.create_checkbox(text, help_text, state, where, idx, column)

    def get_selected_analyses(self):
        selected = {text: state.get() for text, state in self.checkboxes.items()}
        return selected

    def destroy(self):
            self.checkboxes.clear()

    def bind_tooltip_events(self, widget, text):
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
    

class Console(tk.Text):
    def __init__(self, *args, **kwargs):
        kwargs.update({"state": "disabled"})
        tk.Text.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        sys.stdout = self

    def delete(self, *args, **kwargs):
        self.config(state="normal")
        self.delete(*args, **kwargs)
        self.config(state="disabled")

    def write(self, content):
        self.config(state="normal")
        self.insert(tk.END, content)
        self.see("end")
        self.config(state="disabled")

    def reset(self, event):
        sys.stdout = self.old_stdout




class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

    def showtip(self):
        # Method to show tooltip on hover
        self.tooltip_window = tk.Toplevel(self.widget)
        tooltip_label = tk.Label(self.tooltip_window, text=self.text)
        tooltip_label.pack()

        self.tooltip_window.overrideredirect(True)

        x = self.widget.winfo_rootx() + 50
        y = self.widget.winfo_rooty() + 50
        self.tooltip_window.geometry(f"+{x}+{y}")

    def hidetip(self):
        # Method to hide tooltip when not hovering
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class FileOpener:
    def __init__(self, file_path):
        self.file_path = file_path

    def print(self):
        print(self.file_path)

    def open_file(self, *args):
        current_platform = platform.system()
        if current_platform == "Linux":
            subprocess.Popen(["xdg-open", self.file_path])
        elif current_platform == "Windows":
            subprocess.Popen(["cmd", "/c", "start", self.file_path], shell=True)
        elif current_platform == "Darwin":  # macOS
            subprocess.Popen(["open", self.file_path])
        else:
            return
        
    
