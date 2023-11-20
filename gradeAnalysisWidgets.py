import tkinter as tk
from tkinter import ttk
from functools import partial
import sys
import logging
import platform
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

        # Check if the file handler has been created already
        if not Logger._file_handler_created:
            # FileHandler for file output, set to 'w' mode to overwrite file on first creation
            file_handler = logging.FileHandler(log_file, mode='w')
            Logger._file_handler_created = True
        else:
            # Subsequent logger instances should append to the file
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

    def create_multiple_checkboxes(self, options, state, where, row, column):
        self.logger.info("Creating multiple checkboxes")
        for idx, (text, help_text) in enumerate(options.items(), start=row):
            self.create_checkbox(text, help_text, state, where, idx, column)
        self.logger.debug("Multiple checkboxes created")

    def get_selected_analyses(self):
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


        
    
