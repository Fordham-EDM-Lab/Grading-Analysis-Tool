import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from functools import partial
import mplcursors
import sys
import logging
import platform
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.filedialog import asksaveasfilename
from pandas.core.base import NoNewAttributesMixin
from ttkwidgets import autocomplete
import os
import subprocess
import matplotlib.colors as mcolors
import random
import seaborn
from matplotlib.backend_bases import MouseButton
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    MaxAbsScaler,
    Normalizer,
)
from matplotlib.backend_bases import MouseButton
import pandas as pd
import tkinter.scrolledtext as tkst
from functools import partial
from tkinter import colorchooser
import grade_analysis.dictionary
import csv
import grade_analysis.gradeAnalysisFunc
from matplotlib.lines import Line2D
import webcolors
import copy


def popup(title="", popup_text=""):
    messageBox = tk.Toplevel()
    label = tk.Label(messageBox, text=title)
    label.pack()

    show_help_info = tk.Label(messageBox, text=popup_text, justify="left")
    show_help_info.pack()

    button_close = tk.Button(messageBox, text="Close", command=messageBox.destroy)
    button_close.pack()

def name_to_hex(color_name):
    return webcolors.name_to_hex(color_name)


##For matplotlib uses
def get_non_red_colors():
    css4_colors = mcolors.CSS4_COLORS

    def hex_to_rgb(hex_color):
        """Convert hex color to RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def calculate_brightness(rgb_color):
        """Calculate the perceived brightness of an RGB color."""
        r, g, b = rgb_color
        return (0.299 * r + 0.587 * g + 0.114 * b)

    non_red_colors = [
        (name, hex) for name, hex in css4_colors.items()
        if "red" not in name.lower() and calculate_brightness(hex_to_rgb(hex)) <= 200
    ]


    non_red_colors = [i[0] for i in non_red_colors]
    non_red_colors.remove('rebeccapurple')
    return non_red_colors


def get_non_red_colors_name_hex():
    css4_colors = mcolors.CSS4_COLORS

    non_red_colors = {
        name: hex for name, hex in css4_colors.items() if "red" not in name.lower()
    }

    return non_red_colors


def get_nonseaborn_styles():
    plot_styles = plt.style.available

    non_seaborn_styles = [
        color for color in plot_styles if "seaborn" not in color.lower()
    ]

    return non_seaborn_styles


def get_random_values(input_list, number_of_values=7):
    if len(input_list) < number_of_values:
        raise ValueError(
            f"Input list must contain at least {number_of_values} elements."
        )

    return random.sample(input_list, number_of_values)


def normalize_dataframe_column(dataframe, column, normalization_type):
    if column not in dataframe.columns:
        print(f"Column '{column}' not found in the dataframe.")
        return

    normalization_functions = {
        "minmax": lambda x: MinMaxScaler().fit_transform(x),
        "zscore": lambda x: StandardScaler().fit_transform(x),
        "robust": lambda x: RobustScaler().fit_transform(x),
        "maxabs": lambda x: MaxAbsScaler().fit_transform(x),
        "log": lambda x: np.log(
            x - np.min(x) + 1
        ),  # Log scaling with shift to handle non-positive values
    }

    if normalization_type in normalization_functions:
        # Normalize the column and add the normalized column to the dataframe
        scaled_data = normalization_functions[normalization_type](dataframe[[column]])
        dataframe[f"{normalization_type} Normalized {column}"] = (
            scaled_data.squeeze()
        )  # Use squeeze to ensure correct dimensionality
    else:
        print(f"Normalization type '{normalization_type}' is not supported.")


class Logger(logging.Logger):
    _file_handler_created = False  # Class-level attribute

    def __init__(self, name, level=logging.DEBUG, log_file=".log.log"):
        super().__init__(name, level)

        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%m/%d/%Y, [%H:%M:%S]",
        )
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        if not Logger._file_handler_created:
            file_handler = logging.FileHandler(log_file, mode="w")
            Logger._file_handler_created = True
        else:
            # Subsequent logger instances should append to the file
            file_handler = logging.FileHandler(log_file, mode="a")

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

    def make_confirm_button(
        self, where, title="Confirm", command=None, row=int, column=int, helptip=""
    ):
        self.logger.info(
            f"Creating confirm button titled '{title}' at row {row}, column {column}"
        )
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
        self.logger.debug(
            f"Binding tooltip events to widget with tooltip text: '{text}'"
        )
        tooltip = ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())
        self.logger.debug("Tooltip events bound successfully")


class TableWidget:
    def __init__(self):
        self.logger = Logger(__name__)  # Create a logger for this class
        self.table = None
        self.logger.info("TableWidget instance initialized")

    def generic_tableview_widget(
        self, where, row=int, column=int, title="", colHeading="", helptip=""
    ):
        self.logger.info(
            f"Creating table view widget titled '{title}' with columns '{colHeading}' at row {row}, column {column}"
        )
        self.table = ttk.Treeview(
            where, columns=colHeading, show="headings", selectmode=tk.BROWSE
        )
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
            values = item_info.get("values", ())
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
        self.logger.debug(
            f"Binding tooltip events to widget with tooltip text: '{text}'"
        )
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

    def generic_thresholds_widget(
        self, where, state=str, text=str, row=int, column=int, help=str
    ):
        self.logger.info(
            f"Creating threshold widget with label '{text}' at row {row}, column {column}"
        )
        x_pad = len(text) * 7
        self.label = tk.Label(where, text=text)
        self.label.grid(row=row, column=column, sticky=tk.W)
        self.entry = tk.Entry(where, width=3)
        self.entry.config(state=state)
        self.entry.grid(row=row, column=column, sticky=tk.W, padx=(x_pad, 0))
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
        self.logger.debug(
            f"Binding tooltip events to widget with tooltip text: '{text}'"
        )
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
        checkbox = tk.Checkbutton(
            where, state=state, text=text, variable=checkbox_state
        )
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
        self.logger.debug(
            f"Binding tooltip events to widget '{widget}' with tooltip text: '{text}'"
        )
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
            os.startfile(self.file_path)  # Built-in Windows call
            self.logger.debug("Opened file using os.startfile")
        elif current_platform == "Darwin":  # macOS
            subprocess.Popen(["open", self.file_path])
            self.logger.debug("Opened file on macOS using open")
        else:
            self.logger.warning("Unsupported platform for file opening")
            return



class ChangeTitles:
    def __init__(self, initial_x_title="x-axis", initial_y_title="y-axis", initial_plot_title="plot title"):
        if not all(isinstance(title, str) for title in [initial_x_title, initial_y_title, initial_plot_title]):
            print("Only strings are accepted for titles.")
            return

        self.x_title = initial_x_title
        self.x_change_flag = True
        self.y_title = initial_y_title
        self.y_change_flag = True
        self.plot_title = initial_plot_title
        self.plot_change_flag = True

    def x_title_change(self, new_x_title):
        if isinstance(new_x_title, str) and self.x_change_flag:
            self.x_title = new_x_title
        else:
            return
            #print(f"type is {type(new_x_title)}, flag is {self.x_change_flag}")

    def y_title_change(self, new_y_title):
        if isinstance(new_y_title, str) and self.y_change_flag:
            self.y_title = new_y_title
        else:
            return
            #print(f"type is {type(new_y_title)}, flag is {self.y_change_flag}")

    def plot_title_change(self, new_plot_title):
        if isinstance(new_plot_title, str) and self.plot_change_flag:
            self.plot_title = new_plot_title
        else:
            return
            #print(f"type is {type(new_plot_title)}, flag is {self.plot_change_flag}")

    def get_x_title(self):
        return self.x_title

    def get_y_title(self):
        return self.y_title

    def get_plot_title(self):
        return self.plot_title

    def x_flag(self, state: bool):
        if not isinstance(state, bool):
            print('state is not of bool type')
            return 
        self.x_change_flag = state

    def y_flag(self, state: bool):
        if not isinstance(state, bool):
            print('state is not of bool type')
            return
        self.y_change_flag = state

    def plot_flag(self, state: bool):
        if not isinstance(state, bool):
            print('state is not of bool type')
            return
        self.plot_change_flag = state


class tkMatplot:
    def __init__(
        self,
        window_width=800,
        window_height=700,
        df=None,
        title = ChangeTitles(),
        plot_type=None,
        color=None,
        colors=None,
        legend=None,
        x_plot=None,
        y_plot=None,
        data_type=None,
        output_directory=None,
    ):
        
        self.logger = Logger(__name__)
        self.logger.info("Initializing tkMatplot class")
        self.root = tk.Tk()
        self.root.wm_title("Grading Analysis Plotter")

        self.logger.info("Initializing tkMatplot class")

        self.root.geometry(f"{window_width}x{window_height}")
        self.logger.info(f"Setting window size to {window_width}x{window_height}")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button_quit = tk.Button(
            master=self.root, text="Quit", command=self.root.destroy
        )
        button_quit.pack(side=tk.BOTTOM, fill=tk.X)
        self.plot_type = plot_type
        self.color = color
        self.x_plot = x_plot
        self.y_plot = y_plot
        self.legend = legend
        self.df = df
        self.original_index = self.df.index.copy()
        self.title = title
        self.tree = None
        self.highlighted_point = None
        self.ax = None
        self.default_directory = os.path.join(output_directory, 'Binexport.txt') if output_directory else (os.getcwd(), 'Binexport.txt')
        self.left_frame = None
        self.right_frame = None
        self.plot_options = None
        self.plot_colors = None
        self.scale_options = None
        self.scale = "linear"
        self.accept_change_button = None
        self.toolbar = None
        self.plot_style = "grayscale"
        self.plot_style_options = None
        self.change_sort_order = None
        self.change_titles = None
        self.sort_order = "none"
        self.normalize_column_options = None
        self.normalize_option = "none"
        self.data_type = data_type
        self.graphing_bin_check = False
        self.numerical_bin_check = False
        self.use_color_groups = False
        self.bin_selected_groups = None
        self.reset_tuple = (
            copy.deepcopy(title),
            copy.deepcopy(window_width),
            copy.deepcopy(window_height),   
            copy.deepcopy(df),              
            copy.deepcopy(plot_type),
            copy.deepcopy(color),         
            copy.deepcopy(colors),          
            copy.deepcopy(x_plot),          
            copy.deepcopy(y_plot),          
            copy.deepcopy(data_type),       
            copy.deepcopy(self.scale),      
            copy.deepcopy(self.plot_style), 
            copy.deepcopy(self.sort_order), 
            copy.deepcopy(self.normalize_option),
            copy.deepcopy(self.legend),
        )
        self.help_button = None
        self.logger.info("tkMatplot class initialized")

    def sort_dataframe(self, df, sort_order: str = 'descending', by: str = ''):
        if self.sort_order == "ascending":
            df.sort_values(by=by, ascending=True, inplace=True)
        elif self.sort_order == "descending":
            df.sort_values(by=by, ascending=False, inplace=True)
        elif self.sort_order == "random":
            df = df.sample(frac=1).reset_index(drop=True)
        elif self.sort_order == "none":
            df = df.loc[self.original_index]
        return df



    def plot(self):

        self.logger.info("Creating plot")

        self.fig.clear()


        if self.toolbar is None:
            self.set_toolbar()

        plt.style.use(self.plot_style)
        self.ax = self.fig.add_subplot()

        self.ax.ticklabel_format(useOffset=False, style="plain", axis="both")

        df = self.df

        current_yplot = self.y_plot


        self.logger.info(f"Plotting data using {self.plot_type} plot type")

        if self.graphing_bin_check:
            df = self.custom_bin_agg(df, self.bin_selected_groups)
            self.logger.info("Creating plot with custom bin aggregation")
            self.logger.info(f"Sort order: {self.sort_order}")
            df = self.sort_dataframe(df, sort_order=self.sort_order, by=current_yplot)

            if self.normalize_option != "none":
                self.logger.info(f"Normalizing data using '{self.normalize_option}' method")
                normalize_dataframe_column(df, current_yplot, self.normalize_option)
                current_yplot = f"{self.normalize_option} Normalized {current_yplot}"

                self.logger.info(f"Normalized column: {current_yplot}")

            x_data = df['Bin'] 
            y_data = df[current_yplot]  
            colors = df['Color']  
            self.legend = dict(zip(df['Color'], df['Bin']))
            
            if self.plot_type == "line":
                line_plot = self.ax.plot(x_data, y_data, marker="o", linestyle='-', color='black')
                cursor = mplcursors.cursor(line_plot, hover=True)
            elif self.plot_type == "scatter":
                scatter_plot = self.ax.scatter(x_data, y_data, c=colors, label='Bins')
                cursor = mplcursors.cursor(scatter_plot, hover=True)
            elif self.plot_type == "bar":
                bar_plot = self.ax.bar(x_data, y_data, color=colors, align='center')
                cursor = mplcursors.cursor(bar_plot, hover=True)



        elif self.numerical_bin_check and self.bin_selected_groups is not None and not self.use_color_groups:
            self.logger.info("Creating plot with numerical bin aggregation")
            df = self.bin_agg_tuples(df, self.bin_selected_groups, self.x_plot)
            self.logger.info(f"Sort order: {self.sort_order}")
            df = self.sort_dataframe(df, self.sort_order, current_yplot)

            if self.normalize_option != "none":
                self.logger.info(f"Normalizing data using '{self.normalize_option}' method")
                normalize_dataframe_column(df, current_yplot, self.normalize_option)
                current_yplot = f"{self.normalize_option} Normalized {current_yplot}"
                self.logger.info(f"Normalized column: {current_yplot}")

            for bin_data in df.iterrows():
                bin_name = bin_data[1]['Bin']
                x_data = [bin_name]
                y_data = [bin_data[1][current_yplot]]

                if self.plot_type == "line":
                    line_plot = self.ax.plot(x_data, y_data, marker="o", label=bin_name)
                    cursor = mplcursors.cursor(line_plot, hover=True)
                elif self.plot_type == "scatter":
                    scatter_plot = self.ax.scatter(x_data, y_data, label=bin_name)
                    cursor = mplcursors.cursor(scatter_plot, hover=True)
                elif self.plot_type == "bar":
                    bar_plot = self.ax.bar(x_data, y_data, label=bin_name)
                    cursor = mplcursors.cursor(bar_plot, hover=True)


        else:
            self.logger.info("Creating plot without bin aggregation")
            if self.use_color_groups:
                df = self.color_bin_agg(self.df)
                df['legend'] = df['color'].map(self.legend)

            self.logger.info(f"Sort order: {self.sort_order}")
            self.original_index = df.index.copy()
            df = self.sort_dataframe(df, sort_order=self.sort_order, by=current_yplot)

            if self.normalize_option != "none":
                self.logger.info(f"Normalizing data using '{self.normalize_option}' method")
                normalize_dataframe_column(df, current_yplot, self.normalize_option)
                current_yplot = f"{self.normalize_option} Normalized {current_yplot}"
                self.logger.info(f"Normalized column: {current_yplot}")

            x_data = df['legend'] if self.use_color_groups else df[self.x_plot]

            if self.plot_type == "line":
                line_plot = self.ax.plot(x_data, df[current_yplot], color=df['color'].iloc[0])
                cursor = mplcursors.cursor(line_plot, hover=True)
            elif self.plot_type == "scatter":
                scatter_plot = self.ax.scatter(x_data, df[current_yplot], color=df['color'])
                cursor = mplcursors.cursor(scatter_plot, hover=True)
            elif self.plot_type == "bar":
                bar_plot = self.ax.bar(x_data, df[current_yplot], color=df['color'])
                cursor = mplcursors.cursor(bar_plot, hover=True)
                self.ax.set_ylim(0, df[current_yplot].max() + 1)

        if cursor:
            @cursor.connect("add")
            def on_add(sel):
                index = sel.index
                annotation_text = []
                excluded_columns = [
                    'kurtosis', 'skewness', 'CoV(%)', 'ModeGPA', 'A', 'A-', 'B+', 'B', 'B-', 
                    'C+', 'C', 'C-', 'D', 'F', 'color', 'avg_gpa_change', 'avg_gpaw_change', "weighted_underperformance",
                    "zscore Normalized GPAW"
                ]
                for col in df.columns:
                    if col not in excluded_columns:
                        col_value = df[col].iloc[index]
                        annotation_text.append(f"{col}: {col_value}")
                sel.annotation.set_text("\n".join(annotation_text))


        legend_elements = [
            Line2D([0], [0], color=color, lw=4, label=label)
            for color, label in self.legend.items()
        ]

        self.ax.legend(handles=legend_elements, title="Legend")

        self.title.y_title_change(str(current_yplot))
        self.ax.set_xlabel(self.title.get_x_title(), fontsize=14)
        self.ax.set_ylabel(self.title.get_y_title(), fontsize=16)
        self.ax.set_title(self.title.get_plot_title(), fontsize=14)

        self.ax.grid(False)
        self.ax.tick_params(axis="x", rotation=80, labelsize=10)


        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax.set_yscale(self.scale)

        self.canvas.draw()

        if self.graphing_bin_check:
            xplot='Bin'
        elif self.use_color_groups:
            xplot='legend'
        else:
            xplot=self.x_plot

        if self.left_frame is not None:
            self.left_frame.destroy()
        self.add_table(df=df, xplot=xplot ,yplot=current_yplot)

        if self.right_frame is not None:
            self.right_frame.destroy()
        
        self.change_graph_options()
        self.accept_change_button.config(state="disabled")

        self.fig.tight_layout(rect=[1,1,1,1])


        self.canvas.draw()



    def change_plot_type(self):
        if self.plot_type != self.plot_options.get_selected_option():
            self.plot_type = self.plot_options.get_selected_option()
        if self.scale != self.scale_options.get_selected_option():
            self.scale = self.scale_options.get_selected_option()
        if self.plot_style != self.plot_style_options.get_selected_option():
            self.plot_style = self.plot_style_options.get_selected_option()
        if self.sort_order != self.change_sort_order.get_selected_option():
            self.sort_order = self.change_sort_order.get_selected_option()
        if self.normalize_option != self.normalize_column_options.get_selected_option():
            self.normalize_option = self.normalize_column_options.get_selected_option()

        self.plot()

    def reset_state(self):
        (
            title,
            window_width,
            window_height,
            df,
            plot_type,
            color,         
            colors,        
            x_plot,
            y_plot,
            data_type,
            scale,
            plot_style,
            sort_order,
            normalize_option,
            legend,
        ) = self.reset_tuple

        self.root.geometry(f"{window_width}x{window_height}")
        self.df = df
        self.plot_type = plot_type
        self.color = color
        self.colors = colors
        self.x_plot = x_plot
        self.y_plot = y_plot
        self.title = title
        self.scale = scale
        self.plot_style = plot_style
        self.sort_order = sort_order
        self.normalize_option = normalize_option
        self.data_type = data_type
        self.numerical_bin_check = False
        self.graphing_bin_check = False
        self.legend = legend
        self.use_color_groups = False
        self.title = title

        self.plot()


    def change_legend_plot_colors(self):
        selected_color = colorchooser.askcolor(title="Choose color")[1]
        target_color = self.plot_colors.get_selected_option()
        self.df['color'] = self.df['color'].apply(
            lambda x: selected_color if x == target_color else x)
        for old_color, label in list(self.legend.items()):
            if old_color == target_color:
                del self.legend[old_color]
                self.legend[selected_color] = label
                break
        self.plot_colors.update_options(list(self.df['color'].unique()), {x: x for x in self.df['color'].unique()})
        self.accept_change_button.config(state=tk.NORMAL)

    def change_graph_options(self):
        self.logger.info("Creating graph options")
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

        self.logger.info("Creating Plot Type Options")
        self.plot_options = tkOptionMenu(
            master=self.right_frame,
            options=["line", "scatter", "bar"],
            pre_selected=f"{self.plot_type}",
            label_text="Change Plot Type",
            command=self.set_normal_state,
        )
        self.plot_options.grid(row=1, column=1, padx=(0, 20))
        self.logger.info("Plot Type Options created")

        self.logger.info("Creating Plot Color Options")
        self.plot_colors = tkOptionMenu(
            master=self.right_frame,
            options=self.df['color'].unique(),
            pre_selected=f"{list(self.df['color'].unique())[0]}",
            label_text="Change Plot Colors",
            command=self.change_legend_plot_colors,
            colors={x: x for x in self.df['color'].unique()},
        )
        self.plot_colors.grid(row=1, column=3, padx=(20, 0))
        self.logger.info("Plot Color Options created")

        self.logger.info("Creating Axis Scale Options")
        self.scale_options = tkOptionMenu(
            master=self.right_frame,
            options=[
                "linear",
                "log",
                "symlog",
                "asinh",
            ],
            pre_selected=self.scale,
            label_text="Axis Scale",
            command=self.set_normal_state,
        )
        self.scale_options.grid(row=3, column=1)
        self.logger.info("Axis Scale Options created")

        self.logger.info("Creating Plot Style Options")
        self.plot_style_options = tkOptionMenu(
            master=self.right_frame,
            options=get_random_values(get_nonseaborn_styles()),
            pre_selected=self.plot_style,
            label_text="Change Plot Style",
            command=self.set_normal_state,
        )
        self.plot_style_options.grid(row=3, column=3)
        self.logger.info("Plot Style Options created")

        self.accept_change_button = tk.Button(
            self.right_frame,
            text="Accept",
            command=self.change_plot_type,
        )

        self.logger.info("Creating Sort Order Options")
        self.change_sort_order = tkOptionMenu(
            master=self.right_frame,
            options=["ascending", "descending", "random", 'none'],
            pre_selected=self.sort_order,
            label_text="Sort Order",
            command=self.set_normal_state,
        )

        self.change_sort_order.grid(row=5, column=1)
        self.logger.info("Sort Order Options created")

        self.change_titles_button = tk.Button(
            self.right_frame,
            text='Change A Title',
            command=self.change_title_popup
        )
        self.change_titles_button.grid(row=3, column=5)

        self.logger.info("Creating Normalize Column Options")
        self.normalize_column_options = tkOptionMenu(
            master=self.right_frame,
            options=["none", "minmax", "zscore", "robust", "maxabs", "log"],
            pre_selected=self.normalize_option,
            label_text="Normalize Option",
            command=self.set_normal_state,
        )
        self.logger.info("Normalize Column Options created")

        self.normalize_column_options.grid(row=5, column=3)

        self.reset_button = tk.Button(self.right_frame, text='Reset Plot', command = self.reset_state)
        self.reset_button.grid(row=6, column=3)

        self.accept_change_button.grid(row=8, column=2)

        self.help_button = tk.Button(self.right_frame, text='Help', command = self.help_create)
        self.help_button.grid(row=8, column=5)


        if self.df[self.x_plot].dtype == "object":
            self.logger.info("Creating Bin Button")
            self.bin_button = tkOptionMenu(master=self.right_frame, options=['Manual', 'By Colors'], pre_selected='Manual', command=self.str_bin_creation, label_text='Create Groupings')
            self.bin_button.grid(row=6, column=1)
        else:
            self.logger.info("Creating Numerical Bin Button")
            self.bin_button = tkOptionMenu(master=self.right_frame, options=['Manual', 'By Colors'], pre_selected='Manual', command=self.num_bin_creation, label_text='Create Groupings')
            self.bin_button.grid(row=6, column=1)
        
        self.logger.info("Bin Button created")

    def change_title_popup(self):
        def apply_changes():

            x_entry_t = x_entry.get()
            y_entry_t = y_entry.get()
            plot_entry_t = plot_entry.get()

            self.title.x_title_change(x_entry_t)
            self.title.y_title_change(y_entry_t)
            self.title.plot_title_change(plot_entry_t)

            self.title.x_flag(False)
            self.title.y_flag(False)
            self.title.plot_flag(False)

            popup.destroy()
            self.set_normal_state()

        popup = tk.Toplevel(self.root)
        popup.title("Change Plot Titles")

        # X-Axis Title
        ttk.Label(popup, text="X-Axis Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        x_entry = ttk.Entry(popup)
        x_entry.grid(row=0, column=1, padx=10, pady=5)
        x_entry.insert(0, self.title.get_x_title())  

        # Y-Axis Title
        ttk.Label(popup, text="Y-Axis Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        y_entry = ttk.Entry(popup)
        y_entry.grid(row=1, column=1, padx=10, pady=5)
        y_entry.insert(0, self.title.get_y_title())

        # Plot Title
        ttk.Label(popup, text="Plot Title:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        plot_entry = ttk.Entry(popup)
        plot_entry.grid(row=2, column=1, padx=10, pady=5)
        plot_entry.insert(0, self.title.get_plot_title())

        # Apply Button
        ttk.Button(popup, text="Apply", command=apply_changes).grid(row=3, column=0, columnspan=2, pady=10)

        popup.grab_set()
        popup.wait_window()

    def help_create(self):
        self.logger.info("Creating Help Popup")
        popup(self, title='Help', popup_text=
            """
            1. Change Plot Type: Allows you to select between bar, scatter, or line plots\n
            2. Axis Scale: Scales the axis on the selected option\n
            3. Sort Order: Sort the graph on the selected option\n
            4. Change Plot Color: Changes the plot color based on the selected color\n
            5. Change Plot Style: Changes background plot design\n
            6. Normalize option: Normalizes the plots yaxis\n
            """)
        self.logger.info("Help Popup created")

    def num_bin_creation(self):
        if self.bin_button.get_selected_option() == 'Manual':
            self.numbin = NumericalBinApp(self.right_frame, row=7, column=1, set_low=min(self.df[self.x_plot]), set_high=max(self.df[self.x_plot]))
            self.numbin.set_callback(self.on_bins_created)
            self.use_color_groups = False
            self.logger.info("Numerical Bin Button created")
        else:
            self.use_color_groups = True
            self.plot()

    def str_bin_creation(self):
        if self.bin_button.get_selected_option() == 'Manual':
            self.df
            bin_popup = BinPopup(self.root, {key: False for key in self.df[self.x_plot]}, callback=self.on_bins_created, path=self.default_directory)
            self.use_color_groups = False
        else:
            self.use_color_groups = True
            self.plot()

        self.logger.info("Creating Bin Popup")

    def on_bins_created(self, selected_groups):
        if self.df[self.x_plot].dtype == "object":
            self.graphing_bin_check = True
        else:
            self.numerical_bin_check = True

        self.bin_selected_groups = selected_groups
        self.plot()
        if self.numerical_bin_check:
            self.numbin.destroy()

    def set_normal_state(self):
        self.accept_change_button.config(state=tk.NORMAL)

    def set_toolbar(self):
        self.logger.info("Creating toolbar")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar.update()
        self.logger.info("Toolbar created")


    def add_table(self, df,xplot, yplot):
        self.logger.info("Creating table")
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill="both", expand=True)
        self.tree = ttk.Treeview(self.left_frame)

        self.tree["columns"] = ("X-Value", "Y-Value")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("X-Value", anchor=tk.W, width=80)
        self.tree.column("Y-Value", anchor=tk.W, width=80)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("X-Value", text=self.title.get_x_title(), anchor=tk.W)
        self.tree.heading("Y-Value", text=self.title.get_y_title(), anchor=tk.W)

        self.logger.info("Inserting data into table")
        for i, (x, y) in enumerate(zip(df[xplot], df[yplot])):
            self.tree.insert(parent="", index="end", iid=i, text="", values=(x, y))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", partial(self.on_tree_selection_change, df, xplot, yplot))
        self.logger.info("Table created")

    def update_table(self, df, xplot, yplot):
        self.logger.info("Updating table")
        self.tree.delete(*self.tree.get_children())
        for i, (x, y) in enumerate(zip(df[xplot], df[yplot])):
            self.tree.insert(parent="", index="end", iid=i, text="", values=(x, y))
        self.logger.info("Table updated")

    def color_bin_agg(self, df):
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        agg_list = ['Enrollments', 'GPA', 'GPAW', 'stddev', 'kurtosis', 'skewness', 'Sections', 'Courses', 'GPAGroupCounts'] + grades
        agg_dict = {agg: "mean" for agg in agg_list if agg in df.columns}
        df_agg = df.groupby('color', observed=True).agg(agg_dict).reset_index()
        float_cols = df_agg.select_dtypes(include="float").columns
        df_agg[float_cols] = df_agg[float_cols].round(3)
        return df_agg

    def custom_bin_agg(self, df, selected_groups):
        self.logger.info("Aggregating data based on selected groups")
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        agg_list = ['Enrollments', 'GPA', 'GPAW', 'stddev', 'kurtosis', 'skewness', 'Sections', 'Courses', 'GPAGroupCounts'] + grades
        agg_dict = {agg: "mean" for agg in agg_list if agg in df.columns}
        self.logger.info("Aggregated data dict ready")

        df['Bin'] = None
        df['Color'] = None

        self.logger.info("Assigning bins and colors to data")
        for group, colors in selected_groups:
            bin_name = "[" + ", ".join(group) + "]"
            for item in group:
                df.loc[df[self.x_plot] == item, 'Bin'] = bin_name
                df.loc[df[self.x_plot] == item, 'Color'] = colors[0]

        df['Bin'] = df['Bin'].fillna('others')
        df['Color'] = df['Color'].fillna('grey')  # Default color for 'others' bin

        colors = df[['Bin', 'Color']].drop_duplicates().set_index('Bin')

        self.logger.info("Grouping data based on bins")
        df_agg = df.groupby('Bin', observed=True).agg(agg_dict).reset_index()

        bin_counts = df.groupby('Bin').size().reset_index(name='bin_count')

        df_agg = df_agg.merge(bin_counts, on='Bin', how='left')

        df_agg = df_agg.join(colors, on='Bin')

        float_cols = df_agg.select_dtypes(include="float").columns
        df_agg[float_cols] = df_agg[float_cols].round(3)
        self.logger.info("Data grouped and aggregated successfully")
        self.original_index = df_agg.index.copy()

        return df_agg


    def bin_agg_tuples(self, df, bin_tuples, x_plot):
        self.logger.info("Aggregating data based on numerical bin tuples")
        agg_list=['Enrollments', 'GPA', 'stddev', 'kurtosis', 'skewness', 'Sections', 'Courses']
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        all_agg_cols = agg_list + grades
        agg_dict = {col: "mean" for col in all_agg_cols}
        self.logger.info("Aggregated data dict ready")
        edges = [t[0] for t in bin_tuples] + [bin_tuples[-1][1]]

        self.logger.info("Assigning bins to data")
        df['Bin'] = pd.cut(df[x_plot], bins=edges, right=False,
                        labels=[f"{t[0]}-{t[1]}" for t in bin_tuples], include_lowest=True)

        self.logger.info("Grouping data based on bins")
        df_agg = df.groupby('Bin', observed=True).agg(agg_dict)
        bin_counts = df.groupby('Bin').size().rename('bin_count')
        df_agg = df_agg.join(bin_counts)
        df_agg.reset_index(inplace=True)

        float_cols = df_agg.select_dtypes(include="float").columns
        df_agg[float_cols] = df_agg[float_cols].round(3)
        self.original_index = df_agg.index.copy()

        return df_agg


    def on_tree_selection_change(self,df, xplot, yplot ,event):
        self.logger.info("Tree selection changed")
        selected_items = self.tree.selection()
        if selected_items:
            index = int(selected_items[0])
            self.highlight_plot_point(index, df, xplot, yplot)

    def highlight_plot_point(self, index, df, xplot, yplot):
        self.clear_highlight()

        x, y = df[xplot].iloc[index], df[yplot].iloc[index]

        self.ax = self.fig.axes[0]  # Get the current self.axes
        self.highlighted_point = self.ax.plot(
            x, y, marker="o", markersize=10, color="red"
        )  # Customize marker size and color as needed
        self.logger.info(f"Highlighted point at index {index} with x={x}, y={y}")

        self.canvas.draw()

    def clear_highlight(self):
        try:
            if self.highlighted_point:
                self.highlighted_point[0].remove()
                self.highlighted_point = None
                self.logger.info("Highlight cleared")
                self.canvas.draw()
        except Exception as e:
            self.logger.error(f"Error clearing highlight: {e}")


class NumericalBinApp:
    def __init__(self, root, row=0, column=0, set_low=None, set_high=None):
        self.root = root
        self.logger = Logger(__name__)
        self.set_low = set_low
        self.set_high = set_high


        self.create_widgets(row, column)
        self.callback = None  # Initialize callback function to None

    def create_widgets(self, row, column):
        self.logger.info("Creating numerical bin widgets")
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.grid(row=row, column=column, padx=5, pady=5, sticky="w")  # Stick to west (left)

        self.logger.info("Creating Min, Max, and Step input fields")
        ttk.Label(self.input_frame, text="Min:").grid(row=0, column=0, padx=5, pady=5)
        self.min_entry = ttk.Entry(self.input_frame, width=10)
        self.min_entry.insert(0, self.set_low)
        self.min_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Max:").grid(row=0, column=2, padx=5, pady=5)
        self.max_entry = ttk.Entry(self.input_frame, width=10)
        self.max_entry.insert(0, self.set_high)
        self.max_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Step:").grid(row=0, column=4, padx=5, pady=5)
        self.step_entry = ttk.Entry(self.input_frame, width=10)
        self.step_entry.grid(row=0, column=5, padx=5, pady=5)

        # Generate button
        self.generate_button = ttk.Button(self.input_frame, text="Generate", command=self.generate_bins)
        self.generate_button.grid(row=0, column=6, padx=5, pady=5)
        self.logger.info("Numerical bin widgets created")

    def set_callback(self, callback):
        self.logger.info(f"Setting callback function to {callback}")
        self.callback = callback

    def generate_bins(self):
        try:
            self.logger.info("Generating numerical bins")
            min_value = float(self.min_entry.get())
            max_value = float(self.max_entry.get())
            step_value = float(self.step_entry.get())
            bins = self.numerical_bin(min_value, max_value, step_value)

            if self.callback:  # If a callback function is set, use it
                self.callback(bins)
        except ValueError:
            if self.callback:  # If a callback is set, let it handle errors
                self.logger.error("Error generating numerical bins")
                self.callback([])  # Pass an empty list to indicate error

    def numerical_bin(self, start, end, step):
        self.logger.info("Creating numerical bins")
        edges = np.arange(start, end + step, step)
        return [(round(edges[i], 2), round(edges[i + 1], 2)) for i in range(len(edges) - 1)]

    def destroy(self):
        """Destroy all widgets and dereference the object."""
        self.logger.info("Destroying NumericalBinApp instance and cleaning up resources")
        self.input_frame.destroy()
        self.callback = None  # Remove callback reference
        self.root = None  # Clear root reference
        self.logger = None  # Clear logger reference
        self.set_low = None
        self.set_high = None

class BinPopup():
    def __init__(self, master, options_dict, callback=None, path=None):
        self.logger = Logger(__name__)
        self.logger.info("Creating BinPopup instance")
        self.master = master
        self.options_dict = options_dict
        self.popup = tk.Toplevel(master=master)
        self.popup.title('Create Bins for Grouping')
        self.window_length = 500
        self.window_height = 500
        self.popup.geometry(f"{self.window_length}x{self.window_height}")
        self.callback=callback

        self.groups = []
        self.current_row = 0
        self.current_col = 0

        self.create_scrollable_area()
        self.create_bin_options()
        self.check_selection()


    def create_scrollable_area(self):
        self.logger.info("Creating scrollable area")
        # Create a canvas widget
        self.canvas = tk.Canvas(self.popup)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.v_scrollbar = tk.Scrollbar(self.popup, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar = tk.Scrollbar(self.popup, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Make the canvas expandable
        self.popup.grid_rowconfigure(0, weight=1)
        self.popup.grid_columnconfigure(0, weight=1)

        self.bind_scroll_events()

    def bind_scroll_events(self):
        self.logger.info("Binding scroll events")
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)


    def on_mouse_wheel(self, event):
        self.logger.info("Mouse wheel event detected")
        if event.num == 5 or event.delta == -120:  # Scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:  # Scroll up
            self.canvas.yview_scroll(-1, "units")


    def create_bin_options(self):
        self.logger.info("Creating bin options")
        self.group_frame = tk.Frame(self.scrollable_frame)
        self.group_frame.grid(row=self.current_row, column=self.current_col, sticky='nsew', padx=10, pady=10)

        self.logger.info("Creating Dropdown Options")
        self.dropdown = tkDropdown(
            master=self.group_frame, options_dict=self.options_dict, row=0, column=0,
            initial_message='Create a Group', allow_multiple_entries=True,
            scrolltextbox_height=5, scrolltextbox_width=20
        )
        self.dropdown.dropdown_grid(padx=60)

        self.logger.info("Creating Add Group and Accept buttons")
        self.add_group_button = tk.Button(self.group_frame, text="Add Group", command=self.add_group, state='disabled')
        self.add_group_button.grid(row=4, column=0, padx=10)

        self.accept_button = tk.Button(self.group_frame, text="Accept", command=self.accept, state='disabled')
        self.accept_button.grid(row=5, column=0, padx=10)

    def add_group(self):
        self.logger.info("Adding group")
        selected_options = list(self.dropdown.get_selected_options().keys())
        selected_colors = list(self.dropdown.get_selected_options().values())
        if selected_options and selected_colors:
            self.groups.append((selected_options, selected_colors))
            self.current_row += 1
            if self.current_row == 3:
                self.current_row = 0
                self.current_col += 3
            self.add_group_button.destroy()
            self.accept_button.destroy()
            self.create_bin_options()

    def check_selection(self):
        if self.dropdown.get_selected_options():
            self.set_state_normal()
        self.popup.after(1000, self.check_selection)

    def set_state_normal(self):
        self.add_group_button.config(state='normal')
        self.accept_button.config(state='normal')

    def get_selected_groups(self):
        self.logger.info("Getting selected groups")
        return self.groups

    def accept(self):
        self.logger.info("Accepting selected groups")
        selected_options = list(self.dropdown.get_selected_options().keys())
        selected_color = list(self.dropdown.get_selected_options().values())
        if selected_options and selected_color:
            self.groups.append((selected_options, selected_color))

        if self.callback:
            self.callback(self.groups)
        else:
            thing = self.get_selected_groups
        self.popup.destroy()


class tkOptionMenu(tk.Frame):
    def __init__(
        self,
        master,
        options,
        pre_selected,
        label_text,
        colors=None,
        command=None,
        *args,
        **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        self.logger = Logger(__name__)
        self.colors = (
            colors if colors is not None else {}
        )  # Default to empty dict if no colors provided

        self.variable = tk.StringVar(master=self, value=pre_selected)

        if command:
            self.command = command
            self.variable.trace_add("write", self.update_command)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT)

        self.option_menu = tk.OptionMenu(self, self.variable, *options)
        self.option_menu.pack(side=tk.LEFT)

        self.colorize_options()

    def get_selected_option(self):
        return self.variable.get()

    def is_dark(self, color_hex):
        """Determine if a color is dark based on its hex value."""
        if not (isinstance(color_hex, str) and color_hex.startswith("#") and len(color_hex) == 7):
            color_hex = name_to_hex(color_hex)
        try:
            r, g, b = (
                int(color_hex[1:3], 16),
                int(color_hex[3:5], 16),
                int(color_hex[5:7], 16),
            )
        except ValueError as e:
            raise ValueError(f"Failed to parse color hex: {color_hex}") from e
        
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 120

    def update_command(self, *args):
        self.logger.info("Updating command")
        if callable(self.command):
            self.command()

    def colorize_options(self):
        self.logger.info("Colorizing options")
        menu = self.option_menu["menu"]
        for index, label in enumerate(
            menu.entrycget(index, "label") for index in range(menu.index("end") + 1)
        ):
            color_hex = self.colors.get(
                label, "#FFFFFF"
            )  # Default to white if color not found
            menu.entryconfig(
                index,
                background=color_hex,
                foreground="#FFFFFF" if self.is_dark(color_hex) else "#000000",
            )
    def update_options(self, options, colors=None, pre_selected=None):
        """Update menu options and their colors dynamically."""
        self.logger.info("Updating options and colors")
        
        menu = self.option_menu["menu"]
        menu.delete(0, "end")
        
        if colors is not None:
            self.colors = colors
        
        for option in options:
            menu.add_command(
                label=option,
                command=lambda value=option: self.variable.set(value)
            )
        
        # Reapply colors to the menu
        self.colorize_options()
        
        # Update pre-selected option if provided
        if pre_selected is not None and pre_selected in options:
            self.variable.set(pre_selected)
        elif options:
            self.variable.set(options[0])



##Creates a combobox, with the ability to select items from a dropdown and see what you have selected in a textbox
##For viewing purpose. Also allows to export as text file
class tkDropdown():
    def __init__(
        self,
        master,
        options_dict,
        row,
        column,
        initial_message="Select an option",
        allow_multiple_entries=False,
        command=None,
        scrolltextbox_width = 20,
        scrolltextbox_height = 1,
    ):
        self.logger = Logger(__name__)
        self.master = master
        self.allow_multiple_entries = allow_multiple_entries
        self.options_dict = options_dict
        self.selected_options = {}
        self.row = row
        self.column = column
        self.initial_message = initial_message
        self.command = None
        self.scrolltextbox_width = scrolltextbox_width
        self.scrolltextbox_height = scrolltextbox_height
        self.current_key = None
        self.selected_color = get_random_values(get_non_red_colors())[0]
        self.color_labels = {}

        if command:
            self.command = command

        self.create_combobox()
        if self.allow_multiple_entries:
            self.create_selected_options_display()

    def dropdown_grid(self, **kwargs):
        self.logger.info("Creating dropdown grid")
        self.dropdown.grid(**kwargs)

    def choose_color(self):
        selected_color = colorchooser.askcolor(title="Choose color")[1]
        class_categories = [
            "Sciences",
            "Mathematics",
            "Humanities",
            "Languages",
            "Social Sciences",
            "Creative Arts",
            "Performing Arts",
            "Business",
            "Technology",
            "Health Sciences",
            "Physical Education",
            "Engineering",
            "Environmental Studies",
            "Law",
            "Education",
            "Computer Science",
            "Media Studies",
            "Philosophy",
            "Religious Studies",
            "Ethnic and Cultural Studies"
        ]

        if selected_color:
            self.color_chooser.config(bg=selected_color)
            label_value = simpledialog.askstring(title='Label Picker', prompt='What is this label?', initialvalue=random.choice(class_categories))
            self.color_labels[selected_color] = label_value
            self.selected_color = selected_color


    def create_combobox(self):
        self.logger.info("Creating combobox")
        self.dropdown = autocomplete.AutocompleteCombobox(
            self.master, completevalues=list(self.options_dict.keys())
        )
        self.dropdown.grid(row=self.row, column=self.column, sticky=tk.W)
        self.dropdown["state"] = "normal"
        self.dropdown.set(self.initial_message)

        if self.allow_multiple_entries:
            self.color_chooser = tk.Button(self.master, text="", command=self.choose_color, width=1, height=1, bg=self.selected_color)
            self.color_chooser.grid(row=self.row-1, column=self.column+1, sticky=tk.E)


        if self.command:
            self.dropdown.bind("<<ComboboxSelected>>", self.update_command)
        else:
            self.dropdown.bind("<<ComboboxSelected>>", self.update_dict)

        self.dropdown.bind("<Return>", self.update_dict)
        self.dropdown.bind("<Tab>", self.update_dict)

    def create_selected_options_display(self):
        self.logger.info("Creating selected options display")
        self.selected_options_label = tkScrolledtextBox(
            self.master, self.row + 1, self.column,
              self.scrolltextbox_width,
              self.scrolltextbox_height
        )

        tk.Button(
            self.master,
            text="Export Choices",
            command=self.export_to_csv,
        ).grid(row=self.row, column=self.column + 1 if self.column > 0 else 0)

        tk.Button(
            self.master,
            text="Import Choices",
            command=self.import_from_csv,
        ).grid(row=self.row +1, column=self.column + 1)

    def update_command(self, *args):
        selected_key = self.dropdown.get()

        if (
            selected_key in self.options_dict
            and selected_key not in self.selected_options
        ):
            self.selected_options[selected_key] = ''

        if callable(self.command):
            self.command()

    def update_dict(self, event):
        selected_key = self.dropdown.get()
        if self.current_key is not None and grade_analysis.dictionary.is_option_analysis(selected_key):
            grade_analysis.dictionary.change_analysis_value(self.current_key, False)
        self.current_key = selected_key
        if (
            selected_key in self.options_dict
            and selected_key not in self.selected_options
        ):
            self.selected_options[selected_key] = self.selected_color
            self.options_dict[selected_key] = True
            if self.allow_multiple_entries:
                self.selected_options_label.add_text(f"{selected_key},\n")
                self.dropdown.set("")
            else:
                self.dropdown.set(selected_key)

    def get_selected_options(self):
        return self.selected_options

    def get_option_labels(self):
        return self.color_labels

    def isEmpty(self):
        self.logger.info("Checking if selected options is empty")
        return not self.selected_options

    def head_of_options(self):
        return list(self.options_dict.keys())[1]
    
    def head_of_selected_options(self):
        return list(self.selected_options.keys())[1]

    def clearList(self):
        self.logger.info("Clearing selected options")
        self.selected_options.clear()
        self.selected_options_label.config(text="")

    def destroy(self):
        self.logger.info("Destroying dropdown")
        self.dropdown.destroy()
        if self.allow_multiple_entries:
            self.selected_options_label.destroy()
        self.selected_options.clear()


    def save_dataframe_with_dialog(self, df, return_path=False):
        """
        Opens a file dialog to let the user choose where to save the dataframe as a CSV.
        
        :param df: The pandas DataFrame to save.
        :param return_path: If True, returns the saved file path. Default is False.
        :return: The file path if return_path is True, otherwise None.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the Tkinter root window

        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV File",
            initialdir=os.getcwd(),
            initialfile="exported_categories.csv",
        )

        if file_path:  # Ensure user didn't cancel the dialog
            df.to_csv(file_path, index=False)
            print("\n\nFile Created:", f" {file_path}\n\n")
            return file_path if return_path else None
        else:
            print("File save canceled.")
            return None

    def export_to_csv(self):
        self.logger.info("Exporting selected options to text file")
        if self.allow_multiple_entries:
            csv_df = pd.DataFrame(list(self.selected_options.items()), columns=['Type', 'Color'])
            colors = list(self.color_labels.keys())
            labels = list(self.color_labels.values())
            csv_df['Label'] = pd.Series(labels)
            csv_df['LabelColor'] = pd.Series(colors)
            self.save_dataframe_with_dialog(csv_df)
        else:
            path = asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Text File",
                initialdir=os.getcwd(),
                initialfile="exported_category.txt",
            )
            with open(path, "w") as file:
                file.write(self.dropdown.get())
                print("\n\nFile Created:", f" {path}\n\n")


    def import_from_csv(self):
        if self.allow_multiple_entries:
            self.logger.info("Importing selected options from CSV file")

            path = tk.filedialog.askopenfilename()

            # Temporary dictionaries to store imported data
            selected_options = {}
            color_labels = {}

            with open(path, "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row.get('Type') and row.get('Color'):
                        selected_options[row['Type']] = row['Color']
                        self.selected_options_label.add_text(f"{row['Type']},\n")

                    if row.get('Label') and row.get('LabelColor'):
                        color_labels[row['LabelColor']] = row['Label']

            # Update instance dictionaries after reading
            self.selected_options.update(selected_options)
            self.color_labels.update(color_labels)

            print(f"\n\nImported Data from {path}\n")
        else:
            path = tk.filedialog.askopenfilename()
            with open(path, "r") as file:
                self.selected_options[self.dropdown.get()] = file.read().strip()

class tkScrolledtextBox(tkst.ScrolledText):
    def __init__(self, master, row, column, width, height):
        super().__init__(master, width=width, height=height)
        self.grid(row=row, column=column)
        self.config(state="disabled")

    def add_text(self, text):
        self.config(state="normal")
        self.insert(tk.END, text)
        self.config(state="disabled")

    def clear_text(self):
        self.delete("1.0", tk.END)

    def get_text(self):
        return self.get("1.0", tk.END)

    def export_to_txt(self, filename):
        with open(filename, "w") as file:
            file.write(self.get_text())


