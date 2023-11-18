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


class GradingAnalysisTool:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grading Analysis Tool")
        self.root.configure()
        self.terminal_output = None
        self.root.configure(
            background='#DCDCDC',
            bd=2,
            padx=10,
            pady=10,
            highlightbackground='black',
            highlightcolor='white',
            highlightthickness=1,
            width=600,
            height=500
        )


        self.min_sections_threshold = None #
        self.max_sections_threshold = None #
        self.popup_box_threshold = None
        self.analysis_checkbox = None
        self.csv_checkbox = None

        # 

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
        
        self.required_files = None
        self.commands_directory = None
        # Setup commands and GUI
        self.root.geometry("")
        self.setup_commands()
        self.setup_gui()   # Run GUI setup


    def setup_gui(self):

        self.required_files = ["instTable.csv", "deptTable.csv", "filteredData.csv", "majorTable.csv", "courseTable.csv"]

         
        self.pre_processor_check() 

        self.create_json_file()
          
        self.commands_listbox_widget()

        self.change_sourcefile_button()

        self.populate_current_file_state()
 
        tk.Button(self.root, text="Reset", command=self.reset_button).grid(row=6, column=2)
        self.run_command_button_toggle(state = "normal")
        tk.Button(self.root, text="Help", command=self.run_selected_help_command).grid(row=7, column=2)

        self.write_to_GUI()
                
        self.dynamic_resizing()
        
        self.root.iconphoto(False, tk.PhotoImage(file='/home/mariom/Work/EDMLab/Grading Analysis/Athletic_Logo_Block_F.png'))

        self.root.mainloop()



####################################################################################################
##Thresholds

    def thresholds_widget(self, state='disabled', where=None, which=None):
        if where is None:
            where=self.root
        


        if which == 'enrollment':
            self.min_enrollment_threshold = gaw.ThresholdWidget()
            self.min_enrollment_threshold.generic_thresholds_widget(where=where, state=state, text='Minimum Enrollment threshold:', row=0, column=0, help='Enter an integer for a threshold')

            self.max_enrollment_threshold = gaw.ThresholdWidget()
            self.max_enrollment_threshold.generic_thresholds_widget(where=where, state=state, text='Maximum Enrollment threshold:', row=1, column=0, help='Enter an integer for a threshold')

        elif which == 'sections':
            self.min_sections_threshold = gaw.ThresholdWidget()
            self.min_sections_threshold.generic_thresholds_widget(where=where, state=state, text='Minimum Sections threshold:', row=0, column=2, help='Enter an integer for a threshold')
            
            self.max_sections_threshold = gaw.ThresholdWidget()
            self.max_sections_threshold.generic_thresholds_widget(where=where, state=state, text='Maximum Sections threshold:', row=1, column=2, help='Enter an integer for a threshold')
        elif which == 'sections_enrollment':
            self.min_enrollment_threshold = gaw.ThresholdWidget()
            self.min_enrollment_threshold.generic_thresholds_widget(where=where, state=state, text='Minimum Enrollment threshold:', row=0, column=0, help='Enter an integer for a threshold')

            self.max_enrollment_threshold = gaw.ThresholdWidget()
            self.max_enrollment_threshold.generic_thresholds_widget(where=where, state=state, text='Maximum Enrollment threshold:', row=1, column=0, help='Enter an integer for a threshold')

            self.min_sections_threshold = gaw.ThresholdWidget()
            self.min_sections_threshold.generic_thresholds_widget(where=where, state=state, text='Minimum Sections threshold:', row=0, column=2, help='Enter an integer for a threshold')
            
            self.max_sections_threshold = gaw.ThresholdWidget()
            self.max_sections_threshold.generic_thresholds_widget(where=where, state=state, text='Maximum Sections threshold:', row=1, column=2, help='Enter an integer for a threshold')

        return

    def csv_checkbox_widget(self, state='disabled', where=None):
        if where is None:
            where=self.root

        self.csv_checkbox = gaw.CheckboxWidget()
        self.csv_checkbox.create_checkbox(where=where, text='CSV File',state=state, row=0, column=4, help_text='Check this box to create a csv')
        
    def create_analysis_checkboxes(self, where=None):
        if where is None:
            where = self.root

        #Each checkbox is a dictionary with the key being the name of the checkbox and the value being the help text
        analysis_options = {
            'GPA Analysis': 'Check for GPA Analysis',
            'Enrollment Analysis': 'Check for Enrollment Analysis',
            'Combined Analysis': 'Check for Combined Analysis'
        }
        self.analysis_checkbox = gaw.CheckboxWidget()
        self.analysis_checkbox.create_multiple_checkboxes(options=analysis_options, state='normal', where=where, row=0, column=5)

        
    def threshold_popup(self, which):
        self.popup_box_threshold = tk.Toplevel(self.root)
        self.popup_box_threshold.title("Threshold")
        self.popup_box_threshold.geometry("700x100")

        self.thresholds_widget(state='normal', where=self.popup_box_threshold, which=which)
        self.create_analysis_checkboxes(where=self.popup_box_threshold)
        self.csv_checkbox_widget(state='normal', where=self.popup_box_threshold)

    def confirm_threshold_choice(self, command=None):
        tk.Button(self.popup_box_threshold, text="Go", command=lambda: self.run_command_confirm_threshold(command), width=4).grid(row=2, column=2)

    def run_command_confirm_threshold(self, command):
        self.get_thresholds()
        command()
        self.reset_gui()

    def get_thresholds(self):
        min_enrollment_threshold = self.min_enrollment_threshold.get_entry_value()
        max_enrollment_threshold = self.max_enrollment_threshold.get_entry_value()
        min_sections_threshold = self.min_sections_threshold.get_entry_value()
        max_sections_threshold = self.max_sections_threshold.get_entry_value()
        
        self.min_enrollment = min_enrollment_threshold if min_enrollment_threshold else None
        self.max_enrollment = max_enrollment_threshold if max_enrollment_threshold else None
        self.min_sections = min_sections_threshold if min_sections_threshold else None
        self.max_sections = max_sections_threshold if max_sections_threshold else None

##################################################################################
##History File .history.json

    def update_filestate(self, file, which):
        history_path = os.path.join(os.getcwd(), '.history.json')
        
        # Update the appropriate attribute based on which
        if which is self.input_file_name:
            self.input_file_name = file
        elif which is self.output_directory:
            self.output_directory = file
        elif which is self.course_table_file:
            self.course_table_file = file
        elif which is self.department_file:
            self.department_file = file
        elif which is self.instructor_file:
            self.instructor_file = file
        elif which is self.major_file:
            self.major_file = file

        # Update .history.json
        if os.path.exists(history_path):
            with open(history_path, 'w') as f:
                history = {
                    "inputfile": str(self.input_file_name),
                    "outputfile": str(self.output_directory),
                    "coursetablefile": str(self.course_table_file),
                    "departmentfile": str(self.department_file),
                    "instructorfile": str(self.instructor_file),
                    "majorfile": str(self.major_file)
                }
                json.dump(history, f)
        else:
            self.create_json_file()

#################################################################################
##Commands
    def setup_commands(self):
        self.commands_directory = {
        "Unique List": self.command_UniqueList,
        "Calculate GPA": self.command_GPA,
        "Faculty Analysis": self.command_FacultyAnalysis,
        "Department Enrollments": self.command_DeptEnroll,
        "Student Major Count": self.command_StudMjrCount,
        "Department Analysis": self.command_DeptAnalysis,
        "Instructor Analysis": self.command_InstAnalysis,
        "Major Analysis": self.command_MjrAnalysis,
        "Course Analysis": self.command_CrsAnalysis,
        "Run All Commands": self.command_All_Commands,
        "Quit": self.quit_program
        }

    def place_commands(self):
        for command in self.commands_directory.keys():
            self.commands_listbox.insert(parent="", index=tk.END, values=(command,))


##########################################################################################
##specific functions

    def quit_program(self):
        exit()
        
    def dynamic_resizing(self):
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            
    def reset_button(self):
        self.terminal_output = None
        self.reset_gui()
        
    def pre_processor_check(self):
        for file_name in self.required_files:
            full_path = os.path.join(os.getcwd(), file_name)
            if not os.path.isfile(full_path):
                messagebox.showerror("Preprocessor Check Failed", f"Please run the preprocessor file to use the GUI. Missing file: {file_name}")
                sys.exit()
        return

        
    def run_command_button_toggle(self, state = "normal"):
        tk.Button(self.root, text="Run Command", command=self.run_selected_commands, state=state).grid(row=7, column=0, pady=10)


##use this all the time
    def bind_tooltip_events(self, widget, text):
        # Bind tooltip show and hide events to a widget
        tooltip = gaw.ToolTip(widget, text)
        widget.bind("<Enter>", lambda event: tooltip.showtip())
        widget.bind("<Leave>", lambda event: tooltip.hidetip())

    
    def write_to_GUI(self):
        if self.terminal_output is None:
            self.terminal_output = gaw.Console(self.root)
            self.terminal_output.grid(row=9, rowspan=3, column=0, columnspan=10, sticky="nsew")
            self.terminal_output.write("Terminal Display:\n\n\n\n\n\n")
        else:
            return


        

##Gets the content of the terminal_output Text widget from the beginning to the end.
# Split the content into lines and create a counter
# Check if the line contains the phrase "File Created:".
# If found, split the line into two parts. The left part will be ignored, and the right part will be the file path.
# Increment the line number counter for the next iteration.

    def hyperlink_filepath(self):
        content = self.terminal_output.get("1.0", tk.END)
        lines = content.split('\n')
        arrlines = []
        for line_number, line in enumerate(lines, start=1):
            if "File Created:" in line:
                _, file_path = line.split("File Created:")
                file_path = file_path.strip()
                arrlines.append((line_number, line, file_path))
        for arrline in arrlines:
                self.create_hyperlink(hyperlink_tuple=arrline)

    def create_hyperlink(self, hyperlink_tuple):
        line_number, line, file_path = hyperlink_tuple
        col_start = line.find(file_path)
        if col_start != -1: 
            start_index = f"{line_number}.{col_start}"
            end_index = f"{line_number}.{col_start + len(file_path)}"
            file_opener = self.file_dict.get(file_path)
            if file_opener is None:
                file_opener = gaw.FileOpener(file_path)
                self.file_dict[file_path] = file_opener
                a = (start_index, end_index, file_path)
                self.hyperlink_binds(a)

    def process_hyperlinks(self, hyperlink_tuples):
        for hyperlink_tuple in hyperlink_tuples:
            self.create_hyperlink(hyperlink_tuple)

    def clicked_hyperlink(self, file_path, event=None):
        self.file_dict.get(file_path).open_file()


    def hyperlink_binds(self, tuple):
        (start, end, file_path) = tuple
        unique_tag = f"hyperlink_{start}_{end}"  # Create a unique tag

        self.terminal_output.config(state="normal")
        self.terminal_output.tag_add(unique_tag, start, end)
        self.terminal_output.tag_config(unique_tag, foreground="blue", underline=1)
        self.terminal_output.tag_bind(unique_tag, "<Button-1>", lambda event: self.clicked_hyperlink(file_path))
        self.terminal_output.config(state="disabled")

################################################################################################################################################

    def reset_gui(self):
        # Reset state variables
        self.dept = None
        self.major = None
        self.faculty = None
        self.min_enrollment_threshold = None 
        self.max_enrollment_threshold = None

        
        for widget in [ self.departments_listbox, self.faculty_listbox, self.popup_box_threshold, self.csv_checkbox, self.analysis_checkbox,
                        self.majors_listbox, self.commands_listbox, self.unique_listbox, self.max_sections_threshold, self.min_sections_threshold, 
                        self.min_enrollment_threshold, self.max_enrollment_threshold, 
                        ]:
            if widget is not None:
                widget.destroy()
        try:
            self.setup_gui()
        except Exception as e:
            print(f"An error occurred while setting up the GUI: {e}")
##############################################################################################
#input and output directory

    #history to remember the files that the user selected as the input csv and output files checks if the file exists and if it does
    #exits the file, and if it doesn't exist (first startup), creates them with preset paths

    def create_json_file(self):
        history_path = os.path.join(os.getcwd(), '.history.json')
        if os.path.exists(history_path):
            return
        else:
            self.input_file_name = str(os.path.join(os.getcwd(), 'filteredData.csv'))
            self.output_directory = str(os.path.join(os.getcwd(), 'grading_analysis_output'))
            self.course_table_file = str(os.path.join(os.getcwd(), 'courseTable.csv'))
            self.department_file = str(os.path.join(os.getcwd(), 'deptTable.csv'))
            self.instructor_file = str(os.path.join(os.getcwd(), 'instTable.csv'))
            self.major_file = str(os.path.join(os.getcwd(), 'majorTable.csv'))

            with open(history_path, 'w') as f:
                history = {
                    "inputfile": self.input_file_name,
                    "outputfile": self.output_directory,
                    "coursetablefile": self.course_table_file,
                    "departmentfile": self.department_file,
                    "instructorfile": self.instructor_file,
                    "majorfile": self.major_file
                }
                json.dump(history, f)



    #read the json (on reset) or when theres changes in the file
    def populate_current_file_state(self):        
        history_path = os.path.join(os.getcwd(), '.history.json')

        if os.path.exists(history_path):
            with open('.history.json', 'r') as f:
                content = f.read()

                if content:
                    try:
                        file_data = json.loads(content)
                    except json.JSONDecodeError:
                        self.create_json_file()
                        return

                    self.input_file_name = file_data.get('inputfile')
                    self.output_directory = file_data.get('outputfile')
                    self.department_file = file_data.get('departmentfile')
                    self.instructor_file = file_data.get('instructorfile')
                    self.major_file = file_data.get('majorfile')
                    self.course_table_file = file_data.get('coursetablefile')
                else:
                    self.create_json_file()


    #main gui change button
    def change_sourcefile_button(self):
        button = tk.Button(self.root, text="File Paths", command=self.sources_popup)
        button.grid(row=6, column=0)

    #popup containing all the paths that are changeable and needed. If more are needed, put here following the format seen
    def sources_popup(self):
        source_popup = tk.Toplevel(self.root)
        source_popup.title("Source paths")
        self.file_path_browse_widget(source_popup, row=0, column=0, text="Input File:", file=str(self.input_file_name), set_command=self.file_call, required_file=self.input_file_name)
        self.file_path_browse_widget(source_popup, row=1, column=0, text="Output directory:", file=str(self.output_directory), set_command=self.file_call, required_file=self.output_directory, directory=True)
        self.file_path_browse_widget(source_popup, row=2, column=0, text="Department file:", file=str(self.department_file), set_command=self.file_call, required_file=self.department_file)
        self.file_path_browse_widget(source_popup, row=3, column=0, text="Instructor file:", file=str(self.instructor_file), set_command=self.file_call, required_file=self.instructor_file)
        self.file_path_browse_widget(source_popup, row=4, column=0, text="Major file:", file=str(self.major_file), set_command=self.file_call, required_file=self.major_file)
        self.file_path_browse_widget(source_popup, row=5, column=0, text="Course Table file:", file=str(self.course_table_file), set_command=self.file_call, required_file=self.course_table_file)
        tk.Button(source_popup, text="Close", command=source_popup.destroy).grid(row=6, column=1)

    #label with the path of file and also the browse button
    def file_path_browse_widget(self, where, row, column, text, file, set_command, required_file, directory=False):
        label = tk.Label(where, text=text)
        label.grid(row=row, column=column, sticky=tk.W)
        file_path = tk.Label(where, text=file)
        file_path.grid(row=row, column=column+1)
        if directory:
            browse = tk.Button(where, text="Browse", command=lambda: set_command(file_path, file, required_file, directory=True))
        else:
            browse = tk.Button(where, text="Browse", command=lambda: set_command(file_path, file, required_file))

        browse.grid(row=row, column=column+2)

    #file call mainly for csv and directory
    def file_call(self, button = tk.Label, file=str, required_file=None, directory=False):
        if directory:
            file_dir = filedialog.askdirectory()
            file = str(file_dir)

        else:
            file_dir = filedialog.askopenfile()
            file = str(file_dir.name)
        
        self.update_filestate(file=file, which=required_file)
        button.config(text=str(file))



##########################################################################################################
#populate widgets

#any list that needs population gets population here.

    def populate_majors_listbox(self):
        self.majors = gaf.df['Major'].unique().tolist()
        self.majors.sort()
        
        for major in self.majors:
            self.majors_listbox.insert(parent='', index=tk.END, values=(major,))

    def populate_department_listbox(self):
        self.departments = gaf.df['Department'].unique().tolist()
        self.departments.sort()
        
        for dept in self.departments:
            self.departments_listbox.insert(parent='', index=tk.END, values=(dept,))

    def populate_faculty_listbox(self):
        self.faculty_set = gaf.df['FacultyID'].unique().tolist()
        
        for faculty in self.faculty_set:
            self.faculty_listbox.insert(parent='', index=tk.END, values=(faculty,))

    def populate_unique_listbox(self):
        self.unique_list = ["Departments", "Majors", "Instructor IDs", "Courses", "UniqueCourseID", "Student IDs", "All"]
        
        for unique in self.unique_list:
            self.unique_listbox.insert(parent='', index=tk.END, values=(unique,))

################################################################################################################
#Help popups

#code for the popup and the close button on the popup, below is the text
    def popup(self, title = "", popup_text = "", ):
        messageBox = tk.Toplevel()
        label = tk.Label(messageBox, text=title)
        label.pack()
        show_help_info = tk.Label(messageBox, text=popup_text, justify="left")
        show_help_info.pack()
        button_close = tk.Button(messageBox, text="Close", command=messageBox.destroy)
        button_close.pack()

    #simple if elif for all the help commands. Simple to expand
    def popup_text(self, help_output):
        if help_output == "Unique List":
            self.popup(title="Unique List Help", popup_text="This command will display all the unique items in your chosen list. For example, if you select departments, you will get a unique list of all the departments.")
        elif help_output == "Calculate GPA":
            self.popup(title="Calculate GPA Help", popup_text="\nCompute the GPA of all courses in the university, all courses in the department, all students that are \n majoring in a specific major taking any course (related or unrelated to their major), all students that are \n majoring in a specific major taking any course in their major's department, and the grades standard deviation. \n Also, generates a table of student grade distribution of all courses and a table with instructor-weighted GPA \n distribution.\n")
        elif help_output == "Faculty Analysis":
            self.popup(title="Faculty Analysis Help", popup_text="\nProvides the grade analysis of a faculty across all the courses and departments they teach based on their faculty ID")
        elif help_output == "Department Enrollments":
            self.popup(title="Department Enrollments Help", popup_text="\nProvides a table of the student enrollment in each department.")
        elif help_output == "Student Major Count":
            self.popup(title="Student Major Count Help", popup_text="\nProvides a table with number of students in each major")
        elif help_output == "Department Analysis":
            self.popup(title="Department Analysis Help", popup_text="\nA bar chart of department grades, department size, number of enrollments and department GPA. Also, \n generates a scatter plot of total number of students in a department and grades in that department. All \n illustrations have a threshold of departments with enrollments > 600.")
        elif help_output == "Instructor Analysis":
            self.popup(title="Instructor Analysis Help", popup_text="\ninstructor Grade Distribution (histogram) -- frequency of grades and a threshold version, \n excluding inst teaching < 10 sections; instructor Enrollment Distribution (histogram), and a threshold version \n where number of students taught(enrollments) > 200.\n\n")
        elif help_output == "Major Analysis":
            self.popup(title="Major Analysis Help", popup_text="\ngpa vs major size (number of enrollments) scatter plot, and a threshold version for majors with \n > 10,000 enrollments; and major vs enrollments bar chart, for majors with > 10,000 enrollments\n\n")
        elif help_output == "Course Analysis":
            self.popup(title="Course Analysis Help", popup_text="\nCreates a graph of grade distribution of courses with over 70 sections")
        elif help_output == "Run All Commands":
            self.popup(title="Run All Commands Help", popup_text="\nRuns all the commands above.")
        else:
            self.popup(title="Help", popup_text="""
            For extensive help with an individual command, select the command, then press help           
            
            1.)     Unique List: Get a list of all unique departments, majors, instructors, courses, UniqueCourseID, and students.
            
            2.)     Calculate GPA: Compute the GPA of all courses in the university.
            
            3.)     Faculty Analysis: Compute the GPA over all faculty's courses, grades standard deviation, and lowest and highest grades.
            
            4.)     Department Enrollments: Create a table with the number of enrollments per department.
            
            5.)     Student Major Count: Create a table with the number of students per major.
            
            6.)     Department Analysis: bar chart of department grades, department size, number of enrollments and department GPA.
            
            7.)     Instructor Analysis: instructor Grade Distribution (histogram)
            
            8.)     Major Analysis: gpa vs major size (number of enrollments) scatter plot
            
            9.)     Course Analysis: distribution of grades bar chart for courses with > 70 sections
            
            10.)    Run All Commands: run all commands above
            """)


##########################################################################################################
#listbox widgets

    #one generic listbox used for all functions which have a choice of multiple operations.
    #Convert these to classes is on the todo

    def commands_listbox_widget(self, row=3, column=1):
        self.commands_listbox = gaw.TableWidget()
        self.commands_listbox.generic_tableview_widget(where=self.root, row=row, column=column, colHeading="commands" , title="Command(s):", helptip="Select a command to run .")
        self.place_commands()

    def faculty_listbox_widget(self, row=3, column=1):
        self.faculty_listbox = gaw.TableWidget()
        self.faculty_listbox.generic_tableview_widget(where=self.root, row=row, column=column, colHeading="faculty", title="Faculty:", helptip="Which Faculty? Select a valid Faculty")
        self.populate_faculty_listbox()

    def departments_listbox_widget(self, row=3, column=1):
        self.departments_listbox = gaw.TableWidget()
        self.departments_listbox.generic_tableview_widget(where=self.root, row=row, column=column, colHeading="department", title="Department:", helptip="Which department? Select a valid Department")
        self.populate_department_listbox()

    def majors_listbox_widget(self, row=3, column=1):
        self.majors_listbox = gaw.TableWidget()
        self.majors_listbox.generic_tableview_widget(where=self.root, row=row, column=column, colHeading="major", title="Major:", helptip="Which major? Select a valid Major")
        self.populate_majors_listbox()

    def unique_listbox_widget(self, row=3, column=1):
        self.unique_listbox = gaw.TableWidget()
        self.unique_listbox.generic_tableview_widget(where=self.root, row=row, column=column, colHeading="unique", title="Enter Unique List Request:", helptip="Which Entry? Select a valid Entry")
        self.populate_unique_listbox()
            
            
##########################################################################################################
#confirm widgets
    
    #Generic confirm button which just sets a command passed to it that does the operation meant to do when pressed. 


    def confirm_department_major_selections(self):
        confirm_button = gaw.ConfirmButton()
        confirm_button.make_confirm_button(where=self.root, command=self.set_choices_department_major, row=4, column=1, helptip="Confirm Major and Department")

    def confirm_faculty_selection(self):
        confirm_button = gaw.ConfirmButton()
        confirm_button.make_confirm_button(where=self.root, command=self.set_choices_faculty, row=4, column=1, helptip="Confirm Faculty")

    def confirm_unique_selection(self):
        confirm_button = gaw.ConfirmButton()
        confirm_button.make_confirm_button(where=self.root, command=self.set_choices_unique, row=4, column=1, helptip="Confirm Unique")

    def confirm_faculty_dept_major_selection(self):
        confirm_button = gaw.ConfirmButton()
        confirm_button.make_confirm_button(where=self.root, command=self.set_choices_department_major_faculty_selection, row=4, column=1, helptip="Confirm Selections")

        
##########################################################################################################
#set choices widgets
        
    def set_choices_department_major(self):
        if self.departments_listbox.selection() and self.majors_listbox.selection():
            self.dept = self.departments_listbox.item(self.departments_listbox.selection())
            self.major = self.majors_listbox.item(self.majors_listbox.selection())
            self.run_GPA_analysis()
            self.reset_gui()

    def set_choices_department_major_faculty_selection(self):
        if self.departments_listbox.selection() and self.majors_listbox.selection() and self.faculty_listbox.selection():
            self.dept = self.departments_listbox.item(self.departments_listbox.selection())
            self.major = self.majors_listbox.item(self.majors_listbox.selection())
            self.faculty = self.faculty_listbox.item(self.faculty_listbox.selection())

            self.run_every_command()
            self.reset_gui()

    def set_choices_faculty(self):
        if self.faculty_listbox.selection():
            self.faculty = self.faculty_listbox.item(self.faculty_listbox.selection())
            self.run_faculty_analysis()
            self.reset_gui()

    def set_choices_unique(self):
        if self.unique_listbox.selection():
            self.unique_selection = self.unique_listbox.item(self.unique_listbox.selection())
            self.run_unique_analysis()
            self.reset_gui()

##########################################################################################################
##run

    #specific to when the help button is clicked when user has a command highlighted, runs the popup text command with the command
    #highlighted and outputs a specific help to that command. works the same way as the main run command
    
    def run_selected_help_command(self):
        selected_help_command = self.commands_listbox.selection()
        
        if selected_help_command:
            help_output = self.commands_listbox.item(selected_help_command)
            self.popup_text(help_output=help_output)
        else:
            self.popup_text(help_output="Help")

    #runs the highlighted command after 'run command' is clicked
    
    def run_selected_commands(self):
        selected_item = self.commands_listbox.selection()
        retrieved_command = str(self.commands_listbox.item(self.commands_listbox.selection()))
        if selected_item is not None:
            if retrieved_command in self.commands_directory:
                try:
                    command_function = self.commands_directory[retrieved_command]
                    command_function()
                except Exception as e:
                    print(f"An error occurred while running the command {retrieved_command}: {e}")

            
##########################################################################################################
#commands


    #What happens after gpa command is confirmed
    def command_GPA(self):
        self.commands_listbox.grid_forget()
        
        self.run_command_button_toggle(state = "disabled")
        #creates listboxes for selection and waits for confirm to be clicked
        self.departments_listbox_widget(row=3, column=1)
        
        self.majors_listbox_widget(row=5, column=1)
        
        #runs analysis
        self.confirm_department_major_selections()


    #Runs analysis of gpa command
    def run_GPA_analysis(self):
        if self.dept not in gaf.uniqueDept:
            self.dept = gaf.checkMultiple(self.dept, list(gaf.uniqueDept))
        if self.major not in gaf.uniqueMjr:
            self.major = gaf.checkMultiple(self.major, list(gaf.uniqueMjr))
        if self.dept in gaf.uniqueDept and self.major in gaf.uniqueMjr:
            gaf.UniversityCoursesMean(gaf.df)
            gaf.AllCoursesGradeDist(gaf.df)
            gaf.GradeDist(gaf.df)
            gaf.DepartmentCoursesMean(gaf.df, self.dept)
            gaf.MajorDegreeMean(gaf.df, self.major)
            gaf.MajorDeptMean(gaf.df, self.major, self.dept)
        self.reset_gui()
            



    def command_FacultyAnalysis(self):
        self.commands_listbox.grid_forget()
        
        self.run_command_button_toggle(state = "disabled")
        
        self.faculty_listbox_widget(row=3, column=0)
        
        self.populate_faculty_listbox()
        
        self.confirm_faculty_selection()

    def run_faculty_analysis(self):
        if self.faculty not in gaf.uniqueInst:
            self.faculty = gaf.checkMultiple(self.faculty, list(gaf.uniqueInst))
        if self.faculty in gaf.uniqueInst:
            gaf.FacultyAnalysis(gaf.df, self.faculty) 
        self.reset_gui()

    def command_DeptEnroll(self):
        gaf.DeptEnroll(gaf.df)
        self.reset_gui()    


    def command_StudMjrCount(self):
        gaf.StudMjrCount(gaf.df)
        self.reset_gui()    
    

    def command_UniqueList(self):
        self.commands_listbox.grid_forget()
        self.run_command_button_toggle(state = "disabled")
        self.unique_listbox_widget()
                
        self.confirm_unique_selection()
        
    def run_unique_analysis(self):
        if (self.unique_selection == 'Departments'):
            print(gaf.uniqueDept)
        elif (self.unique_selection == 'Majors'):
            print(gaf.uniqueMjr)
        elif (self.unique_selection == 'Instructor IDs'):
            print(gaf.uniqueInst)
        elif (self.unique_selection == 'Courses'):
            print(gaf.uniqueCrs)
        elif (self.unique_selection == 'UniqueCourseID'):
            print(gaf.uniqueCRSID)
        elif (self.unique_selection == 'Student IDs'):
            print(gaf.uniqueStud)
        elif (self.unique_selection == 'All'):
            print(gaf.uniqueDept)
            print(gaf.uniqueMjr)
            print(gaf.uniqueInst)
            print(gaf.uniqueCrs)
            print(gaf.uniqueCRSID)
            print(gaf.uniqueStud)            
        else:
            print("This is not a valid option.")
            self.reset_gui()
            
    def command_DeptAnalysis(self):
        self.run_command_button_toggle(state = "disabled")
        self.threshold_popup(which='enrollment')
        self.confirm_threshold_choice(self.run_department_analysis)   

    def run_department_analysis(self):
        gaf.DeptGPA(self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.DeptSize(self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.DeptEnrollGPA(self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.DeptStudGPA(self.output_directory, self.min_enrollment, self.max_enrollment)
        self.hyperlink_filepath()
        
    def command_InstAnalysis(self):
        self.run_command_button_toggle(state = "disabled")
        self.threshold_popup(which='sections_enrollment')
        self.confirm_threshold_choice(self.run_instructor_analysis)
    
    def run_instructor_analysis(self):
        gaf.InstGPATrunc(gaf.df, self.output_directory, self.min_sections, self.max_sections, csv=self.csv_checkbox.get_selected_analyses())
        gaf.InstEnrollTrunc(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment, csv=self.checkbox.get_value())
        self.hyperlink_filepath()
        
    def command_MjrAnalysis(self):
        self.run_command_button_toggle(state = "disabled")
        self.threshold_popup(which='sections_enrollment')
        self.confirm_threshold_choice(self.run_major_analysis)

    def run_major_analysis(self):
        gaf.MjrGPATrunc(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment,csv=self.csv_checkbox.get_selected_analyses())
        gaf.MjrEnroll(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment, csv=self.csv_checkbox.get_selected_analyses())
        self.hyperlink_filepath()

    def command_CrsAnalysis(self):
        self.run_command_button_toggle(state = "disabled")
        self.threshold_popup(which='sections_enrollment')
        self.confirm_threshold_choice(self.run_crs_analysis)


    def run_crs_analysis(self):
        csv = self.csv_checkbox.get_selected_analyses()
        gaf.CourseGPA(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment, self.min_sections, self.max_sections, csv=csv, analysis='enrollment')

        self.hyperlink_filepath()
                
    
    def command_All_Commands(self):
        self.commands_listbox.grid_forget()
        
        self.run_command_button_toggle(state = "disabled")
        
        self.departments_listbox_widget(row = 3, column=0)
        
        self.majors_listbox_widget(row = 3, column=1)
        
        self.faculty_listbox_widget(row = 3, column=2)

        self.thresholds_widget(state="normal", where=self.root, which='sections_enrollment')
        
        self.confirm_faculty_dept_major_selection()

    def run_every_command(self):
        self.get_thresholds()
        gaf.UniversityCoursesMean(gaf.df)
        gaf.DepartmentCoursesMean(gaf.df, self.dept)
        gaf.MajorDegreeMean(gaf.df, self.major)
        gaf.MajorDeptMean(gaf.df, self.major, self.dept)
        gaf.FacultyAnalysis(gaf.df, self.faculty)
        gaf.AllCoursesGradeDist(gaf.df)
        gaf.DeptEnroll(gaf.df)
        gaf.StudMjrCount(gaf.df)
        gaf.GradeDist(gaf.df)
        gaf.DeptGPA(self.output_directory, self.min_enrollment, self.max_enrollment_threshold)
        gaf.DeptSize(self.output_directory)
        gaf.DeptEnrollGPA(self.output_directory)
        gaf.DeptStudGPA(self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.InstGPATrunc(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment, csv=self.csv_checkbox.get_selected_analyses())
        gaf.InstEnrollTrunc(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.MjrGPATrunc(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.MjrEnroll(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment)
        gaf.CourseGPA(gaf.df, self.output_directory, self.min_enrollment, self.max_enrollment)
        self.hyperlink_filepath()
        

if __name__ == "__main__":
    GradingAnalysisTool()   # Run the tool

