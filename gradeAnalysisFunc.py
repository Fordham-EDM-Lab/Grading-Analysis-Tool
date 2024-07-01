from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.completion import WordCompleter
import string
import random
from timeit import repeat
from pandas.core.reshape.concat import concat
from tkinter import ttk
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
import gradeAnalysisWidgets as gaw
import dictionary as dic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tabulate import tabulate
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    MaxAbsScaler,
    Normalizer,
)
def file_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), file)

plt.rcParams.update({"font.size": 14})

# save the data file as df
df = pd.read_csv(file_path("filteredData.csv"))

# get useful list of all unique departments, majors, instructors, courses, UniqueCourseID, and students
uniqueDept = df["Department"].unique()
uniqueMjr = df["Major"].unique()
uniqueInst = df["FacultyID"].unique()
uniqueCrs = df["CourseTitle"].unique()
uniqueCRSID = df["UniqueCourseID"].unique()
uniqueStud = df["SID"].unique()


# returns filtered dataframe. Each condition should be passed as column name = LIST of targets
# e.g. "filter(df, crsTitle = ['PHYSICS I LAB'], facultyID = ['F18125', 'F97128'])" returns df with 84 rows
def filter(df, **kwargs):
    for key in kwargs.keys():
        df = df[(df[key]).isin(kwargs.get(key))]
    return df


# All this is done to make a csv file with all the unique entries appearing in the given dataset. It is
# not used and is only there for refrence purposes.


def save_unique_entries(df, user_directory):
    uniquevalue = df["Department"].unique()
    uniqueMjr = df["Major"].unique()
    uniqueInst = df["FacultyID"].unique()
    uniqueCrs = df["CourseTitle"].unique()
    uniqueCRSID = df["UniqueCourseID"].unique()
    uniqueStud = df["SID"].unique()

    save_path = os.path.join(user_directory, "unique_entries.csv")

    with open(save_path, "w", newline="") as f:
        writer = csv.writer(f)

        # Write headers
        writer.writerow(
            [
                "These courses are purely informational and do not correlate between columns."
            ]
        )
        writer.writerow(
            [
                "They are the unique courses that appear in the dataset for the given column."
            ]
        )
        writer.writerow(
            [
                "Departments:",
                "Majors:",
                "FacultyIDs:",
                "CourseTitles:",
                "UniqueCourseIDs:",
                "SIDs:",
            ]
        )

        max_length = max(
            len(uniquevalue),
            len(uniqueMjr),
            len(uniqueInst),
            len(uniqueCrs),
            len(uniqueCRSID),
            len(uniqueStud),
        )

        for i in range(max_length):
            row = [
                uniquevalue[i] if i < len(uniquevalue) else "",
                uniqueMjr[i] if i < len(uniqueMjr) else "",
                uniqueInst[i] if i < len(uniqueInst) else "",
                uniqueCrs[i] if i < len(uniqueCrs) else "",
                uniqueCRSID[i] if i < len(uniqueCRSID) else "",
                uniqueStud[i] if i < len(uniqueStud) else "",
            ]
            writer.writerow(row)

        print("\n\nFile Created:", f" {save_path}\n\n")


def drop_courses_by_threshold(df, column, min_threshold=None, max_threshold=None):
    if min_threshold is not None:
        df = df[df[column] >= min_threshold]
    if max_threshold is not None:
        df = df[df[column] <= max_threshold]
    return df


def avgWeighted(df, course, weight):
    return (df[weight] * df[course]).sum() / df[weight].sum()


# generate table of student grade distribution of all courses
# a list of all unique departments, majors, instructors, courses, UniqueCourseID, and students
def unique(df):
    req = input(
        "\nWould you like a list of unique Departments, Majors, Instructor IDs, Courses, UniqueCourseID, or Student IDs?\n"
    )
    if req == "Departments":
        print("\nThese are all Departments:")
        print(uniqueDept)
    elif req == "Majors":
        print("\nThese are all Majors:")
        print(uniqueMjr)
    elif req == "Instructor IDs":
        print("\nThese are all Instructor IDs:")
        print(uniqueInst)
    elif req == "Courses":
        print("\nThese are all Courses:")
        print(uniqueCrs)
    elif req == "UniqueCourseID":
        print("\nThese are all UniqueCourseID:")
        print(uniqueCRSID)
    elif req == "Student IDs":
        print("\nThese are all Student IDs:")
        print(uniqueStud)
    else:
        print("This is not a valid option.")


# average & std grades of all students taking courses in specific department


# RESEARCH CODE:
# Function to create a list of consecutive numbers spaced out as needed (to use when creating bins for a graph)
def createList(r1, r2, space):
    if r1 == r2:
        return 0
    else:
        cl = []
        while r1 < r2 + 1:
            cl.append(r1)
            r1 += space
        return cl


# department grades bar chart (y=gpa, x=department) for departments with enrollments > 700
def coloring(dt):
    # department grades bar chart (y=gpa, x=department) for departments with enrollments > 700
    barsColor = []
    # clustering departments per area of study
    arts = {"Theatre", "Visual Arts", "Music", "Dance", "Julliard Exchange"}
    comm = {
        "Comm & Media Stud.",
        "Comm. & Culture",
        "New Media/Dig. Dsgn",
        "Digital Tech/Media",
        "Film & Television",
        "Journalism",
        "Marketing",
    }
    hum = {
        "Anthropology",
        "Afr. & Afr. Amer Stud.",
        "Art History",
        "English",
        "History",
        "Philosophy",
        "Theology",
        "Irish Stud.",
        "Classic Lang & Civ.",
        "Amer Catholic Stud.",
        "Medieval Stud.",
        "Latin Amer & Latino Stud.",
        "Comparative Lit.",
        "American Stud.",
        "Linguistics",
    }
    lang = {
        "French",
        "German",
        "Japanese",
        "Russian",
        "Arabic",
        "Latin",
        "Greek",
        "Italian",
        "Mandarin Chinese",
        "Spanish",
        "Modern Languages",
        "HEBW",
    }
    sciTec = {
        "Biological Sci.",
        "Chemistry",
        "Physics",
        "Comp & Info Sci.",
        "Math",
        "Natural Sci.",
        "Environmental Sci.",
        "Integrative Neuroscience",
        "Information Systems",
    }
    soSci = {
        "Economics",
        "Political Sci.",
        "Psychology",
        "Sociology",
        "Social Work",
        "Peace&Justice Stud.",
        "Human. Affairs",
        "Human. Stud.",
        "Ethics Education",
        "WG&S Stud.",
        "Women's Stud.",
        "Middle East Studies",
        "International Stud.",
        "Urban Stud.",
        "Environmental Policy",
        "Environmental Stud.",
        "Management",
    }
    dt.sort_courses("GPA W", inplace=True)
    uniquevalue = dt["Department"].unique()
    for dpt in uniquevalue:
        if dpt in arts:
            color = "#e6ae6e"  # orangy
        elif dpt in hum:
            color = "#e6ae6e"  # orangy
        elif dpt in lang:
            color = "#e6ae6e"  # orangy
        elif dpt in comm:
            color = "#94bff7"  # light blue
        elif dpt in soSci:
            color = "#94bff7"  # sky blue
        elif dpt in sciTec:
            color = "#18979e"  # teal
        else:
            color = "#000000"  # black
        barsColor.append(color)

    return barsColor


def check_list_is_subset(target_list, check_list):
    return set(target_list).issubset(check_list)


def MajorDepartmentAnalysis(
    df,
    department,
    major,
    user_directory=None,
    min_enrollments=None,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    generate_grade_dist=False,
):
    deptTable = pandas_df_agg(df, "Department")
    mjrTable = pandas_df_agg(df, "Major")

    deptTable = deptTable[deptTable["Department"] == department]
    mjrTable = mjrTable[mjrTable["Major"] == major]

    if csv:
        save_path = os.path.join(user_directory, f"{department}_data.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        deptTable.to_csv(save_path, encoding="utf-8-sig")
        save_path = os.path.join(user_directory, f"{major}_data.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        mjrTable.to_csv(save_path, encoding="utf-8-sig")

    if generate_grade_dist:
        graph_grade_distribution(
            df=deptTable,
            column="Department",
            target_values=[department],
            value_colors=gaw.get_random_values(gaw.get_non_red_colors()),
            user_directory=user_directory,
            csv=csv,
        )
        graph_grade_distribution(
            df=mjrTable,
            column="Major",
            target_values=[major],
            value_colors=gaw.get_random_values(gaw.get_non_red_colors()),
            user_directory=user_directory,
            csv=csv,
        )

    print(tabulate(deptTable, headers="keys", tablefmt="pretty"))
    print(tabulate(mjrTable, headers="keys", tablefmt="pretty"))


def DepartmentAnalysis(
    df,
    user_directory,
    target_values=None,
    min_enrollments=None,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    generate_grade_dist=False,
):
    deptTable = pandas_df_agg(df, "Department")
    deptTable = drop_courses_by_threshold(
        deptTable, "Enrollments", min_enrollments, max_enrollments
    )
    deptTable = drop_courses_by_threshold(
        deptTable, "Sections", min_sections, max_sections
    )

    target_values = list(target_values)

    deptTable = deptTable[deptTable["Department"].isin(target_values)]

    if dic.department_analysis_options["Department vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Department vs GPA",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="GPA",
            plot_type="bar",
            color="teal",
            x_plot="Department",
            y_plot="GPA",
            df=deptTable,
        )
        plotter.plot()

    if dic.department_analysis_options["Department vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Department vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="Enrollment",
            plot_type="scatter",
            color="teal",
            x_plot="Department",
            y_plot="Enrollments",
            df=deptTable,
        )
        plotter.plot()

    if csv:
        save_path = os.path.join(user_directory, "deptTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        deptTable.to_csv(save_path, encoding="utf-8-sig")

    if generate_grade_dist:
        graph_grade_distribution(
            df=deptTable,
            column="Department",
            target_values=target_values,
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )

    dic.reset_all_false()


def InstructorAnalysis(
    df,
    user_directory,
    min_enrollments=None,
    max_enrollments=None,
    target_values=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    generate_grade_dist=False,
):
    if check_list_is_subset(target_values, uniqueDept):
        df = df[df["Department"].isin(list(target_values))]

    if check_list_is_subset(target_values, uniqueCrs):
        df = df[df["CourseTitle"].isin(list(target_values))]

    if check_list_is_subset(target_values, uniqueInst):
        df = df[df["FacultyID"].isin(list(target_values))]

    instTable = pandas_df_agg(df, "FacultyID")
    instTable = drop_courses_by_threshold(
        instTable, "Enrollments", min_enrollments, max_enrollments
    )
    instTable = drop_courses_by_threshold(
        instTable, "Sections", min_sections, max_sections
    )
    instTable = instTable.drop_duplicates(subset=["FacultyID"])
    target_values = instTable["FacultyID"].tolist()

    if csv:
        save_path = os.path.join(user_directory, "instTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        instTable.to_csv(save_path, encoding="utf-8-sig")

    if generate_grade_dist:
        graph_grade_distribution(
            df=instTable,
            column="FacultyID",
            target_values=target_values,
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )

    if dic.instructor_analysis_options["Instructor vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Instructor vs GPA",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            y_plot="GPA",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Instructor vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            y_plot="Enrollments",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Course(By Instructor) vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course(By Instructor) vs GPA",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseTitle",
            y_plot="GPA",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Section #"]:
        plotter = gaw.tkMatplot(
            title="Instructor vs Section #",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            y_plot="Sections",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Course #"]:
        plotter = gaw.tkMatplot(
            title="Instructor vs Course #",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            y_plot="Courses",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Instructor vs Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            y_plot="stddev",
            df=instTable,
        )
        plotter.plot()

    if dic.instructor_analysis_options["GPA vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="GPA vs Enrollment for Instructors",
            window_width=800,
            window_height=700,
            x_label="Average GPA",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="GPA",
            y_plot="Enrollments",
            df=instTable,
        )
        plotter.plot()

        dic.reset_all_false()


def MajorAnalysis(
    df,
    user_directory,
    min_enrollments=None,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    target_values=None,
    generate_grade_dist=False,
):
    mjrTable = pandas_df_agg(df, "Major")
    mjrTable = drop_courses_by_threshold(
        mjrTable, "Enrollments", min_enrollments, max_enrollments
    )
    mjrTable = drop_courses_by_threshold(
        mjrTable, "Sections", min_sections, max_sections
    )

    mjrTable.loc[0, "Major"] = "Undefined"

    mjrTable = mjrTable[mjrTable["Major"].isin(target_values)]

    if dic.major_analysis_options["Major vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Major vs GPA",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="Major",
            y_plot="GPA",
            df=mjrTable,
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Major vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Enrollment",
            plot_type="scatter",
            color="teal",
            x_plot="Major",
            y_plot="Enrollments",
            df=mjrTable,
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Section #"]:
        plotter = gaw.tkMatplot(
            title="Major vs Section #",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="Major",
            y_plot="Sections",
            df=mjrTable,
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Course #"]:
        plotter = gaw.tkMatplot(
            title="Major vs Course #",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="Major",
            y_plot="Courses",
            df=mjrTable,
        )
        plotter.plot()

    if dic.major_analysis_options["Standard Deviation vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Standard Deviation vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Standard Deviation",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="stddev",
            y_plot="Enrollments",
            df=mjrTable,
        )
        plotter.plot()

    if generate_grade_dist:
        graph_grade_distribution(
            df=mjrTable,
            column="Major",
            target_values=target_values,
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )

    if csv:
        save_path = os.path.join(user_directory, "majorTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        mjrTable.to_csv(save_path, encoding="utf-8-sig")

    dic.reset_all_false()



def pandas_df_agg(df, index=["Major"]):
    # Ensure index is a list
    if isinstance(index, str):
        index = [index]

    df_enrollments = (
        df.groupby(index)["SID"].nunique().reset_index(name="Enrollments")
    )

    df_agg = (
        df.groupby(index)
        .agg(
            Sections=("UniqueCourseID", "nunique"),
            Courses=("CourseTitle", "nunique"),
            GPA=("FinNumericGrade", "mean"),
            # GPAW=('FinNumericGrade', lambda x: np.average(x, weights=df.loc[x.index, 'CredHrs'])),
            stddev=("FinNumericGrade", "std"),
            kurtosis=("FinNumericGrade", lambda x: x.kurt()),
            skewness=("FinNumericGrade", lambda x: x.skew()),
        )
        .reset_index()
    )

    df_grade = grade_distribution_df(df, index)

    df_final = pd.merge(df_enrollments, df_agg, on=index)
    df_final = pd.merge(df_final, df_grade, on=index)

    float_cols = df_final.select_dtypes(include="float").columns

    df_final[float_cols] = df_final[float_cols].round(3)

    return df_final


def section_analysis(
    df,
    user_directory,
    target_courses,
    csv=False,
    min_enrollments=None,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    generate_grade_dist=False,
):
    target_courses = list(target_courses)
    # sectionTable = gpa_by_section(df, target_courses)
    sectionTable = pandas_df_agg(df, "UniqueCourseID")
    sectionTable = pd.merge(
        sectionTable,
        df[["UniqueCourseID", "CourseTitle"]],
        on="UniqueCourseID",
        how="left",
    )

    sectionTable = sectionTable.drop_duplicates(subset=["UniqueCourseID"])
    sectionTable = sectionTable[sectionTable["CourseTitle"].isin(target_courses)]
    sectionTable = drop_courses_by_threshold(
        sectionTable, "ClassSize", min_enrollments, max_enrollments
    )
    sectionTable = drop_courses_by_threshold(
        sectionTable, "semyear", min_sections, max_sections
    )

    sectionTable = sectionTable.drop("Sections", axis=1)
    sectionTable = sectionTable.drop("Courses", axis=1)

    if dic.section_analysis_options["Section vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Section vs GPA",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="GPA",
            plot_type="line",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="UniqueCourseID",
            y_plot="GPA",
            df=sectionTable,
        )
        plotter.plot()

    if dic.section_analysis_options["Section vs Class Size"]:
        plotter = gaw.tkMatplot(
            title="Section vs Class Size",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="UniqueCourseID",
            y_plot="Enrollments",
            df=sectionTable,
        )
        plotter.plot()

    if dic.section_analysis_options["GPA vs Class Size"]:
        plotter = gaw.tkMatplot(
            title="GPA vs ClassSize per section",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Class Size",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="GPA",
            y_plot="Enrollments",
            df=sectionTable,
        )
        plotter.plot()

    elif dic.section_analysis_options["Section vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Section vs Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="UniqueCourseID",
            y_plot="stddev",
            df=sectionTable,
        )
        plotter.plot()

    elif dic.section_analysis_options["Enrollment vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Enrollment vs Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Enrollment",
            y_label="Standard Deviation",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="Enrollments",
            y_plot="stddev",
            df=sectionTable,
        )
        plotter.plot()

    if csv:
        save_path = os.path.join(user_directory, "sectionTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        sectionTable.to_csv(save_path, encoding="utf-8-sig")

    if generate_grade_dist:
        graph_grade_distribution(
            df=sectionTable,
            column="UniqueCourseID",
            target_values=target_courses,
            value_colors=gaw.get_random_values(gaw.get_non_red_colors()),
            user_directory=user_directory,
            csv=csv,
        )

    for key in dic.section_analysis_options.keys():
        dic.section_analysis_options[key] = False


def CourseAnalysis(
    df,
    user_directory,
    min_enrollments=None,
    target_values=None,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    generate_grade_dist=False,
):

    if check_list_is_subset(target_values, uniqueDept):
        df = df[df["Department"].isin(list(target_values))]

    if check_list_is_subset(target_values, uniqueCrs):
        df = df[df["CourseTitle"].isin(list(target_values))]

    crsTable = pandas_df_agg(df, "CourseTitle")
    crsTable = drop_courses_by_threshold(
        crsTable, "Enrollments", min_enrollments, max_enrollments
    )
    crsTable = drop_courses_by_threshold(
        crsTable, "Sections", min_sections, max_sections
    )

    target_values = crsTable["CourseTitle"].tolist()

    if dic.course_analysis_options["Course vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course vs GPA",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseTitle",
            y_plot="GPA",
            df=crsTable,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Course vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Enrollments",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseTitle",
            y_plot="Enrollments",
            df=crsTable,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Section #"]:
        plotter = gaw.tkMatplot(
            title="GPA vs Section",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseTitle",
            y_plot="Sections",
            df=crsTable,
        )
        plotter.plot()

    elif dic.course_analysis_options["Enrollment vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Enrollment vs GPA",
            window_width=800,
            window_height=700,
            x_label="Enrollment",
            y_label="GPA",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="Enrollments",
            y_plot="GPA",
            df=crsTable,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Course vs Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseTitle",
            y_plot="stddev",
            df=crsTable,
        )
        plotter.plot()

    elif dic.course_analysis_options["GPA vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="GPA vs Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Standard Deviation",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="GPA",
            y_plot="stddev",
            df=crsTable,
        )
        plotter.plot()

    if csv:
        save_path = os.path.join(user_directory, "crsTableTrunc.csv")
        crsTable.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    if generate_grade_dist:
        graph_grade_distribution(
            df=crsTable,
            target_values=target_values,
            column="CourseTitle",
            value_colors=gaw.get_random_values(gaw.get_non_red_colors()),
            user_directory=user_directory,
            csv=csv,
        )

        dic.reset_all_false()



## Should we use enrollment threshold for class size?


def student_level_analysis(
    df,
    user_directory,
    csv=False,
    min_enrollments=None,
    max_enrollments=None,
    generate_grade_dist=False,
):
    df = drop_courses_by_threshold(df, "ClassSize", min_enrollments, max_enrollments)

    df["StudentLevel"] = df["StudentLevel"].apply(
        lambda x: (
            "Freshman" if x in ["Continuing Freshman", "First-Time Freshman"] else x
        )
    )


    df['StudentLevel'] = df['StudentLevel'].apply(lambda x: "Unknown" if pd.isna(x) or x == "" else x)


    df_agg = pandas_df_agg(df, "StudentLevel")

    if dic.studentlevel_analysis_options["Student Level vs Enrollments"]:
        plotter = gaw.tkMatplot(
            title="Student Level vs Enrollment",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="Enrollment",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="StudentLevel",
            y_plot="Enrollments",
            df=df_agg,
        )
        plotter.plot()

    if dic.studentlevel_analysis_options["Student Level vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Student Level vs GPA",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="StudentLevel",
            y_plot="GPA",
            df=df_agg,
        )
        plotter.plot()

    if dic.studentlevel_analysis_options["Student Level vs Courses"]:
        plotter = gaw.tkMatplot(
            title="Student Level vs Courses",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="StudentLevel",
            y_plot="Courses",
            df=df_agg,
        )
        plotter.plot()

    if generate_grade_dist:
        graph_grade_distribution(
            df=df_agg,
            column="StudentLevel",
            target_values=df_agg["StudentLevel"].unique(),
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )


    if csv:
        save_path = os.path.join(user_directory, "student_level_analysis.csv")
        df.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    dic.reset_all_false()



def sort_courses(course):
    if course >= 1000 and course < 2000:
        return "1000"
    elif course >= 2000 and course < 3000:
        return "2000"
    elif course >= 3000 and course < 4000:
        return "3000"
    elif course >= 4000:
        return "4000"
    elif course <= 1000:
        return "Beginner"


def course_level_analysis(
    df,
    user_directory,
    min_enrollments=None,
    max_enrollments=None,
    csv=False,
    generate_grade_dist=False,
):
    df = drop_courses_by_threshold(df, "ClassSize", min_enrollments, max_enrollments)

    df["CourseLevel"] = df["CourseNum"].apply(sort_courses)

    df_agg = pandas_df_agg(df, "CourseLevel")

    if dic.courselevel_analysis_options["Course Level vs Course #"]:
        plotter = gaw.tkMatplot(
            title="Course Level vs Num. Courses",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="Courses #",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseLevel",
            y_plot="Courses",
            df=df_agg,
        )
        plotter.plot()

    if dic.courselevel_analysis_options["Course Level vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course Level vs Avg GPA",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseLevel",
            y_plot="GPA",
            df=df_agg,
        )
        plotter.plot()


    if dic.courselevel_analysis_options["Course Level vs Enrollments"]:
        plotter = gaw.tkMatplot(
            title="Course Level vs Enrollments",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="Enrollments",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="CourseLevel",
            y_plot="Enrollments",
            df=df_agg,
        )
        plotter.plot()

    if generate_grade_dist:
        graph_grade_distribution(
            df=df_agg,
            column="CourseLevel",
            target_values=df_agg["CourseLevel"].unique(),
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )

    if csv:
        save_path = os.path.join(user_directory, "course_level_analysis.csv")
        df_agg.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    dic.reset_all_false()


def studentCourse_level_analysis(
    df,
    user_directory,
    min_enrollments=None,
    max_enrollments=None,
    csv=False,
):
    df = drop_courses_by_threshold(df, "ClassSize", min_enrollments, max_enrollments)

    df["StudentLevel"] = df["StudentLevel"].apply(
        lambda x: (
            "Freshman" if x in ["Continuing Freshman", "First-Time Freshman"] else x
        )
    )

    df["CourseLevel"] = df["CourseNum"].apply(sort_courses)

    df_agg = pandas_df_agg(df, ["StudentLevel", "CourseLevel"])

    if csv:
        save_path = os.path.join(user_directory, "student_course_level_analysis.csv")
        df_agg.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    if dic.studentcourse_analysis_options["Student-Course vs GPA"]:
        pivot = df_agg.pivot_table(index='StudentLevel', columns='CourseLevel', values='GPA', fill_value=0)
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('GPA Heatmap: Student Level vs Course Level')
        plt.xlabel('Course Level')
        plt.ylabel('Student Level')
        plt.show()

    if dic.studentcourse_analysis_options["Student-Course vs Enrollment"]:
        pivot = df_agg.pivot_table(index='StudentLevel', columns='CourseLevel', values='Enrollments', fill_value=0)
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Enrollment Heatmap: Student Level vs Enrollment')
        plt.xlabel('Course Level')
        plt.ylabel('Student Level')
        plt.show()

    dic.reset_all_false()





def normalize_rows_by_grade_frequency(df, column, grade_columns):

    for value in df[column].unique():
        department_grades = df.loc[df[column] == value, grade_columns]
        total_grades = department_grades.sum(axis=1)
        df.loc[df[column] == value, grade_columns] = department_grades.div(
            total_grades, axis=0
        )

    return df


def graph_grade_distribution(
    df,
    column,
    user_directory,
    csv=False,
    target_values=None,
    value_colors=None,
    cutoff_enrollment=100,
):
    if target_values is None:
        target_values = []
    if value_colors is None:
        value_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-"]
    value_colors = value_colors[: len(target_values)]

    df = df[df[f"{column}"].isin(target_values)]
    df = normalize_rows_by_grade_frequency(df, column, grades)

    if csv:
        save_path = os.path.join(user_directory, f"grade_distribution_{column}.csv")
        df.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    fig = plt.figure(figsize=(20, 8.5))
    ax = fig.add_subplot(111)

    scatter_plots = {}  # Dictionary to store scatter plot references and original states

    for i, value in enumerate(target_values):
        value_df = df[df[f"{column}"] == value]
        grade_counts = [
            round(
                value_df[grade].iloc[0], 4
            )
            if (not value_df.empty and grade in value_df.columns)
            else 0
            for grade in grades
        ]

        scatter = ax.scatter(
            grades,
            grade_counts,
            label=f"{value}",
            color=value_colors[i % len(value_colors)],
            edgecolors="black",
            linewidths=1,
            s=100  # Initial size of the markers
        )
        ax.plot(
            grades,
            grade_counts,
            color='black',
            linewidth=3,
            linestyle="-",
        )
        ax.plot(
            grades,
            grade_counts,
            color=value_colors[i % len(value_colors)],
            linewidth=1,
            linestyle="-",
        )
        # Store the scatter plot and its original facecolors and sizes
        scatter_plots[value] = (scatter, {'facecolors': scatter.get_facecolor(), 'sizes': scatter.get_sizes()})

    ax.legend(fontsize='small', loc='best')
    ax.set_xlabel("Letter Grades", fontsize=12)
    ax.set_ylabel("Number of Each Grade (normalized)", fontsize=10)
    ax.set_title("Frequency of Letter Grades", fontsize=14)
    ax.grid(True)

    root, canvas = create_figure_window(
        fig, title="Grade Distribution", geometry="1000x700"
    )

    # Adjusting the Treeview to have an additional "Category" column
    tree = ttk.Treeview(root)
    tree["columns"] = ["Category"] + grades
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Category", anchor=tk.CENTER, width=120)
    tree.heading("Category", text=column, anchor=tk.CENTER)

    for grade in grades:
        tree.column(grade, anchor=tk.CENTER, width=80)
        tree.heading(grade, text=grade, anchor=tk.CENTER)

    for value in target_values:
        value_df = df[df[f"{column}"] == value]
        row = [round(value_df[grade].iloc[0], 4) if (not value_df.empty and grade in value_df.columns and not value_df[grade].empty) else 0 for grade in grades]
        tree.insert("", tk.END, values=(value, *row))

    tree.grid(row=2, column=0, sticky="nsew")

    def on_tree_selection_change(event):
        selected_items = tree.selection()
        if selected_items:
            item = tree.item(selected_items[0])["values"][0]
            highlight_plot_points(item)

    def clear_highlight():
        for scatter, original in scatter_plots.values():
            scatter.set_facecolors(original['facecolors'])
            scatter.set_sizes(original['sizes'])

    def highlight_plot_points(category):
        clear_highlight()
        scatter, original = scatter_plots.get(category, (None, None))
        if scatter:
            scatter.set_facecolors("red")
            scatter.set_sizes([size * 2 for size in original['sizes']])
        canvas.draw_idle()

    tree.bind("<<TreeviewSelect>>", on_tree_selection_change)

    canvas.draw()

def create_figure_window(fig, window=None, title="Figure Window", geometry="1000x700"):
    if window is None:
        root = tk.Tk()
        root.title(title)
        root.geometry(geometry)
    else:
        root = window

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")

    toolbar_frame = ttk.Frame(root)
    toolbar_frame.grid(row=1, column=0, sticky="ew")
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    button_quit = ttk.Button(root, text="Quit", command=root.destroy)
    button_quit.grid(row=3, column=0, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    canvas.draw()

    return root, canvas


def grade_distribution_df(df, index_col):
    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
    df_filtered = df[df["FinLetterGrade"].isin(grades)]

    df_pivot = df_filtered.pivot_table(
        index=index_col, columns="FinLetterGrade", aggfunc="size", fill_value=0
    )
    df_pivot = df_pivot.reset_index()

    df_pivot.columns.name = None
    for grade in grades:
        if grade not in df_pivot.columns:
            df_pivot[grade] = 0

    # This step ensures that the grade columns are in the expected order
    grade_columns = [grade for grade in grades if grade in df_pivot.columns]
    other_columns = [col for col in df_pivot.columns if col not in grade_columns]
    ordered_columns = other_columns + grade_columns
    df_pivot = df_pivot[ordered_columns]

    return df_pivot


def piechart_df_columns(df, col_values, col_labels):
    df = drop_courses_by_threshold(df, "TrueClassSize", 1000)

    sizes = df[col_values].tolist()
    labels = df[col_labels].tolist()

    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(sizes, startangle=90, wedgeprops=dict(width=0.5))

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(
            labels[i],
            xy=(x, y),
            xytext=(1.35 * np.sign(x), 1.4 * y),
            horizontalalignment=horizontalalignment,
            **kw,
        )

    _, canvas = create_figure_window(fig, title="Pie Chart", geometry="1000x700")

    return _, canvas


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
        dataframe[f"{normalization_type}Normalized{column}"] = (
            scaled_data.squeeze()
        )  # Use squeeze to ensure correct dimensionality
    else:
        print(f"Normalization type '{normalization_type}' is not supported.")
