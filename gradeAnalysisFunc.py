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

from requests.packages import target

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
# get useful list of all unique departments, majors, instructors, courses, UniqueCourseID, and students
def get_unique_dept(df):
    return df["Department"].unique()

def get_unique_major(df):
    return df["Major"].unique()

def get_unique_inst(df):
    return df["FacultyID"].unique()

def get_unique_crs(df):
    return df["CourseTitle"].unique()

def get_unique_crscode(df):
    return df["CourseCode"].unique()

def get_unique_crsid(df):
    return df["UniqueCourseID"].unique()

def get_unique_stud(df):
    return df["SID"].unique()


# returns filtered dataframe. Each condition should be passed as column name = LIST of targets
# e.g. "filter(df, crsTitle = ['PHYSICS I LAB'], facultyID = ['F18125', 'F97128'])" returns df with 84 rows
def filter(df, **kwargs):
    for key in kwargs.keys():
        df = df[(df[key]).isin(kwargs.get(key))]
    return df


# All this is done to make a csv file with all the unique entries appearing in the given dataset. It is
# not used and is only there for refrence purposes.


def save_unique_entries(df, user_directory):
    uniquevalue = get_unique_dept(df)

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
            len(get_unique_major(df)),
            len(get_unique_inst(df)),
            len(get_unique_crs(df)),
            len(get_unique_crsid(df)),
            len(get_unique_stud(df)),
        )

        for i in range(max_length):
            row = [
                uniquevalue[i] if i < len(uniquevalue) else "",
                get_unique_major(df)[i] if i < len(get_unique_major(df)) else "",
                get_unique_inst(df)[i] if i < len(get_unique_inst(df)) else "",
                get_unique_crs(df)[i] if i < len(get_unique_crs(df)) else "",
                get_unique_crsid(df)[i] if i < len(get_unique_crsid(df)) else "",
                get_unique_stud(df)[i] if i < len(get_unique_stud(df)) else "",
            ]
            writer.writerow(row)

        print("\n\nFile Created:", f" {save_path}\n\n")


def drop_courses_by_threshold(df, column, min_threshold=None, max_threshold=None):
    if min_threshold is not None:
        df = df[df[column] >= min_threshold]
    if max_threshold is not None:
        df = df[df[column] <= max_threshold]
    return df



# average & std grades of all students taking courses in specific department


def check_list_is_subset(target_list, check_list):
    return all(item in check_list for item in target_list)


def DepartmentAnalysis(
    df,
    user_directory,
    target_values=None,
    min_enrollments=100,
    max_enrollments=None,
    min_sections=None,
    max_sections=None,
    csv=False,
    generate_grade_dist=False,
):

    col = find_column_by_value(df, list(target_values.keys())[1])

    deptTable = pandas_df_agg(df, "Department")

    deptTable = drop_courses_by_threshold(
        deptTable, "Enrollments", min_enrollments, max_enrollments
    )
    deptTable = drop_courses_by_threshold(
        deptTable, "Sections", min_sections, max_sections
    )

    if csv:
        save_path = os.path.join(user_directory, "deptTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        deptTable.to_csv(save_path, encoding="utf-8-sig")

    deptTable['color'] = deptTable[col].map(target_values)



    if dic.department_analysis_options["Department vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Average Department GPA",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="GPA",
            plot_type="bar",
            colors=target_values,
            color='black',
            x_plot="Department",
            y_plot="GPA",
            df=deptTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.department_analysis_options["Department vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Average Department Enrollment",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="Enrollment",
            plot_type="scatter",
            colors=target_values,
            color="teal",
            x_plot="Department",
            y_plot="Enrollments",
            df=deptTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.department_analysis_options["Department vs Section #"]:
        plotter = gaw.tkMatplot(
            title="# Sections offered by Department",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="Sections",
            plot_type="scatter",
            colors=target_values,
            color="teal",
            x_plot="Department",
            y_plot="Sections",
            df=deptTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.department_analysis_options["Department vs Course #"]:
        plotter = gaw.tkMatplot(
            title="# Courses offered by Department",
            window_width=800,
            window_height=700,
            x_label="Department",
            y_label="Courses",
            plot_type="bar",
            colors=target_values,
            color="teal",
            x_plot="Department",
            y_plot="Courses",
            df=deptTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.department_analysis_options["Standard Deviation vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="GPA Standard Deviation vs Department Enrollment Number",
            window_width=800,
            window_height=700,
            x_label="Standard Deviation",
            y_label="Enrollment",
            plot_type="scatter",
            colors=target_values,
            color="teal",
            x_plot="stddev",
            y_plot="Enrollments",
            df=deptTable,
        )
        plotter.plot()

    if dic.department_analysis_options["Enrollment vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Department Enrollment vs GPA",
            window_width=800,
            window_height=700,
            x_label="Enrollment",
            y_label="GPA",
            plot_type="scatter",
            colors=target_values,
            color="teal",
            x_plot="Enrollments",
            y_plot="GPA",
            df=deptTable,
        )
        plotter.plot()



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


def return_filtered_dataframe(df: pd.DataFrame, column: str, values: list) -> pd.DataFrame:
    mask = df[column].isin(values)
    return df[mask]


def find_column_by_value(df, value):
    for col in df.columns:
        if df[col].eq(value).any():
            return col
    return None

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

    col = find_column_by_value(df, list(target_values.keys())[1])
    if col != 'FacultyID':
        instTable = pandas_df_agg(df, ["FacultyID", col])
    else:
        instTable = pandas_df_agg(df, 'FacultyID')

    instTable = drop_courses_by_threshold(
        instTable, "Enrollments", min_enrollments, max_enrollments
    )
    instTable = drop_courses_by_threshold(
        instTable, "Sections", min_sections, max_sections
    )

    if col == 'FacultyID':
        instTable = instTable.drop_duplicates(subset=["FacultyID"])


    if csv:
        save_path = os.path.join(user_directory, "instTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        instTable.to_csv(save_path, encoding="utf-8-sig")

    instTable['color'] = instTable[col].map(target_values)

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
            title="Average Instructor GPA",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="FacultyID",
            y_plot="GPA",
            df=instTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="# Enrollment per Instructor",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="FacultyID",
            y_plot="Enrollments",
            df=instTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Section #"]:
        plotter = gaw.tkMatplot(
            title="# Sections taught per Instructor",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="FacultyID",
            colors=target_values,
            y_plot="Sections",
            df=instTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Course #"]:
        plotter = gaw.tkMatplot(
            title="# Courses taught per Instructor",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="FacultyID",
            y_plot="Courses",
            df=instTable,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.instructor_analysis_options["Instructor vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="GPA Standard Deviation per Instructor",
            window_width=800,
            window_height=700,
            x_label="Instructor",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="FacultyID",
            y_plot="stddev",
            df=instTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.instructor_analysis_options["Enrollment vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Instructor's Average GPA vs Total Enrollment",
            window_width=800,
            window_height=700,
            x_label="Instructor GPA",
            y_label="Enrollment #",
            plot_type="scatter",
            colors=target_values,
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

    col = find_column_by_value(df, list(target_values.keys())[1])
    mjrTable = pandas_df_agg(df, "Major")
    mjrTable = drop_courses_by_threshold(
        mjrTable, "Enrollments", min_enrollments, max_enrollments
    )
    mjrTable = drop_courses_by_threshold(
        mjrTable, "Sections", min_sections, max_sections
    )

    mjrTable['Major'].replace("", pd.NA, inplace=True)
    mjrTable.dropna(subset=['Major'], inplace=True)


    if csv:
        save_path = os.path.join(user_directory, "majorTable.csv")
        print("\n\nFile Created:", f" {save_path}\n\n")
        mjrTable.to_csv(save_path, encoding="utf-8-sig")

    mjrTable['color'] = mjrTable[col].map(target_values)

    if dic.major_analysis_options["Major vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Major's Average GPA",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="Major",
            y_plot="GPA",
            df=mjrTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="# Enrollment per Major",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Enrollment",
            plot_type="scatter",
            color="teal",
            colors=target_values,
            x_plot="Major",
            y_plot="Enrollments",
            df=mjrTable,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Section #"]:
        plotter = gaw.tkMatplot(
            title="# Sections taken by Major",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="Major",
            y_plot="Sections",
            df=mjrTable,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.major_analysis_options["Major vs Course #"]:
        plotter = gaw.tkMatplot(
            title="# Courses taken by Major",
            window_width=800,
            window_height=700,
            x_label="Major",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="Major",
            y_plot="Courses",
            df=mjrTable,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.major_analysis_options["GPA vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Major's Average GPA vs Major's Total Enrollment",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="GPA",
            y_plot="Enrollments",
            df=mjrTable,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.major_analysis_options["Standard Deviation vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="Major's GPA Standard Deviation vs Major's Total Enrollment",
            window_width=800,
            window_height=700,
            x_label="Standard Deviation",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="stddev",
            y_plot="Enrollments",
            df=mjrTable,
            output_directory=user_directory
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


    dic.reset_all_false()



def pandas_df_agg(df, index=["Major"]):
    """Sections: Unique instances of a CourseID for a given index
       Courses: Unique instances of a CourseTitle for a given index
       GPA: Average GPA for a given index
       stddev: Standard deviation of GPA for a given index
       kurtosis: Kurtosis of GPA for a given index
       skewness: Skewness of GPA for a given index
       """
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
            GPAW=('FinNumericGrade', lambda x: np.average(x, weights=df.loc[x.index, 'CredHrs']) if df.loc[x.index, 'CredHrs'].sum() != 0 else np.nan),
            stddev=("FinNumericGrade", "std"),
            kurtosis=("FinNumericGrade", lambda x: x.kurt()),
            skewness=("FinNumericGrade", lambda x: x.skew()),
            CoV=("FinNumericGrade", lambda x: ((x.std() / x.mean()) * 100) if x.mean() != 0 else np.nan), #coefficent of variation
            ModeGPA=("FinNumericGrade", lambda x: x.mode()[0] if not x.mode().empty else np.nan),

        )
        .rename(columns={'CoV': 'CoV(%)'})
        .reset_index()
    )

    df_grade = grade_distribution_df(df, index)

    df_final = pd.merge(df_enrollments, df_agg, on=index)
    df_final = pd.merge(df_final, df_grade, on=index)

    delta_gpa_ret_df = pd.DataFrame()
    delta_gpa_ret_df[index] = df_final[index]

    if not any(item in ['UniqueCourseID', 'SID'] for item in index):
        delta_gpa = df.groupby(index + ['Semester']).agg(GPA=("FinNumericGrade", "mean"), GPAW=('FinNumericGrade', lambda x: np.average(x, weights=df.loc[x.index, 'CredHrs']) if df.loc[x.index, 'CredHrs'].sum() != 0 else np.nan))
        temp_copy = delta_gpa.copy()
        delta_gpa['DELTA(GPA)'] = temp_copy.groupby(index)['GPA'].diff().fillna(0)
        delta_gpa['DELTA(GPAW)'] = temp_copy.groupby(index)['GPAW'].diff().fillna(0)
        delta_gpa_ret_df['avg_gpa_change'] = delta_gpa.groupby(index)['DELTA(GPA)'].mean().values
        delta_gpa_ret_df['avg_gpaw_change'] = delta_gpa.groupby(index)['DELTA(GPAW)'].mean().values
        df_final = pd.merge(df_final, delta_gpa_ret_df, on=index)


    float_cols = df_final.select_dtypes(include="float").columns

    df_final[float_cols] = df_final[float_cols].round(3)

    return df_final


def section_analysis(
    df: pd.DataFrame,
    user_directory,
    target_courses,
    csv=False,
    min_enrollments=None,
    max_enrollments=None,
    min_gpa=None,
    max_gpa=None,
    generate_grade_dist=False,
):

    col = find_column_by_value(df, list(target_courses.keys())[1])
    if col != 'UniqueCourseID':
        sectionTable = pandas_df_agg(df, ["UniqueCourseID", col])
    else:
        sectionTable = pandas_df_agg(df, 'UniqueCourseID')
        sectionTable = sectionTable.drop_duplicates(subset=["FacultyID"])



    sectionTable = drop_courses_by_threshold(
        sectionTable, "Enrollments", min_enrollments, max_enrollments
    )
    sectionTable = drop_courses_by_threshold(
        sectionTable, "GPA", min_gpa, max_gpa
    )

    sectionTable['UniqueCourseID'] = sectionTable['UniqueCourseID'].astype(str)

    sectionTable = pd.merge(
        sectionTable,
        df[["UniqueCourseID", "CourseTitle"]],
        on="UniqueCourseID",
        how="left",
    )
    sectionTable = pd.merge(sectionTable, df[['FacultyID',  'UniqueCourseID']], on="UniqueCourseID", how="left")


    sectionTable = sectionTable.drop_duplicates(subset=["UniqueCourseID"])

    sectionTable = drop_courses_by_threshold(
        sectionTable, "Enrollments", min_enrollments, max_enrollments
    )

    sectionTable = drop_courses_by_threshold(
        sectionTable, "GPA", min_gpa, max_gpa
    )
    sectionTable = sectionTable.drop("Sections", axis=1)
    sectionTable = sectionTable.drop("Courses", axis=1)
    sectionTable['color'] = sectionTable[col].map(target_courses)

    if dic.section_analysis_options["Section vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Individual Section's GPA",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="GPA",
            plot_type="line",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_courses,
            x_plot="UniqueCourseID",
            y_plot="GPA",
            df=sectionTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.section_analysis_options["Section vs Class Size"]:
        plotter = gaw.tkMatplot(
            title="Individual Section's Class Size",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="Enrollment",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_courses,
            x_plot="UniqueCourseID",
            y_plot="Enrollments",
            df=sectionTable,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.section_analysis_options["GPA vs Class Size"]:
        plotter = gaw.tkMatplot(
            title="GPA vs ClassSize per Individual Section",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Class Size",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_courses,
            x_plot="GPA",
            y_plot="Enrollments",
            df=sectionTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.section_analysis_options["Section vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Individual Section's GPA Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Section",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_courses,
            x_plot="UniqueCourseID",
            y_plot="stddev",
            df=sectionTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.section_analysis_options["Enrollment vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Enrollment vs GPA Standard Deviation per Individual Section",
            window_width=800,
            window_height=700,
            x_label="Enrollment",
            y_label="Standard Deviation",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_courses,
            x_plot="Enrollments",
            y_plot="stddev",
            df=sectionTable,
            output_directory=user_directory,
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

    dic.reset_all_false()


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

    col = find_column_by_value(df, list(target_values.keys())[1])

    crsTable = pandas_df_agg(df, "CourseCode")

    crsTable = pd.merge(crsTable, df[['CourseCode',  'Department']], on="CourseCode", how="left")

    crsTable = drop_courses_by_threshold(
        crsTable, "Enrollments", min_enrollments, max_enrollments
    )
    crsTable = drop_courses_by_threshold(
        crsTable, "Sections", min_sections, max_sections
    )

    if csv:
        save_path = os.path.join(user_directory, "crsTable.csv")
        crsTable.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    crsTable['color'] = crsTable[col].map(target_values)

    if dic.course_analysis_options["Course vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course Average GPA",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="CourseTitle",
            y_plot="GPA",
            df=crsTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Enrollment"]:
        plotter = gaw.tkMatplot(
            title="# Enrollment per Course",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Enrollments",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="CourseTitle",
            y_plot="Enrollments",
            df=crsTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Section #"]:
        plotter = gaw.tkMatplot(
            title="# Sections per Course",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Sections",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="CourseTitle",
            y_plot="Sections",
            df=crsTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.course_analysis_options["Enrollment vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course Enrollment vs Average GPA",
            window_width=800,
            window_height=700,
            x_label="Enrollment",
            y_label="GPA",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="Enrollments",
            y_plot="GPA",
            df=crsTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.course_analysis_options["Course vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Course GPA Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="Course",
            y_label="Standard Deviation",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="CourseTitle",
            y_plot="stddev",
            df=crsTable,
            output_directory=user_directory,
        )
        plotter.plot()

    elif dic.course_analysis_options["GPA vs Standard Deviation"]:
        plotter = gaw.tkMatplot(
            title="Average GPA vs GPA Standard Deviation",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Standard Deviation",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=target_values,
            x_plot="GPA",
            y_plot="stddev",
            df=crsTable,
        )
        plotter.plot()

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

    df = df[df['StudentLevel'].notna() & (df['StudentLevel'] != "")]

    colors = {'Freshman': 'black',
              'Sophomores': 'green',
              'Juniors': 'purple',
              'Seniors': 'orange',
              'Graduate Students': 'yellow',
              'Unclassified': 'grey'}

    df_agg = pandas_df_agg(df, "StudentLevel")

    if csv:
        save_path = os.path.join(user_directory, "student_level_analysis.csv")
        df.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    df_agg['color'] = df_agg['StudentLevel'].map(colors)

    if dic.studentlevel_analysis_options["Student Level vs Enrollments"]:
        plotter = gaw.tkMatplot(
            title="Student Academic Year Enrollment",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="Enrollment",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="StudentLevel",
            y_plot="Enrollments",
            df=df_agg,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.studentlevel_analysis_options["Student Level vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Student Academic Year Average GPA",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="StudentLevel",
            y_plot="GPA",
            df=df_agg,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.studentlevel_analysis_options["Student Level vs Courses"]:
        plotter = gaw.tkMatplot(
            title="Student Academic Year # of Courses",
            window_width=800,
            window_height=700,
            x_label="Student Level",
            y_label="Courses",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="StudentLevel",
            y_plot="Courses",
            df=df_agg,
            output_directory=user_directory
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



    colors = {'Beginner': 'black',
              '1000': 'green',
              '2000': 'purple',
              '3000': 'orange',
              '4000': 'yellow',
              }
    df_agg = pandas_df_agg(df, "CourseLevel")

    if csv:
        save_path = os.path.join(user_directory, "course_level_analysis.csv")
        df_agg.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    df_agg['color'] = df_agg['CourseLevel'].map(colors)

    if dic.courselevel_analysis_options["Course Level vs Course #"]:
        plotter = gaw.tkMatplot(
            title="Course Level Num. Courses",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="Courses #",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="CourseLevel",
            y_plot="Courses",
            df=df_agg,
            output_directory=user_directory,
        )
        plotter.plot()

    if dic.courselevel_analysis_options["Course Level vs GPA"]:
        plotter = gaw.tkMatplot(
            title="Course Level Avg GPA",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="GPA",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="CourseLevel",
            y_plot="GPA",
            df=df_agg,
            output_directory=user_directory
        )
        plotter.plot()


    if dic.courselevel_analysis_options["Course Level vs Enrollments"]:
        plotter = gaw.tkMatplot(
            title="Course Level # Enrollments",
            window_width=800,
            window_height=700,
            x_label="Course Level",
            y_label="Enrollments",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            colors=colors,
            x_plot="CourseLevel",
            y_plot="Enrollments",
            df=df_agg,
            output_directory=user_directory
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



    dic.reset_all_false()

def student_analysis(
    df,
    user_directory,
    min_enrollments=None,
    max_enrollments=None,
    csv=False,
    generate_grade_dist=False,):

    df_agg = pandas_df_agg(df, "SID")
    df_agg = drop_courses_by_threshold(df_agg, "Courses", min_enrollments, max_enrollments)
    df_agg.drop(['Enrollments'], axis=1, inplace=True)

    labels = []
    for i in range(0, 40):
        start = round(i * 0.1, 1)
        end = round((i + 1) * 0.1, 1)
        labels.append(f"{start}-{end}")

    if dic.student_analysis_options["GPA groups vs Student Count"]:
        df_agg['GPAGroups'] = pd.cut(df_agg['GPA'], bins=40, labels=labels)
        df_agg['GPAGroupCounts'] = df_agg['GPAGroups'].map(df_agg['GPAGroups'].value_counts())
        countvsgpaDF = df_agg.drop_duplicates(subset=['GPAGroups'])
        countvsgpaDF.sort_values(by='GPAGroups', inplace=True)
        countvsgpaDF['GPAGroups'] = countvsgpaDF['GPAGroups'].astype(str)
        plotter = gaw.tkMatplot(
            title="GPA groups vs Student Count",
            window_width=800,
            window_height=700,
            x_label="GPA Group",
            y_label="Student Count",
            plot_type="bar",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="GPAGroups",
            y_plot="GPAGroupCounts",
            df=countvsgpaDF,
            output_directory=user_directory
        )
        plotter.plot()

    if dic.student_analysis_options["Student Course # Taken vs Student Average GPA"]:
        plotter = gaw.tkMatplot(
            title="Student Course # Taken vs Student Average GPA",
            window_width=800,
            window_height=700,
            x_label="GPA",
            y_label="Courses Taken",
            plot_type="scatter",
            color=gaw.get_random_values(gaw.get_non_red_colors())[0],
            x_plot="GPA",
            y_plot="Courses",
            df=df_agg,
            output_directory=user_directory
        )
        plotter.plot()


    if csv:
        save_path = os.path.join(user_directory, "SID_student_analysis.csv")
        df_agg.to_csv(save_path, encoding="utf-8-sig")
        print("\n\nFile Created:", f" {save_path}\n\n")

    if generate_grade_dist:
        graph_grade_distribution(
            df=df_agg,
            column="SID",
            target_values=df_agg["SID"].unique(),
            value_colors=gaw.get_non_red_colors(),
            user_directory=user_directory,
            csv=csv,
        )

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
    normalize_dataframe_column(df_agg, "Enrollments", 'robust')

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
        pivot = df_agg.pivot_table(index='StudentLevel', columns='CourseLevel', values=f'robustNormalizedEnrollments', fill_value=0)
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

    target_values = df[column].unique()

    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
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
            s=100
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
