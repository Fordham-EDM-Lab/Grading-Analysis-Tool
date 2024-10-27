import tkinter as tk
from tkinter import messagebox
import gradeAnalysisFunc as gaf
import gradeAnalysisWidgets as gaw
from tkinter import filedialog
from tkinter import ttk
from functools import partial
import platform
import os
import sys
import subprocess
import json
import dictionary as dic
import test_data_creation as randData
from gradeAnalysisFunc import return_filtered_dataframe


def file_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file)

def check_list_is_subset(target_list, check_list):
    if set(target_list) == set(check_list):
        return True
    return all(item in check_list for item in target_list)

def return_filtered_dataframe(df: gaf.pd.DataFrame, column: str, values: list) -> gaf.pd.DataFrame:
    mask = df[column].isin(values)
    return df[mask]

class GradingAnalysisTool:
    def __init__(self):
        self.logger = gaw.Logger(__name__)

        self.root = tk.Tk()
        self.root.title("Grading Analysis Tool")
        self.root.configure()
        self.terminal_output = None
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.configure(
            background="#DCDCDC",
            bd=2,
            padx=10,
            pady=10,
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=1,
            width=width,
            height=height
        )
        self.dataframe = gaf.pd.read_csv('data-processed-ready.csv')

        self.max_sections_threshold = None
        self.popup_box_threshold = None
        self.analysis_checkbox = None
        self.csv_checkbox = None
        self.heatmap_checkbox = None
        self.grade_dist_checkbox = None
        self.confirm_button = None

        self.course_names = None

        self.reset_gui_button = None
        self.file_path_button = None

        # GUI elements: Listbox variables
        self.commands_listbox = None
        self.departments_listbox = None
        self.majors_listbox = None
        self.faculty_listbox = None
        self.unique_listbox = None

        # Data analysis variables
        self.results = None
        self.dept = None
        self.major = None
        self.unique_selection = None
        self.min_enrollment_threshold = None
        self.min_enrollment = None
        self.max_enrollment_threshold = None
        self.max_enrollment = None
        self.min_sections_threshold = None
        self.min_sections = None
        self.max_sections_threshold = None
        self.max_sections = None
        self.min_gpa_threshold = None
        self.min_gpa = None
        self.max_gpa_threshold = None
        self.max_gpa = None
        self.analysis_options = None

        ##Option to pass whatever between methods
        self.generic_instance = None

        self.faculty = None
        self.departments = None
        self.majors = None
        self.faculty_set = None
        self.unique_list = None

        # File and directory variables
        self.input_file_name = None
        self.output_directory = None
        self.department_file = None
        self.instructor_file = None
        self.major_file = None
        self.course_table_file = None

        self.file_dict = {}

        self.commands_directory = None
        self.rand_data = None
        # Setup commands and GUI
        self.root.geometry("")
        self.setup_commands()
        self.setup_gui()  # Run GUI setup

    def setup_gui(self):

        #self.pre_processor_check()

        self.create_json_file()

        self.commands_listbox_widget()

        self.change_sourcefile_button()

        self.populate_current_file_state()

        if self.reset_gui_button is None:
            self.reset_gui_button = tk.Button(
                self.root, text="Reset", command=self.reset_button
            ).grid(row=6, column=2)


        self.run_command_button_toggle(state="normal")
        tk.Button(self.root, text="Help", command=self.run_selected_help_command).grid(
            row=7, column=2
        )

        if self.rand_data is None:
            self.rand_data = tk.Button(
                self.root, text="Use Random Data?", command=self.create_random_data
            )
            self.rand_data.grid(row=1, column=0)


        self.write_to_GUI()

        self.dynamic_resizing()

        self.root.iconphoto(
            False,
            tk.PhotoImage(
                file=file_path("Athletic_Logo_Block_F.png")
            ),
        )

        self.root.wm_iconphoto(False, tk.PhotoImage(file=file_path("Athletic_Logo_Block_F.png")))

        self.root.protocol("WM_DELETE_WINDOW", self.quit_program)

        self.root.mainloop()

    ####################################################################################################
         ##Thresholds
    def enrollment_threshold_widget(self, state="disabled", where=None, row=None, column=None):
        self.logger.info("Setting up enrollment threshold widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.min_enrollment_threshold = gaw.ThresholdWidget()
        self.min_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Min Enrollment:",
            row=row,
            column=column,
            help="Enter an integer for a threshold",
        )

        self.max_enrollment_threshold = gaw.ThresholdWidget()
        self.max_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Max Enrollment:",
            row=row + 1,
            column=column,
            help="Enter an integer for a threshold",
        )
        self.logger.info("Enrollment threshold widget setup completed")

    def sections_threshold_widget(self, state="disabled", where=None, row=None, column=None):
        self.logger.info("Setting up sections threshold widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.min_sections_threshold = gaw.ThresholdWidget()
        self.min_sections_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Min Sections:",
            row=row,
            column=column,
            help="Enter an integer for a threshold",
        )

        self.max_sections_threshold = gaw.ThresholdWidget()
        self.max_sections_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Max Sections:",
            row=row + 1,
            column=column,
            help="Enter an integer for a threshold",
        )
        self.logger.info("Sections threshold widget setup completed")

    def class_size_threshold_widget(self, state="disabled", where=None, row=None, column=None):
        self.logger.info("Setting up class size threshold widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.min_enrollment_threshold = gaw.ThresholdWidget()
        self.min_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Min Class Size:",
            row=row,
            column=column,
            help="Enter an integer for a threshold",
        )

        self.max_enrollment_threshold = gaw.ThresholdWidget()
        self.max_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Max Class Size:",
            row=row + 1,
            column=column,
            help="Enter an integer for a threshold",
        )
        self.logger.info("Class size threshold widget setup completed")

    def gpa_threshold_widget(self, state="disabled", where=None, row=None, column=None):
        self.logger.info("Setting up class size threshold widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.min_gpa_threshold = gaw.ThresholdWidget()
        self.min_gpa_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Min GPA:",
            row=row,
            column=column,
            help="Enter an integer for a threshold",
        )

        self.max_gpa_threshold = gaw.ThresholdWidget()
        self.max_gpa_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Max GPA:",
            row=row + 1,
            column=column,
            help="Enter an integer for a threshold",
        )
        self.logger.info("Class size threshold widget setup completed")

    def course_num_taken_threshold_widget(self, state="disabled", where=None, row=None, column=None):
        self.logger.info("Setting up course num taken threshold widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.min_enrollment_threshold = gaw.ThresholdWidget()
        self.min_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Min Courses Taken:",
            row=row,
            column=column,
            help="Enter an integer for a threshold",
        )

        self.max_enrollment_threshold = gaw.ThresholdWidget()
        self.max_enrollment_threshold.generic_thresholds_widget(
            where=where,
            state=state,
            text="Max Courses Taken:",
            row=row + 1,
            column=column,
            help="Enter an integer for a threshold",
        )
        self.logger.info("Course num taken threshold widget setup completed")

    def thresholds_widget(self, state="disabled", where=None, which=None):
        self.logger.info(f"Setting up thresholds widget for: {which}")
        for threshold_widget in [
            self.min_enrollment_threshold,
            self.max_enrollment_threshold,
            self.min_sections_threshold,
            self.max_sections_threshold,
        ]:
            if threshold_widget is not None:
                threshold_widget.destroy()

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        where.protocol("WM_DELETE_WINDOW", self.reset_gui)

    def csv_checkbox_widget(self, state="disabled", where=None, row=1, column=4):
        self.logger.info("Starting setup of CSV checkbox widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.csv_checkbox = gaw.CheckboxWidget()
        self.csv_checkbox.create_checkbox(
            where=where,
            text="CSV File",
            state=state,
            row=row,
            column=column,
            help_text="Check this box to create a csv",
        )
        self.logger.info("CSV checkbox widget created successfully")

    def heatmap_checkbox_widget(self, state="disabled", where=None, row=1, column=4):
        self.logger.info("Starting setup of heatmap checkbox widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.heatmap_checkbox = gaw.CheckboxWidget()
        self.heatmap_checkbox.create_checkbox(
            where=where,
            text="Heatmap",
            state=state,
            row=row,
            column=column,
            help_text="Check this box to create a heatmap",
        )
        self.logger.info("Heatmap checkbox widget created successfully")

    def grade_distribution_checkbox(
        self, state="disabled", where=None, row=1, column=4
    ):
        self.logger.info("Starting setup of grade distribution checkbox widget")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.grade_dist_checkbox = gaw.CheckboxWidget()
        self.grade_dist_checkbox.create_checkbox(
            where=where,
            text="Generate Grade Distribution?",
            state=state,
            row=row,
            column=column,
            help_text="Check this box to create a grade distribution",
        )
        self.logger.info("Grade distribution checkbox widget created successfully")

    # general analysis checkboxes, pick which one you want by passing a list of booleans, like [True, False, True] to use the first and third checkbox
    # places them top down
    def create_analysis_dropdown(
        self,
        where=None,
        analysis_options=None,
        row=0,
        column=0,
        initial_message="Select Analysis",
    ):
        self.logger.info("Starting setup of analysis dropdowns")

        if where is None:
            where = self.root
            self.logger.debug("Default 'where' parameter used: self.root")

        self.logger.debug(f"Analysis options set: {analysis_options}")

        self.analysis_dropdown = gaw.tkDropdown(
            where, analysis_options, row, column, initial_message=initial_message
        )
        self.logger.info("Analysis dropdown created successfully")

    # Creates the appropriate checkboxes and thresholds when used on the root gui itself
    # right now only used for run all commands but can and should be used for future commands
    # will add way to control row and column of each widget
    def thresholds_on_root(self, which=None, row=0, column=0):
        self.logger.info("Setting up thresholds on root")

        self.thresholds_widget(
            state="normal", where=self.root, which="sections_enrollment"
        )
        self.logger.debug("Thresholds widget setup completed")

        self.logger.info("Thresholds setup on root completed")

    # Some commands need thresholds, but it wouldn't look right to have them on main
    # popup seemed like the best way
    # you can toggle the analysis checkboxes and csv checkbox on or off, but you at least need the thresholds on it
    def threshold_popup(
        self,
        window_length=700,
        window_height=100,
    ):

        self.popup_box_threshold = tk.Toplevel(self.root)
        self.popup_box_threshold.title("Threshold")
        self.popup_box_threshold.geometry(f"{window_length}x{window_height}")
        self.logger.debug("Threshold popup window initialized")

        self.popup_box_threshold.protocol("WM_DELETE_WINDOW", self.reset_gui)

        return self.popup_box_threshold

    def confirm_threshold_choice(self, command=None):
        self.logger.info("Adding confirm button to threshold popup")

        if command:
            self.logger.debug(f"Confirm button will execute command: {command.__name__}")
        else:
            self.logger.warning("No command provided for confirm button")

        tk.Button(self.popup_box_threshold, text="Go", command=lambda: self.run_command_confirm_threshold(command), width=4).grid(row=2, column=2)
        self.logger.debug("Confirm button added to popup")

    def run_command_confirm_threshold(self, command):
        self.logger.info("Running command for confirming threshold")

        self.get_thresholds()
        self.logger.debug("Threshold values retrieved")

        if command:
            self.logger.debug(f"Executing provided command: {command.__name__}")
            command()
        else:
            self.logger.warning("No command provided to execute")

        self.reset_gui()
        self.logger.info("GUI reset after command execution")

    # foolproof function to minimize error brought by thresholds, they love to break
    def get_valid_integer(self, threshold=gaw.ThresholdWidget()):
        if threshold is not None:
            try:
                value = threshold.get_entry_value()
                return float(value) if value is not None else None
            except ValueError:
                self.logger.error(f"Value for {threshold} is not a valid integer.")
                return None
        else:
            self.logger.warning(f"Threshold not found")
            return None

    def get_thresholds(self):
        self.logger.info("Retrieving threshold values")

        if self.min_enrollment_threshold is not None:
            self.min_enrollment = self.get_valid_integer(self.min_enrollment_threshold)
        if self.max_enrollment_threshold is not None:
            self.max_enrollment = self.get_valid_integer(self.max_enrollment_threshold)
        if self.min_sections_threshold is not None:
            self.min_sections = self.get_valid_integer(self.min_sections_threshold)
        if self.max_sections_threshold is not None:
            self.max_sections = self.get_valid_integer(self.max_sections_threshold)
        if self.min_gpa_threshold is not None:
            self.min_gpa = self.get_valid_integer(self.min_gpa_threshold)
        if self.max_gpa_threshold is not None:
            self.max_gpa = self.get_valid_integer(self.max_gpa_threshold)
        self.logger.debug(
            f"Thresholds set - Min Enrollment: {self.min_enrollment}, Max Enrollment: {self.max_enrollment}, Min Sections: {self.min_sections}, Max Sections: {self.max_sections}, Min GPA: {self.min_gpa}, Max GPA: {self.max_gpa}"
        )

    ##################################################################################
    ##History File .history.json

    def update_filestate(self, file, which):
        self.logger.info(f"Updating file state for: {which}")

        history_path = file_path(".history.json")

        # update the appropriate attribute based on which file is being updated
        attribute_map = {
            self.input_file_name: "input_file_name",
            self.output_directory: "output_directory",
            self.course_table_file: "course_table_file",
            self.department_file: "department_file",
            self.instructor_file: "instructor_file",
            self.major_file: "major_file",
        }

        if which in attribute_map:
            if which == self.input_file_name:
                self.dataframe = gaf.pd.read_csv(file)
            setattr(self, attribute_map[which], file)
            self.logger.debug(f"Updated {attribute_map[which]} to {file}")
        else:
            self.logger.warning(f"Unrecognized attribute for update: {which}")

        # update .history.json
        if os.path.exists(history_path):
            with open(history_path, "w") as f:
                history = {
                    "inputfile": str(self.input_file_name),
                    "outputfile": str(self.output_directory),
                    "coursetablefile": str(self.course_table_file),
                    "departmentfile": str(self.department_file),
                    "instructorfile": str(self.instructor_file),
                    "majorfile": str(self.major_file),
                }
                json.dump(history, f)
                self.logger.info(f"Updated .history.json with new file paths")
        else:
            self.logger.warning(".history.json does not exist, creating a new one")
            self.create_json_file()

    #################################################################################
    ##Commands
    def setup_commands(self):
        self.logger.info("Setting up commands for GradingAnalysisTool")

        self.commands_directory = {
            # "1 Major & Department Analysis": self.command_MajorDepartment,
            "Department Analysis": self.command_DeptAnalysis,
            "Instructor Analysis": self.command_InstAnalysis,
            "Major Analysis": self.command_MjrAnalysis,
            "Course Analysis": self.command_CrsAnalysis,
            "Section Analysis": self.command_SectionAnalysis,
            "Level Analysis": self.command_LevelAnalysis,
            "Student Analysis": self.command_student_analysis,
            # "Run All Commands": self.command_All_Commands,
            "Quit": self.quit_program,
        }

        self.logger.debug(f"Commands set up: {list(self.commands_directory.keys())}")
        self.logger.info("Command setup completed")

    def place_commands(self):
        self.logger.info("Placing commands in the listbox")

        for command in self.commands_directory.keys():
            self.commands_listbox.insert(parent="", index=tk.END, values=(command,))
            self.logger.debug(f"Command '{command}' added to listbox")

        self.logger.info("All commands placed in listbox successfully")

    ##########################################################################################
    ##specific functions

    # used for Unique List to do some basic top level analysis on main attributes of the data
    def numpy_array_metadata(self, arr):
        if arr.size == 0:
            print("The array is empty.")
            return

        print(f"Number of Unique Elements: {arr.size}")
        print(f"Data Type of Elements: {arr.dtype}")

        if arr.ndim == 1 and arr.size >= 5:
            print("First 5 Elements:")
            print(arr[:5])

    def quit_program(self):
        self.logger.info("Quitting Program")
        exit()

    # no idea how this works or if it even works, need to visit again. works for now tho
    def dynamic_resizing(self):
        self.logger.info("Setting up dynamic resizing for the GUI")

        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        self.logger.info("Dynamic resizing setup completed")

    def reset_button(self):
        self.terminal_output = None
        self.logger.info("Reset Button Clicked")
        self.reset_gui()

    def pre_processor_check(self):
        self.logger.info("Starting pre-processor check for required files")

        for file_name in self.required_files:
            full_path = file_path(file_name)
            self.logger.debug(f"Checking for file: {full_path}")

            if not os.path.isfile(full_path):
                self.logger.error(
                    f"Pre-processor check failed. Missing file: {file_name}"
                )
                messagebox.showerror(
                    "Preprocessor Check Failed",
                    f"Please run the generateTables file to use the GUI. Missing file: {file_name}",
                )
                self.ask_run_generateTables()
                sys.exit()

        self.logger.info("Pre-processor check completed successfully")
        return

    def ask_run_generateTables(self):
        self.logger.info("Asking user to run generateTables.py")

        if messagebox.askyesno(
            "Preprocessor Check Failed",
            "Please run the generateTables file to use the GUI. Would you like to run it now?",
        ):
            self.logger.debug("User selected to run generateTables.py")
            subprocess.Popen([sys.executable, "generateTables.py"])
            sys.exit()
        else:
            self.logger.debug("User selected not to run generateTables.py")
            sys.exit()

    def run_command_button_toggle(self, state="normal"):
        self.logger.info("Toggling run command button")
        tk.Button(
            self.root,
            text="Run Command",
            command=self.run_selected_commands,
            state=state,
        ).grid(row=7, column=0, pady=10)

    ##use this all the time
    # lovely command to bind a helpful tooltip to literally anything tkinter
    def bind_tooltip_events(self, widget, text):
        tooltip = gaw.ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())

    # creates the console output for the terminal
    def write_to_GUI(self):
        self.logger.info("Writing to GUI terminal output")

        if self.terminal_output is None:
            self.logger.debug("Initializing terminal output console")
            self.terminal_output = gaw.Console(self.root)
            self.terminal_output.grid(
                row=9, rowspan=3, column=0, columnspan=10, sticky="nsew"
            )
            self.terminal_output.write("Terminal Display:\n\n\n\n\n\n")
            self.logger.info("Terminal output console initialized and displayed")
        else:
            self.logger.debug("Terminal output console already initialized")
            return

    ##Gets the content of the terminal_output Text widget from the beginning to the end.
    # Split the content into lines and create a counter
    # Check if the line contains the phrase "File Created:".
    # If found, split the line into two parts. The left part will be ignored, and the right part will be the file path.
    # Increment the line number counter for the next iteration.

    def hyperlink_filepath(self):
        self.logger.info("Processing file paths for hyperlinks in terminal output")
        self.file_dict = {}
        content = self.terminal_output.get("1.0", tk.END)
        lines = content.split("\n")
        arrlines = []

        for line_number, line in enumerate(lines, start=1):
            if "File Created:" in line:
                _, file_path = line.split("File Created:")
                file_path = file_path.strip()
                arrlines.append((line_number, line, file_path))
                self.logger.debug(f"File path identified for hyperlinking: {file_path}")

        for arrline in arrlines:
            self.create_hyperlink(hyperlink_tuple=arrline)
        self.logger.info("Hyperlink processing completed")

    def create_hyperlink(self, hyperlink_tuple):
        line_number, line, file_path = hyperlink_tuple
        self.logger.debug(f"Creating hyperlink for file: {file_path}")
        col_start = line.find(file_path)

        if col_start != -1:
            start_index = f"{line_number}.{col_start}"
            end_index = f"{line_number}.{col_start + len(file_path)}"
            file_opener = gaw.FileOpener(file_path)
            self.file_dict[file_path] = file_opener
            a = (start_index, end_index, file_path)
            self.hyperlink_binds(a)
            self.logger.debug(f"Hyperlink created for: {file_path}")

    def clicked_hyperlink(self, file_path, event=None):
        self.logger.info(f"Hyperlink clicked for file: {file_path}")
        file_opener = self.file_dict.get(file_path)

        if file_opener is not None:
            file_opener.open_file()
        else:
            self.logger.warning(f"File path {file_path} not found in dictionary.")

    def hyperlink_binds(self, tuple):
        (start, end, file_path) = tuple
        unique_tag = f"hyperlink_{start}_{end}"  # Create a unique tag
        self.logger.debug(f"Binding {unique_tag} to: {file_path}")

        self.terminal_output.config(state="normal")
        self.terminal_output.tag_add(unique_tag, start, end)
        self.terminal_output.tag_config(unique_tag, foreground="blue", underline=1)
        self.terminal_output.tag_bind(
            unique_tag, "<Button-1>", lambda event: self.clicked_hyperlink(file_path)
        )
        self.terminal_output.config(state="disabled")
        self.logger.debug(f"{unique_tag} bound and configured for: {file_path}")

    ################################################################################################################################################

    # goal here is, after every command, the whole gui is reset as it is on startup. Ensures nothing breaks and
    # no weird errors occur by variables states being in weird state when running specific commands
    def reset_gui(self):
        self.logger.info("Resetting the GUI")

        self.dept = self.major = self.faculty = self.min_enrollment = (
            self.max_enrollment
        ) = self.min_sections = self.max_sections = self.generic_instance = None

        self.logger.debug("State variables reset")

        for widget in [
            self.departments_listbox,
            self.faculty_listbox,
            self.popup_box_threshold,
            self.csv_checkbox,
            self.analysis_checkbox,
            self.majors_listbox,
            self.commands_listbox,
            self.heatmap_checkbox,
            self.grade_dist_checkbox,
            self.unique_listbox,
            self.max_sections_threshold,
            self.min_sections_threshold,
            self.analysis_checkbox,
            self.min_enrollment_threshold,
            self.max_enrollment_threshold,
            self.confirm_button,
            self.max_gpa_threshold,
            self.min_gpa_threshold
        ]:
            if widget is not None:
                widget.destroy()
                self.logger.debug(f"Widget destroyed: {type(widget).__name__}")

        self.min_enrollment_threshold = self.min_sections_threshold = (
            self.max_enrollment_threshold
        ) = self.max_sections_threshold = None

        try:
            self.setup_gui()
            self.logger.info("GUI re-setup completed successfully")
        except Exception as e:
            self.logger.error(f"An error occurred while setting up the GUI: {e}")
            print(f"An error occurred while setting up the GUI: {e}")

    ##############################################################################################
    # input and output directory

    # history to remember the files that the user selected as the input csv and output files checks if the file exists and if it does
    # exits the file, and if it doesn't exist (first startup), creates them with preset paths

    def create_json_file(self):
        self.logger.info("Creating or checking .history.json file")

        history_path = file_path(".history.json")
        if os.path.exists(history_path):
            self.logger.debug(".history.json already exists")

            return
        else:
            self.logger.debug(
                ".history.json does not exist, creating with default values"
            )
            self.input_file_name = str(file_path("data-processed-ready.csv"))
            self.output_directory = str(
                file_path("grading_analysis_output")
            )
            self.course_table_file = str(file_path("courseTable.csv"))
            self.department_file = str(file_path("deptTable.csv"))
            self.instructor_file = str(file_path("instTable.csv"))
            self.major_file = str(file_path("majorTable.csv"))

            with open(history_path, "w") as f:
                history = {
                    "inputfile": self.input_file_name,
                    "outputfile": self.output_directory,
                }
                json.dump(history, f)
                self.logger.info(
                    ".history.json created and initialized with default file paths"
                )

    # read the json (on reset) or when theres changes in the file
    def populate_current_file_state(self):
        self.logger.info("Populating current file state from .history.json")

        history_path = file_path(".history.json")

        if os.path.exists(history_path):
            self.logger.debug(f"Found .history.json at {history_path}")
            with open(history_path, "r") as f:
                content = f.read()

                if content:
                    try:
                        file_data = json.loads(content)
                        self.logger.debug("File data loaded from .history.json")
                    except json.JSONDecodeError as e:
                        self.logger.error(
                            f"JSON decoding error: {e}. Recreating .history.json"
                        )
                        self.create_json_file()
                        return

                    self.input_file_name = file_data.get("inputfile")
                    self.dataframe = gaf.pd.read_csv(self.input_file_name)
                    self.output_directory = file_data.get("outputfile")
                    self.department_file = file_data.get("departmentfile")
                    self.instructor_file = file_data.get("instructorfile")
                    self.major_file = file_data.get("majorfile")
                    self.course_table_file = file_data.get("coursetablefile")
                    self.logger.info("File paths updated from .history.json")
                else:
                    self.logger.warning(
                        ".history.json is empty. Recreating file with default values"
                    )
                    self.create_json_file()
        else:
            self.logger.warning(
                ".history.json not found. Creating new file with default values"
            )
            self.create_json_file()

    # main gui change button
    def change_sourcefile_button(self):
        self.logger.info("Creating 'File Paths' button for source file change")

        self.file_path_button = tk.Button(
            self.root, text="File Paths", command=self.sources_popup
        )
        self.file_path_button.grid(row=6, column=0)

        self.logger.debug("'File Paths' button created and placed in GUI")

    # popup containing all the paths that are changeable and needed. If more are needed, put here following the format seen
    def sources_popup(self):
        self.logger.info("Creating 'Source paths' popup window")

        source_popup = tk.Toplevel(self.root)
        source_popup.title("Source paths")

        self.file_path_browse_widget(
            source_popup,
            row=0,
            column=0,
            text="Input File:",
            file=str(self.input_file_name),
            set_command=self.file_call,
            required_file=self.input_file_name,
        )
        self.file_path_browse_widget(
            source_popup,
            row=1,
            column=0,
            text="Output directory:",
            file=str(self.output_directory),
            set_command=self.file_call,
            required_file=self.output_directory,
            directory=True,
        )

        tk.Button(source_popup, text="Close", command=source_popup.destroy).grid(
            row=6, column=1
        )
        self.logger.debug(
            "'Source paths' popup window created with all file path browse widgets"
        )

    # label with the path of file and also the browse button
    def file_path_browse_widget(
        self,
        where,
        row,
        column,
        text,
        file,
        set_command,
        required_file,
        directory=False,
    ):
        self.logger.info(f"Creating file path browse widget for: {text}")

        label = tk.Label(where, text=text)
        label.grid(row=row, column=column, sticky=tk.W)
        file_path = tk.Label(where, text=file)
        file_path.grid(row=row, column=column + 1)

        if directory:
            browse = tk.Button(
                where,
                text="Browse",
                command=lambda: set_command(
                    file_path, file, required_file, directory=True
                ),
            )
            self.logger.debug(f"Browse button created for directory selection: {text}")
        else:
            browse = tk.Button(
                where,
                text="Browse",
                command=lambda: set_command(file_path, file, required_file),
            )
            self.logger.debug(f"Browse button created for file selection: {text}")

        browse.grid(row=row, column=column + 2)
        self.logger.debug(f"File path browse widget set up completed for: {text}")

    # file call mainly for csv and directory
    def file_call(self, button=tk.Label, file=str, required_file=None, directory=False):
        self.logger.info(
            f"Initiating file call for {('directory' if directory else 'file')} selection"
        )

        if directory:
            file_dir = filedialog.askdirectory()
            file = str(file_dir)
            self.logger.debug(f"Directory selected: {file}")
        else:
            file_dir = filedialog.askopenfile()
            if file_dir:
                file = str(file_dir.name)
                self.logger.debug(f"File selected: {file}")
            else:
                self.logger.warning("File selection cancelled")
                return

        self.update_filestate(file=file, which=required_file)
        if file == self.input_file_name:
            print('Input File updated, Dataframe changed, to undo this, change the path of the input file')
        button.config(text=str(file))
        self.logger.info(f"File state updated for {required_file}")


    def update_df(self):
        if isinstance(self.dataframe, gaf.pd.Dataframe()):
            self.dataframe = gaf.pd.read_csv(self.input_file_name)
            self.reset_gui()
        else:
            return
    ##########################################################################################################
    # populate widgets

    # any list that needs population gets population here.

    def populate_majors_listbox(self):
        self.logger.info("Populating majors listbox")
        self.majors = self.dataframe["Major"].unique().tolist()
        self.majors.sort()

        for major in self.majors:
            self.majors_listbox.insert(parent="", index=tk.END, values=(major,))

    def populate_department_listbox(self):
        self.logger.info("Populating departments listbox")
        self.departments = self.dataframe["Department"].unique().tolist()
        self.departments.sort()

        for dept in self.departments:
            self.departments_listbox.insert(parent="", index=tk.END, values=(dept,))

    def populate_faculty_listbox(self):
        self.logger.info("Populating faculty listbox")
        self.faculty_set = self.dataframe["FacultyID"].unique().tolist()

        for faculty in self.faculty_set:
            self.faculty_listbox.insert(parent="", index=tk.END, values=(faculty,))

    def populate_unique_listbox(self):
        self.logger.info("Populating unique listbox")
        self.unique_list = [
            "Departments",
            "Majors",
            "Instructor IDs",
            "Courses",
            "UniqueCourseID",
            "Student IDs",
            "All",
            "Export All",
        ]

        for unique in self.unique_list:
            self.unique_listbox.insert(parent="", index=tk.END, values=(unique,))

    ################################################################################################################
    # Help popups

    # code for the popup and the close button on the popup, below is the text
    def file_path_popup(self, title="", popup_text="", type_file = ""):
        self.logger.info(f"Creating popup with title: '{title}'")

        messageBox = tk.Toplevel()
        label = tk.Label(messageBox, text=title)
        label.pack()
        self.logger.debug("Popup title label created")

        show_help_info = tk.Label(messageBox, text=popup_text, justify="left")
        show_help_info.pack()
        self.logger.debug("Popup text label created")

        button_close = tk.Button(messageBox, text="Close", command=messageBox.destroy)
        button_close.pack()
        self.logger.debug("Close button created for popup")

        self.logger.info("Popup created and displayed successfully")



    def popup(self, title="", popup_text=""):
        self.logger.info(f"Creating popup with title: '{title}'")

        messageBox = tk.Toplevel()
        label = tk.Label(messageBox, text=title)
        label.pack()
        self.logger.debug("Popup title label created")

        show_help_info = tk.Label(messageBox, text=popup_text, justify="left")
        show_help_info.pack()
        self.logger.debug("Popup text label created")

        button_close = tk.Button(messageBox, text="Close", command=messageBox.destroy)
        button_close.pack()
        self.logger.debug("Close button created for popup")

        self.logger.info("Popup created and displayed successfully")

    # simple if elif for all the help commands. Simple to expand
    def popup_text(self, help_output):
        self.logger.info(f"Displaying help popup for: {help_output}")

        if help_output == "Department Analysis":
            self.popup(
                title="Department Analysis Help",
                popup_text="\nWhen this command is clicked, you have options to select between what type of analysis (x and y plots) and can choose and specify specifically which departments you would like to see.\nIF YOU WANT TO HAVE ALL DEPARTMENTS REPRESENTED, DO NOT CHANGE THE DEPARTMENT OPTION.\nThere is also an option for checking the grade distribution, which is a graph representing the frequency of letter grades normalized across selected departments.",
            )
        elif help_output == "Instructor Analysis":
            self.popup(
                title="Instructor Analysis Help",
                popup_text="\nInstructor Analysis allows you to select analysis options (x and y plots) can can choose which instructors you would like individually. You can also choose if you would like to select all instructors in a Department, or a Course.\nIF YOU WANT TO USE ALL DEPARTMENTS/COURSES, DO NOT CHANGE THE OPTION.\nYou can also use see the grade distrubtion of letter grades normalized across selected instructors\n",
            )
        elif help_output == "Major Analysis":
            self.popup(
                title="Major Analysis Help",
                popup_text="\nMajor Analysis allows you to select analysis options (x and y plots) can can choose which Majors you would like individually\nIF YOU WANT TO USE ALL MAJORS, DO NOT CHANGE THE OPTION.\nYou can also use see the grade distrubtion of letter grades normalized across selected Majors\n",
            )
        elif help_output == "Level Analysis":
            self.popup(
                title="Level Analysis Help",
                popup_text="\nThis commabnd allows you to select if you want to do analysis on Course Levels (0000-4000) or Student Level (Freshman-Graduate Students in Undergraduate Courses\nYou can Also see the grade distribution of each option\n\n\nThe 3rd option, Student-Level Analysis, only creates a heatmap of the courses and student level as the plot",
            )
        elif help_output == "Course Analysis":
            self.popup(
                title="Course Analysis Help",
                popup_text="\nCourse Analysis allows you to select analysis options (x and y plots) can can choose which Course you would like individually\nIF YOU WANT TO USE ALL COURSES, DO NOT CHANGE THE OPTION.\nYou can also use see the grade distrubtion of letter grades normalized across selected Courses\n",
            )

        elif help_output == "Section Analysis":
            self.popup(
                title="Section Analysis Help",
                popup_text="\nSection Analysis allows you to select analysis options of all the Sections of a course (x and y plots) can can choose which Course Sections you would like individually\nIF YOU WANT TO USE ALL COURSES AND THEIR SECTIONS, DO NOT CHANGE THE OPTION.(SLOWER)\nYou can also use see the grade distrubtion of letter grades normalized across selected Courses Sections\n",
            )
        elif help_output == "Student Analysis":
            self.popup(
                title="Student Analysis Help",
                popup_text="\nStudent Analysis allows you to select analysis options (x and y plots) of various grouping of students\nYou can also use see the grade distrubtion of letter grades normalized across selected Students\n",
            )
        else:
            self.logger.info(f"Displaying general help popup")

            self.popup(
                title="Help",
                popup_text="""

                (1) Department Analysis: Analyze and graph Departments, see grade distribution of departments

                (2) Instructor Analysis: Analyze and graph Instructors, see grade distribution of instructors

                (3) Major Analysis: Analyze and graph Majors, see grade distribution of majors

                (4) Course Analysis: Analyze and graph Courses, see grade distribution of courses

                (5) Section Analysis: Analyze and graph Course Sections, see grade distribution of course sections

                (6) Level Analysis: Analyze and graph Course Levels or Student Levels, see grade distribution of each selected level.
                    Heatmap options available for Student-Course Level Analysis.

                (7) Student Analysis: Analyze and graph Students, see grade distribution of students""",
            )
        self.logger.debug(f"Help popup for '{help_output}' displayed")

    ##########################################################################################################
    # listbox widgets

    # one generic listbox used for all functions which have a choice of multiple operations.
    # Convert these to classes is on the todo

    def commands_listbox_widget(self, row=3, column=1):
        self.logger.info("Setting up commands listbox widget")
        self.commands_listbox = gaw.TableWidget()
        self.commands_listbox.generic_tableview_widget(
            where=self.root,
            row=row,
            column=column,
            colHeading="commands",
            title="Command(s):",
            helptip="Select a command to run.",
        )
        self.place_commands()
        self.logger.debug("Commands listbox widget set up and populated")

    def faculty_listbox_widget(self, row=3, column=1):
        self.logger.info("Setting up faculty listbox widget")
        self.faculty_listbox = gaw.TableWidget()
        self.faculty_listbox.generic_tableview_widget(
            where=self.root,
            row=row,
            column=column,
            colHeading="faculty",
            title="Faculty:",
            helptip="Which Faculty? Select a valid Faculty",
        )
        self.populate_faculty_listbox()
        self.logger.debug("Faculty listbox widget set up and populated")

    def departments_listbox_widget(self, row=3, column=1):
        self.logger.info("Setting up departments listbox widget")
        self.departments_listbox = gaw.TableWidget()
        self.departments_listbox.generic_tableview_widget(
            where=self.root,
            row=row,
            column=column,
            colHeading="department",
            title="Department:",
            helptip="Which department? Select a valid Department",
        )
        self.populate_department_listbox()
        self.logger.debug("Departments listbox widget set up and populated")

    def majors_listbox_widget(self, row=3, column=1):
        self.logger.info("Setting up majors listbox widget")
        self.majors_listbox = gaw.TableWidget()
        self.majors_listbox.generic_tableview_widget(
            where=self.root,
            row=row,
            column=column,
            colHeading="major",
            title="Major:",
            helptip="Which major? Select a valid Major",
        )
        self.populate_majors_listbox()
        self.logger.debug("Majors listbox widget set up and populated")

    def unique_listbox_widget(self, row=3, column=1):
        self.logger.info("Setting up unique listbox widget")
        self.unique_listbox = gaw.TableWidget()
        self.unique_listbox.generic_tableview_widget(
            where=self.root,
            row=row,
            column=column,
            colHeading="unique",
            title="Enter Unique List Request:",
            helptip="Which Entry? Select a valid Entry",
        )
        self.populate_unique_listbox()
        self.logger.debug("Unique listbox widget set up and populated")

    ##########################################################################################################
    # confirm widgets

    # Generic confirm button which just sets a command passed to it that does the operation meant to do when pressed.

    def confirm_department_major_selections(self):
        self.logger.info("Creating confirm button for department and major selections")
        self.confirm_button = gaw.ConfirmButton()
        self.confirm_button.make_confirm_button(
            where=self.root,
            command=self.set_choices_department_major,
            row=6,
            column=1,
            helptip="Confirm Major and Department",
        )
        self.logger.debug("Confirm button for department and major selections created")

    def confirm_faculty_selection(self):
        self.logger.info("Creating confirm button for faculty selection")
        self.confirm_button = gaw.ConfirmButton()
        self.confirm_button.make_confirm_button(
            where=self.root,
            command=self.set_choices_faculty,
            row=4,
            column=1,
            helptip="Confirm Faculty",
        )
        self.logger.debug("Confirm button for faculty selection created")

    def confirm_unique_selection(self):
        self.logger.info("Creating confirm button for unique selection")
        self.confirm_button = gaw.ConfirmButton()
        self.confirm_button.make_confirm_button(
            where=self.root,
            command=self.set_choices_unique,
            row=4,
            column=1,
            helptip="Confirm Unique",
        )
        self.logger.debug("Confirm button for unique selection created")

    def confirm_faculty_dept_major_selection(self):
        self.logger.info(
            "Creating confirm button for faculty, department, and major selections"
        )
        self.confirm_button = gaw.ConfirmButton()
        self.confirm_button.make_confirm_button(
            where=self.root,
            command=self.set_choices_department_major_faculty_selection,
            row=4,
            column=1,
            helptip="Confirm Selections",
        )
        self.logger.debug(
            "Confirm button for faculty, department, and major selections created"
        )

    ##########################################################################################################
    # set choices widgets

    def set_choices_department_major(self):
        self.logger.info("Setting department and major choices")
        if self.departments_listbox.selection() and self.majors_listbox.selection():
            self.dept = self.departments_listbox.item(
                self.departments_listbox.selection()
            )
            self.major = self.majors_listbox.item(self.majors_listbox.selection())
            self.logger.debug(f"Selected Department: {self.dept}, Major: {self.major}")
            self.run_MajorDepartment_analysis()
            self.reset_gui()
        else:
            self.logger.warning("Department or major not selected")

    def set_choices_department_major_faculty_selection(self):
        self.logger.info("Setting department, major, and faculty choices")
        if (
            self.departments_listbox.selection()
            and self.majors_listbox.selection()
            and self.faculty_listbox.selection()
        ):
            self.dept = self.departments_listbox.item(
                self.departments_listbox.selection()
            )
            self.major = self.majors_listbox.item(self.majors_listbox.selection())
            self.faculty = self.faculty_listbox.item(self.faculty_listbox.selection())
            self.logger.debug(
                f"Selected Department: {self.dept}, Major: {self.major}, Faculty: {self.faculty}"
            )
            self.run_every_command()
            self.reset_gui()
        else:
            self.logger.warning("Department, major, or faculty not selected")

    def set_choices_faculty(self):
        self.logger.info("Setting faculty choice")
        if self.faculty_listbox.selection():
            self.faculty = self.faculty_listbox.item(self.faculty_listbox.selection())
            self.logger.debug(f"Selected Faculty: {self.faculty}")
            self.run_faculty_analysis()
            self.reset_gui()
        else:
            self.logger.warning("Faculty not selected")

    def set_choices_unique(self):
        self.logger.info("Setting unique choice")
        if self.unique_listbox.selection():
            self.unique_selection = self.unique_listbox.item(
                self.unique_listbox.selection()
            )
            self.logger.debug(f"Selected Unique Option: {self.unique_selection}")
            self.run_unique_analysis()
            self.reset_gui()
        else:
            self.logger.warning("Unique option not selected")

    ##########################################################################################################
    ##run

    # specific to when the help button is clicked when user has a command highlighted, runs the popup text command with the command
    # highlighted and outputs a specific help to that command. works the same way as the main run command

    def run_selected_help_command(self):
        self.logger.info("Executing selected help command")
        selected_help_command = self.commands_listbox.selection()

        if selected_help_command:
            help_output = self.commands_listbox.item(selected_help_command)
            self.logger.debug(f"Help command selected: {help_output}")
            self.popup_text(help_output=help_output)
        else:
            self.logger.warning(
                "No help command selected (or quit was selected), running generic help"
            )
            self.popup_text(help_output="Help")

    # runs the highlighted command after 'run command' is clicked

    def run_selected_commands(self):
        self.logger.info("Executing selected command")
        selected_item = self.commands_listbox.selection()
        retrieved_command = str(
            self.commands_listbox.item(self.commands_listbox.selection())
        )

        if selected_item is not None:
            if retrieved_command in self.commands_directory:
                try:
                    command_function = self.commands_directory[retrieved_command]
                    self.logger.debug(f"Running command: {retrieved_command}")
                    command_function()
                except Exception as e:
                    self.logger.error(
                        f"An error occurred while running the command {retrieved_command}: {e}"
                    )
                    print(
                        f"An error occurred while running the command {retrieved_command}: {e}"
                    )
            else:
                self.logger.warning(
                    f"Command not found in directory: {retrieved_command}"
                )
        else:
            self.logger.warning("No command selected")

    ##########################################################################################################
    # commands

    # What happens after gpa command is confirAnalysis
    # def command_MajorDepartment(self):
    #     self.logger.info("Executing GPA command")
    #     self.commands_listbox.grid_forget()

    #     self.run_command_button_toggle(state="disabled")
    #     # creates listboxes for selection and waits for confirm to be clicked
    #     self.departments_listbox_widget(row=3, column=1)
    #     self.majors_listbox_widget(row=4, column=1)
    #     self.thresholds_on_root(
    #         which="sections_enrollment",
    #     )
    #     self.csv_checkbox_widget(state="normal", row=2, column=0)
    #     self.grade_distribution_checkbox(state="normal", row=2, column=2)

    #     # runs analysis
    #     self.confirm_department_major_selections()
    #     self.logger.debug("GPA command setup completed")

    # def run_MajorDepartment_analysis(self):
    #     self.logger.info("Running GPA analysis")

    #     self.major = self.majors_listbox.item(self.majors_listbox.selection())
    #     self.dept = self.departments_listbox.item(self.departments_listbox.selection())

    #     gaf.MajorDepartmentAnalysis(
    #         self.dataframe,
    #         self.dept,
    #         self.major,
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         min_sections=self.min_sections,
    #         max_sections=self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     self.hyperlink_filepath()
    #     self.reset_gui()
    #     self.logger.info("GUI reset after GPA analysis")

    def run_unique_analysis(self):
        self.logger.info(
            f"Running unique analysis for selection: {self.unique_selection}"
        )
        if self.unique_selection == "Departments":
            print("Departments: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_dept(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "Majors":
            print("Majors: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_major(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "Instructor IDs":
            print("Instructor IDs: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_inst(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "Courses":
            print("Courses: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_crs(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "UniqueCourseID":
            print("UniqueCourseID: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_crsid(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "Student IDs":
            print("Student IDs: \n\n")
            self.numpy_array_metadata(arr=gaf.get_unique_stud(self.dataframe))
            print("\n\n")
        elif self.unique_selection == "All":
            for name, array in [
                ("Departments", gaf.get_unique_dept(self.dataframe)),
                ("Majors", gaf.get_unique_major(self.dataframe)),
                ("Instructor ID", gaf.get_unique_inst(self.dataframe)),
                ("Courses", gaf.get_unique_crs(self.dataframe)),
                ("Course IDs", gaf.get_unique_crsid(self.dataframe)),
                ("Student IDs", gaf.get_unique_stud(self.dataframe)),
            ]:
                print(f"{name}:")
                self.numpy_array_metadata(arr=array)
                print("\n\n")
        elif self.unique_selection == "Export All":
            gaf.save_unique_entries(self.dataframe, user_directory=self.output_directory)
            self.hyperlink_filepath()
        else:
            self.logger.warning("Invalid unique selection")
            print("This is not a valid option.")
        self.reset_gui()
        self.logger.debug("Unique analysis completed")

    def command_DeptAnalysis(self):
        self.logger.info("Executing Department Analysis command")
        self.run_command_button_toggle(state="disabled")
        popup = self.threshold_popup(600, 125)
        self.create_analysis_dropdown(popup, dic.department_analysis_options, row=0, column=4)
        self.enrollment_threshold_widget('normal', popup, row=0, column=0)
        self.sections_threshold_widget('normal', popup, row=0, column=2)



        self.generic_instance = gaw.tkDropdown(
            self.popup_box_threshold,
            row=1,
            column=4,
            options_dict={course: False for course in gaf.get_unique_dept(self.dataframe).flatten()},
            initial_message="Select Department",
            allow_multiple_entries=True,
            filename="department_selections",
        )

        self.csv_checkbox_widget(
            where=self.popup_box_threshold, state="normal", row=2, column=0
        )
        self.grade_distribution_checkbox(
            where=self.popup_box_threshold, state="normal", row=3, column=0
        )
        self.confirm_threshold_choice(self.run_department_analysis)
        self.logger.debug("Department Analysis command setup completed")

    def run_department_analysis(self):
        if self.generic_instance.isEmpty():
            departments = gaf.get_unique_dept(self.dataframe)
        else:
            departments = self.generic_instance.get_selected_options()

        self.logger.info("Running department analysis")
        gaf.DepartmentAnalysis(
            self.dataframe,
            target_values=departments,
            user_directory=self.output_directory,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            min_sections=self.min_sections,
            max_sections=self.max_sections,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def command_InstAnalysis(self):
        self.logger.info("Executing Instructor Analysis command")
        self.run_command_button_toggle(state="disabled")
        popup = self.threshold_popup(600, 125)
        self.create_analysis_dropdown(popup, dic.instructor_analysis_options, row=0, column=4)
        self.enrollment_threshold_widget('normal', popup, row=0, column=0)
        self.sections_threshold_widget('normal', popup, row=0, column=2)

        dept_or_course = [
            "Department Instructors",
            "Course Instructors",
            "Manual Select",
        ]

        self.generic_instance = gaw.tkDropdown(
            self.popup_box_threshold,
            row=1,
            column=4,
            options_dict={str(inst): False for inst in dept_or_course},
            initial_message="Analyze instructors by what?",
            allow_multiple_entries=True,
            command=self.update_generic_instance_instructor,
        )
        self.csv_checkbox_widget(
            where=self.popup_box_threshold, state="normal", row=2, column=0
        )
        self.grade_distribution_checkbox(
            where=self.popup_box_threshold, state="normal", row=3, column=0
        )
        self.confirm_threshold_choice(self.run_instructor_analysis)
        self.logger.debug("Instructor Analysis command setup completed")

    def update_generic_instance_instructor(self):
        option = self.generic_instance.get_selected_options()[0]
        if option == "Department Instructors":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(dept): False for dept in gaf.get_unique_dept(self.dataframe)},
                initial_message="Get Department Instructors",
                allow_multiple_entries=True,
            )

        if option == "Course Instructors":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(crs): False for crs in gaf.get_unique_crscode(self.dataframe)},
                initial_message="Get Course Instructors",
                allow_multiple_entries=True,
            )

        if option == "Manual Select":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(inst): False for inst in gaf.get_unique_inst(self.dataframe)},
                initial_message="Get Course Instructors",
                allow_multiple_entries=True,
            )

    def get_unique_items(self, list1, list2):
        set1 = set(list1)
        set2 = set(list2)

        unique_items = set1.symmetric_difference(set2)

        return list(unique_items)

    def run_instructor_analysis(self):
        if self.generic_instance.isEmpty():
            instructors = gaf.get_unique_inst(self.dataframe)
        else:
            instructors = self.generic_instance.get_selected_options()

        if check_list_is_subset(instructors, gaf.get_unique_crscode(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'CourseCode', instructors)
        elif check_list_is_subset(instructors, gaf.get_unique_dept(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'Department', instructors)
        elif check_list_is_subset(instructors, gaf.get_unique_inst(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'FacultyID', instructors)


        self.logger.info("Running instructor analysis")
        gaf.InstructorAnalysis(
            df,
            user_directory=self.output_directory,
            target_values=instructors,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            min_sections=self.min_sections,
            max_sections=self.max_sections,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()
        self.logger.debug("Instructor analysis completed")

    def command_MjrAnalysis(self):
        self.run_command_button_toggle(state="disabled")

        popup = self.threshold_popup(600, 125)
        self.create_analysis_dropdown(popup, dic.major_analysis_options, row=0, column=4)
        self.enrollment_threshold_widget('normal', popup, row=0, column=0)
        self.sections_threshold_widget('normal', popup, row=0, column=2)

        self.generic_instance = gaw.tkDropdown(
            self.popup_box_threshold,
            row=1,
            column=4,
            options_dict={str(major): False for major in gaf.get_unique_major(self.dataframe).flatten()},
            initial_message="Select Major",
            allow_multiple_entries=True,
        )

        self.csv_checkbox_widget(
            where=self.popup_box_threshold, state="normal", row=2, column=0
        )
        self.grade_distribution_checkbox(
            where=self.popup_box_threshold, state="normal", row=3, column=0
        )
        self.confirm_threshold_choice(self.run_major_analysis)

    def run_major_analysis(self):
        if self.generic_instance.isEmpty():
            majors = gaf.get_unique_major(self.dataframe)
        else:
            majors = self.generic_instance.get_selected_options()

        gaf.MajorAnalysis(
            self.dataframe,
            self.output_directory,
            self.min_enrollment,
            self.max_enrollment,
            self.min_sections,
            self.max_sections,
            target_values=majors,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def command_SectionAnalysis(self):
        self.run_command_button_toggle(state="disabled")
        popup = self.threshold_popup(500, 125)
        self.create_analysis_dropdown(popup, dic.section_analysis_options, row=0, column=4)
        self.enrollment_threshold_widget('normal', popup, row=0, column=0)
        self.gpa_threshold_widget('normal', popup, row=0, column=1)

        self.csv_checkbox_widget(
            where=self.popup_box_threshold, state="normal", row=2, column=0
        )

        dept_or_course = [
            "Department Sections",
            "Course Sections",
            "Manual Select",
        ]

        self.generic_instance = gaw.tkDropdown(
            self.popup_box_threshold,
            row=1,
            column=4,
            options_dict={str(inst): False for inst in dept_or_course},
            initial_message="Analyze sections by what?",
            allow_multiple_entries=True,
            command=self.update_generic_instance_section,
        )
        self.grade_distribution_checkbox(
            where=self.popup_box_threshold, state="normal", row=3, column=0
        )
        self.confirm_threshold_choice(self.run_section_analysis)

    def update_generic_instance_section(self):
        option = self.generic_instance.get_selected_options()[0]
        if option == "Department Sections":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(dept): False for dept in gaf.get_unique_dept(self.dataframe)},
                initial_message="Get Department Instructors",
                allow_multiple_entries=True,
            )

        if option == "Course Sections":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(crs): False for crs in gaf.get_unique_crscode(self.dataframe)},
                initial_message="Get Course Instructors",
                allow_multiple_entries=True,
            )

        if option == "Manual Select":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(inst): False for inst in gaf.get_unique_inst(self.dataframe)},
                initial_message="Get Course Instructors",
                allow_multiple_entries=True,
            )

    def run_section_analysis(self):
        if self.generic_instance.isEmpty():
            courses = gaf.get_unique_crscode(self.dataframe)
        else:
            courses = self.generic_instance.get_selected_options()

        if check_list_is_subset(courses, gaf.get_unique_crscode(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'CourseCode', courses)
        elif check_list_is_subset(courses, gaf.get_unique_dept(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'Department', courses)
        elif check_list_is_subset(courses, gaf.get_unique_inst(self.dataframe)):
            df = return_filtered_dataframe(self.dataframe, 'UniqueCourseID', courses)


        gaf.section_analysis(
            df,
            user_directory=self.output_directory,
            target_courses=courses,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            min_gpa=self.min_gpa,
            max_gpa=self.max_gpa,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def command_CrsAnalysis(self):
        self.run_command_button_toggle(state="disabled")
        popup = self.threshold_popup(600, 125)
        self.create_analysis_dropdown(popup, dic.course_analysis_options, row=0, column=4)
        self.enrollment_threshold_widget('normal', popup, row=0, column=0)
        self.sections_threshold_widget('normal', popup, row=0, column=2)

        self.csv_checkbox_widget(
            where=self.popup_box_threshold, state="normal", row=2, column=0
        )
        self.grade_distribution_checkbox(
            where=self.popup_box_threshold, state="normal", row=3, column=0
        )

        self.generic_instance = gaw.tkDropdown(
            self.popup_box_threshold,
            row=1,
            column=4,
            options_dict={
                course: False for course in ["Department Courses", "Manual Select"]
            },
            initial_message="Select Course",
            allow_multiple_entries=True,
            command=self.update_generic_instance_course,
        )
        self.confirm_threshold_choice(self.run_crs_analysis)

    def run_crs_analysis(self):
        if self.generic_instance.isEmpty():
            courses = gaf.get_unique_crs(self.dataframe)
        else:
            courses = self.generic_instance.get_selected_options()

        gaf.CourseAnalysis(
            self.dataframe,
            self.output_directory,
            self.min_enrollment,
            courses,
            self.max_enrollment,
            self.min_sections,
            self.max_sections,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def update_generic_instance_course(self):
        option = self.generic_instance.get_selected_options()[0]
        if option == "Department Courses":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(dept): False for dept in gaf.get_unique_dept(self.dataframe)},
                initial_message="Get Department Courses",
                allow_multiple_entries=True,
            )

        if option == "Manual Select":
            self.generic_instance.destroy()
            self.generic_instance = gaw.tkDropdown(
                self.popup_box_threshold,
                row=1,
                column=4,
                options_dict={str(crs): False for crs in gaf.get_unique_crs(self.dataframe)},
                initial_message="Get Courses Manually",
                allow_multiple_entries=True,
            )

    def command_StudentLevelAnalysis(self):
        self.run_command_button_toggle(state="disabled")

        popup = self.threshold_popup(500, 125)

        self.class_size_threshold_widget('normal', popup, row=0, column=0)

        self.csv_checkbox_widget(
            where=popup, state="normal", row=1, column=4
        )

        self.grade_distribution_checkbox(
            state='normal', where=popup, row=2, column=4
        )

        self.create_analysis_dropdown(
            popup, dic.studentlevel_analysis_options, row=0, column=4
        )
        self.confirm_threshold_choice(self.run_student_level_analysis)

    def run_student_level_analysis(self):
        gaf.student_level_analysis(
            self.dataframe,
            user_directory=self.output_directory,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
                "Generate Grade Distribution?"
            ),
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def command_CourseLevelAnalysis(self):
        self.run_command_button_toggle(state="disabled")

        popup = self.threshold_popup(500, 125)

        self.create_analysis_dropdown(popup, dic.courselevel_analysis_options, row=0, column=4)

        self.class_size_threshold_widget('normal', popup, row=0, column=0)

        self.csv_checkbox_widget(
            where=popup, state="normal", row=1, column=4
        )

        self.grade_distribution_checkbox(
            state='normal', where=popup, row=2, column=4
        )
        self.confirm_threshold_choice(self.run_course_level_analysis)

    def run_course_level_analysis(self):
        gaf.course_level_analysis(
            self.dataframe,
            user_directory=self.output_directory,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
            generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get("Generate Grade Distribution?")
        )
        self.hyperlink_filepath()
        self.reset_gui()

    def command_StudentCourseLevelAnalysis(self):
        self.run_command_button_toggle(state="disabled")

        popup = self.threshold_popup(500, 100)

        self.class_size_threshold_widget('normal', popup, row=0, column=0)

        self.create_analysis_dropdown(where=popup, analysis_options=dic.studentcourse_analysis_options, row=0, column=4)

        self.csv_checkbox_widget(
            where=popup, state="normal", row=1, column=4
        )

        self.confirm_threshold_choice(self.run_student_course_level_analysis)

    def run_student_course_level_analysis(self):
        gaf.studentCourse_level_analysis(
            self.dataframe,
            user_directory=self.output_directory,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File")
        )

        self.hyperlink_filepath()
        self.reset_gui()


    def command_LevelAnalysis(self):
        popup = self.threshold_popup(250, 125)
        popup.title("Choose Level Analysis")
        level_analysis_checkbox = gaw.CheckboxWidget()
        level_analysis_checkbox.create_multiple_checkboxes(options={"Course Level Analysis": "Does various analysis on the course number level (1000,2000...)", "Student Level Analysis": "Does various analysis on the student level(Freshman, Sophmore)...","Student-Course Level Analysis": "Categorizes Students and Course level and does analysis on them (Freshman in 1000 level courses)"}, flags=["normal", "normal", "normal"], state='normal', where=popup, row=0, column=0)
        confirm = gaw.ConfirmButton()
        confirm.make_confirm_button(where=popup, command=lambda: self.run_level_analysis(level_analysis_checkbox, popup), row=3, column=0)

    def run_level_analysis(self, checkboxes, popup):
        TFvalues = checkboxes.get_dict_of_checkbox()
        if TFvalues.get("Course Level Analysis"):
            self.command_CourseLevelAnalysis()
            popup.destroy()
        if TFvalues.get("Student Level Analysis"):
            self.command_StudentLevelAnalysis()
            popup.destroy()
        if TFvalues.get("Student-Course Level Analysis"):
            self.command_StudentCourseLevelAnalysis()
            popup.destroy()

    def command_student_analysis(self):
        self.logger.info("Executing Student Analysis command")
        self.run_command_button_toggle(state="disabled")

        popup = self.threshold_popup(500, 125)

        self.course_num_taken_threshold_widget('normal', popup, row=0, column=0)

        self.create_analysis_dropdown(where=popup, analysis_options=dic.student_analysis_options, row=0, column=3)

        self.csv_checkbox_widget(
            where=popup, state="normal", row=1, column=3
        )

        self.grade_distribution_checkbox(
            state='normal', where=popup, row=2, column=3
        )

        self.confirm_threshold_choice(self.run_student_analysis)
        self.logger.info("Student Analysis command setup completed")

    def run_student_analysis(self):
        self.logger.info("Running student analysis")
        gaf.student_analysis(
            self.dataframe,
            user_directory=self.output_directory,
            min_enrollments=self.min_enrollment,
            max_enrollments=self.max_enrollment,
            csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File")
        )

        self.hyperlink_filepath()
        self.logger.info("Student analysis completed")
        self.reset_gui()



    # def command_All_Commands(self):
    #     self.logger.info("Executing 'Run All Commands'")
    #     self.commands_listbox.grid_forget()

    #     self.run_command_button_toggle(state="disabled")

    #     self.departments_listbox_widget(row=3, column=0)
    #     self.majors_listbox_widget(row=3, column=1)
    #     self.faculty_listbox_widget(row=3, column=2)
    #     self.csv_checkbox_widget(where=self.root, state="normal", row=2, column=0)
    #     self.grade_distribution_checkbox(
    #         where=self.root, state="normal", row=2, column=2
    #     )
    #     self.thresholds_on_root(which="sections_enrollment")
    #     self.confirm_faculty_dept_major_selection()
    #     self.logger.debug("'Run All Commands' setup completed")

    # def run_every_command(self):
    #     self.logger.info("Running all commands")
    #     self.get_thresholds()
    #     gaf.save_unique_entries(self.dataframe, user_directory=self.output_directory)

    #     gaf.MajorDepartmentAnalysis(
    #         self.dataframe,
    #         self.dept,
    #         self.major,
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         min_sections=self.min_sections,
    #         max_sections=self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     gaf.DepartmentAnalysis(
    #         self.dataframe,
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         min_sections=self.min_sections,
    #         max_sections=self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     gaf.InstructorAnalysis(
    #         self.dataframe,
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         min_sections=self.min_sections,
    #         max_sections=self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     gaf.MajorAnalysis(
    #         self.dataframe,
    #         self.output_directory,
    #         self.min_enrollment,
    #         self.max_enrollment,
    #         self.min_sections,
    #         self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     gaf.section_analysis(
    #         self.dataframe,
    #         self.output_directory,
    #         target_courses="Calculus I",
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         min_sections=self.min_sections,
    #         max_sections=self.max_sections,
    #         generate_grade_dist=self.grade_dist_checkbox.get_dict_of_checkbox().get(
    #             "Generate Grade Distribution?"
    #         ),
    #     )

    #     gaf.CourseAnalysis(
    #         self.dataframe,
    #         self.output_directory,
    #         self.min_enrollment,
    #         self.max_enrollment,
    #         self.min_sections,
    #         self.max_sections,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #     )

    #     gaf.student_level_analysis(
    #         self.dataframe,
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #     )
    #     gaf.course_level_analysis(
    #         self.dataframe,
    #         heatmap=self.heatmap_checkbox.get_dict_of_checkbox().get("Heatmap"),
    #         user_directory=self.output_directory,
    #         min_enrollments=self.min_enrollment,
    #         max_enrollments=self.max_enrollment,
    #         csv=self.csv_checkbox.get_dict_of_checkbox().get("CSV File"),
    #     )

    #     self.hyperlink_filepath()
    #     self.reset_gui()
    #     self.logger.debug("All commands executed")

    def create_random_data(self, num_rows = 40000):
        rand_df = randData.create_random_dataframe(num_rows = num_rows)
        rand_df.to_csv('random_csv')
        self.update_filestate(file=gaf.file_path('random_df.csv'), which=self.input_file_name)
        print('Input File updated, Dataframe changed, to undo this, change the path of the input file')
        self.dataframe = gaf.pd.read_csv(gaf.file_path(self.input_file_name))



if __name__ == "__main__":
    GradingAnalysisTool()  # Run the tool
