import tkinter as tk
from tkinter import ttk
from functools import partial
import sys
import logging
import platform
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.filedialog import asksaveasfilename
import os
import subprocess

class Logger(logging.Logger):
    _file_handler_created = False  # Class-level attribute

    def __init__(self, name, level=logging.DEBUG, log_file='.log.log'):
        super().__init__(name, level)

        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                            datefmt='%m/%d/%Y, [%H:%M:%S]')
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        if not Logger._file_handler_created:
            file_handler = logging.FileHandler(log_file, mode='w')
            Logger._file_handler_created = True
        else:
            #Subsequent logger instances should append to the file
            file_handler = logging.FileHandler(log_file, mode='a')

        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        self.setLevel(level)

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def warning(self, message):
        self.log(logging.WARNING, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def critical(self, message):
        self.log(logging.CRITICAL, message)

class ConfirmButton:
    def __init__(self):
        self.logger = Logger(__name__)  # Create a logger using the custom Logger class
        self.confirm_button = None
        self.logger.info("ConfirmButton instance initialized")

    def make_confirm_button(self, where, title="Confirm", command=None, row=int, column=int, helptip=""):
        self.logger.info(f"Creating confirm button titled '{title}' at row {row}, column {column}")
        self.confirm_button = tk.Button(where, text=title, command=command)
        self.confirm_button.grid(row=row, column=column)
        self.bind_tooltip_events(self.confirm_button, helptip)
        self.logger.debug("Confirm button created and grid placement set")

    def destroy(self):
        self.logger.debug("Destroying confirm button")
        if self.confirm_button is not None:
            self.confirm_button.destroy()
        self.logger.info("Confirm button destroyed")

    def bind_tooltip_events(self, widget, text):
        self.logger.debug(f"Binding tooltip events to widget with tooltip text: '{text}'")
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
        self.logger.debug("Tooltip events bound successfully")

class TableWidget:
    def __init__(self):
        self.logger = Logger(__name__)  # Create a logger for this class
        self.table = None
        self.logger.info("TableWidget instance initialized")

    def generic_tableview_widget(self, where, row=int, column=int, title="", colHeading="", helptip=""):
        self.logger.info(f"Creating table view widget titled '{title}' with columns '{colHeading}' at row {row}, column {column}")
        self.table = ttk.Treeview(where, columns=colHeading, show='headings', selectmode=tk.BROWSE)
        self.table.grid(row=row, column=column)
        self.table.heading(colHeading, text=title)
        self.bind_tooltip_events(self.table, helptip)
        self.logger.debug("Table view widget created and configured")
        return self.table
    
    def insert(self, parent, index, values=()):
        if self.table is not None:
            self.table.insert(parent=parent, index=index, values=values)
        else:
            self.logger.warning("Attempted to insert into uninitialized table")

    def selection(self):
        self.logger.debug("Getting selected item from table")
        if self.table is not None:
            selected = self.table.selection()
            if selected:
                self.logger.info(f"Selected item: {selected}")
                return selected
            else:
                self.logger.warning("No selection found")
        else:
            self.logger.error("Table is not initialized")

    def item(self, selected_item):
        self.logger.debug(f"Getting item info for: {selected_item}")
        if self.table is not None:
            item_info = self.table.item(selected_item)
            values = item_info.get('values', ())
            if values:
                self.logger.info(f"Values for item {selected_item}: {values}")
                return values[0]
            else:
                self.logger.warning(f"No values found for item: {selected_item}")
        else:
            self.logger.error("Table is not initialized")

    def destroy(self):
        self.logger.debug("Destroying table widget")
        if self.table is not None:
            self.table.destroy()

    def grid_forget(self):
        self.logger.debug("Forgetting grid placement of table")
        if self.table is not None:
            self.table.grid_forget()

    def bind_tooltip_events(self, widget, text):
        self.logger.debug(f"Binding tooltip events to widget with tooltip text: '{text}'")
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
        self.logger.debug("Tooltip events bound successfully")


class ThresholdWidget:
    def __init__(self):
        self.logger = Logger(__name__)  # Create a logger for this class
        self.label = None
        self.entry = None
        self.logger.info("ThresholdWidget instance initialized")

    def generic_thresholds_widget(self, where, state=str, text=str, row=int, column=int, help=str):
        self.logger.info(f"Creating threshold widget with label '{text}' at row {row}, column {column}")
        self.label = tk.Label(where, text=text)
        self.label.grid(row=row, column=column, sticky=tk.W)
        self.entry = tk.Entry(where, width=3)
        self.entry.config(state=state)
        self.entry.grid(row=row, column=column+1, sticky=tk.W)
        self.bind_tooltip_events(self.entry, help)
        self.logger.debug("Threshold widget created and configured")

    def get_entry_value(self):
        if self.entry is None or self.label is None:
            self.logger.error("Entry is not initialized")
            return
        entry_value = self.entry.get()
        if entry_value != "":
            self.logger.debug(f"Retrieving entry value: {entry_value}")
            return int(entry_value)
        else:
            self.logger.warning("Entry value is empty")
            return

    def destroy(self):
        self.logger.debug("Destroying threshold widget components")
        if self.label is not None:
            self.label.destroy()
        if self.entry is not None:
            self.entry.destroy()
        self.logger.info("Threshold widget components destroyed")

    def bind_tooltip_events(self, widget, text):
        self.logger.debug(f"Binding tooltip events to widget with tooltip text: '{text}'")
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
        self.logger.debug("Tooltip events bound successfully")



class CheckboxWidget:
    def __init__(self):
        self.logger = Logger(__name__)  # Create a logger for this class
        self.checkboxes = {}
        self.logger.info("CheckboxWidget instance initialized")

    def create_checkbox(self, text, help_text, state, where, row, column):
        self.logger.info(f"Creating checkbox '{text}' at row {row}, column {column}")
        checkbox_state = tk.BooleanVar()
        checkbox = tk.Checkbutton(where, state=state, text=text, variable=checkbox_state)
        checkbox.grid(row=row, column=column, sticky=tk.W)
        self.bind_tooltip_events(checkbox, help_text)
        self.checkboxes[text] = (checkbox, checkbox_state)
        self.logger.debug(f"Checkbox '{text}' created")

    def create_multiple_checkboxes(self, options, flags, state, where, row, column):
        self.logger.info("Creating multiple checkboxes")
        current_row = row
        for (text, help_text), flag in zip(options.items(), flags):
            if flag:
                self.create_checkbox(text, help_text, state, where, current_row, column)
                current_row += 1
        self.logger.debug("Multiple checkboxes created")


    def get_dict_of_checkbox(self):
        self.logger.debug("Retrieving selected checkboxes")
        selected = {text: state.get() for text, (_, state) in self.checkboxes.items()}
        self.logger.info(f"Selected checkboxes: {selected}")
        return selected

    def destroy(self):
        self.logger.debug("Destroying all checkboxes")
        for checkbox, _ in self.checkboxes.values():
            checkbox.destroy()
        self.checkboxes.clear()
        self.logger.info("All checkboxes destroyed")


    def bind_tooltip_events(self, widget, text):
        self.logger.debug(f"Binding tooltip events to widget '{widget}' with tooltip text: '{text}'")
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
        self.logger.debug(f"Tooltip events bound to widget '{widget}'")
    

class Console(tk.Text):
    def __init__(self, *args, **kwargs):
        self.logger = Logger(__name__)  # Create a logger for this class
        kwargs.update({"state": "disabled"})
        tk.Text.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        sys.stdout = self
        self.logger.info("Console widget initialized and stdout redirected")

    def delete(self, *args, **kwargs):
        self.logger.debug("Clearing console text")
        self.config(state="normal")
        super().delete(*args, **kwargs)  # Use super() to avoid recursion
        self.config(state="disabled")

    def write(self, content):
        self.config(state="normal")
        self.insert(tk.END, content)
        self.see(tk.END)
        self.config(state="disabled")

    def reset(self, event):
        sys.stdout = self.old_stdout
        self.logger.info("Console widget destroyed and stdout reset")




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
        self.logger = Logger(__name__) 
        self.file_path = file_path
        self.logger.info(f"FileOpener instance created for file: {file_path}")

    def print(self):
        self.logger.debug(f"Printing file path: {self.file_path}")
        print(self.file_path)

    def open_file(self, *args):
        current_platform = platform.system()
        self.logger.info(f"Attempting to open file on {current_platform} platform")
        if current_platform == "Linux":
            subprocess.Popen(["xdg-open", self.file_path])
            self.logger.debug("Opened file using xdg-open")
        elif current_platform == "Windows":
            subprocess.Popen(["cmd", "/c", "start", self.file_path], shell=True)
            self.logger.debug("Opened file using Windows cmd")
        elif current_platform == "Darwin":  # macOS
            subprocess.Popen(["open", self.file_path])
            self.logger.debug("Opened file on macOS using open")
        else:
            self.logger.warning("Unsupported platform for file opening")
            return
        

class tkMatplot:
    def __init__(self, title="", window_width=800, window_height=600, df=None, x_label=None, y_label=None, plot_type=None, color=None, x_plot=None, y_plot=None):
        self.root = tk.Tk()
        self.root.wm_title(title)

        self.logger = Logger(__name__)
        self.logger.info("Initializing tkMatplot class")

        
        self.root.geometry(f"{window_width}x{window_height}")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

        button_quit = tk.Button(master=self.root, text="Quit", command=self.root.destroy)
        button_quit.pack(side=tk.BOTTOM, fill=tk.X)
        self.x_label = x_label
        self.y_label = y_label
        self.plot_type = plot_type
        self.color = color
        self.x_plot = x_plot
        self.y_plot = y_plot
        self.df = df
        self.title = title
        self.tree = None
        self.highlighted_point = None
        self.ax = None
        self.default_directory = None

    def plot(self):
        self.logger.info("Creating plot")

        self.set_toolbar()

        plt.style.use('ggplot') 
        self.ax = self.fig.add_subplot()

        self.ax.ticklabel_format(useOffset=False, style='plain', axis='both')

        
        if self.plot_type == 'line':
            self.ax.plot(self.df[self.x_plot], self.df[self.y_plot], color=self.color, marker='o')
        elif self.plot_type == 'scatter':
            self.ax.scatter(self.df[self.x_plot], self.df[self.y_plot], color=self.color)
        elif self.plot_type == 'bar':
            self.ax.bar(self.df[self.x_plot], self.df[self.y_plot], color=self.color)
        
        self.ax.set_xlabel(self.x_label, fontsize=12)
        self.ax.set_ylabel(self.y_label, fontsize=12)
        self.ax.set_title(self.title, fontsize=14)
        self.ax.grid(True)
        self.ax.tick_params(axis='x', rotation=45)
        self.ax.legend()  

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.canvas.draw()

        self.add_table()


    def set_toolbar(self):
        toolbar = CustomToolbar(self.canvas, self.root, pack_toolbar=False)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.update()

    def add_table(self):
        self.tree = ttk.Treeview(self.root)

        self.tree['columns'] = ("X-Value", "Y-Value")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("X-Value", anchor=tk.W, width=80)
        self.tree.column("Y-Value", anchor=tk.W, width=80)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("X-Value", text=self.x_label, anchor=tk.W)
        self.tree.heading("Y-Value", text=self.y_label, anchor=tk.W)

        for i, (x, y) in enumerate(zip(self.df[self.x_plot], self.df[self.y_plot])):
            self.tree.insert(parent='', index='end', iid=i, text='', values=(x, y))

        self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_selection_change)


    def on_tree_selection_change(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            index = int(selected_items[0])
            self.highlight_plot_point(index)
        
    def highlight_plot_point(self, index):
        self.clear_highlight()


        x, y = self.df[self.x_plot].iloc[index], self.df[self.y_plot].iloc[index]

        self.ax = self.fig.self.axes[0]  # Get the current self.axes
        self.highlighted_point = self.ax.plot(x, y, marker='o', markersize=10, color='red')  # Customize marker size and color as needed

        self.canvas.draw()

    def clear_highlight(self):
        try:
            if self.highlighted_point:
                self.highlighted_point[0].remove()
                self.highlighted_point = None
                self.canvas.draw()
            self.logger.info("Highlight cleared")
        except Exception as e:
            self.logger.error(f"Error clearing highlight: {e}")

class CustomToolbar(NavigationToolbar2Tk):
    def save_figure(self, *args):
        # Define the filetypes you want to save as
        filetypes = self.canvas.get_supported_filetypes_grouped()
        tk_filetypes = [
            (name, " ".join(f"*.{ext}" for ext in exts))
            for name, exts in sorted(filetypes.items())
        ]

        #initial directory to open in the dialog
        initialdir = os.path.expanduser(plt.rcParams['savefig.directory'])
        # Determine the initial file name to suggest in the dialog
        initialfile = os.path.splitext(self.canvas.get_default_filename())[0]

        # Open a file dialog and ask the user for a filename to save as
        fname = asksaveasfilename(
            master=self.canvas.get_tk_widget().master,
            title='Save the figure',
            initialdir=initialdir,
            initialfile=initialfile,
            defaultextension='png',
            filetypes=tk_filetypes
        )

        # Check if a filename was provided
        if fname:
            if not any(fname.endswith(f'.{ext}') for exts in filetypes.values() for ext in exts):
                fname += '.png'
            try:
                self.canvas.figure.savefig(fname)
                print("\n\nFile Created:", f" {fname}\n\n")
                plt.rcParams['savefig.directory'] = os.path.dirname(fname)
            except Exception as e:
                tk.messagebox.showerror("Error saving file", str(e))
        else:
            # User cancelled the dialog
            print("Save figure operation cancelled.")
class tkDropdown:
    def __init__(self, master, options_dict, row, column):
        self.options_dict = options_dict
        self.dropdown_var = tk.StringVar()

        # Create the dropdown menu
        self.dropdown = ttk.Combobox(master, textvariable=self.dropdown_var)
        self.dropdown['values'] = list(self.options_dict.keys())
        self.dropdown.grid(row=row, column=column)
        self.dropdown['state'] = 'normal'


        # Bind the selection event
        self.dropdown.bind('<<ComboboxSelected>>', self.update_dict)
        self.dropdown.bind('<KeyRelease>', self.filter_options)


    def update_dict(self, event):
        for key in self.options_dict:
            self.options_dict[key] = False

        selected_key = self.dropdown_var.get()
        if selected_key in self.options_dict:
            self.options_dict[selected_key] = True

    def get_selected_option(self):
        for key, value in self.options_dict.items():
            if value:
                return key
        return None

    def filter_options(self, event):
        typed = self.dropdown_var.get()
        if typed == '':
            self.dropdown['values'] = list(self.options_dict.keys())
        else:
            filtered = [option for option in list(self.options_dict.keys()) if typed.lower() in option.lower()]
            self.dropdown['values'] = filtered

        self.dropdown.event_generate('<Down>')






            
        
