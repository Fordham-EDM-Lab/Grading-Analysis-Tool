"""
This is an Educational Data Mining tool. It reads data from an university and makes analysis of its contents. Created by Luisa Rosa (lrosa6@fordham.edu), with Dr.Daniel Leeds, Dr.Gary Weiss, and Ashley Saliasi at Fordham University.

Library free for use, required citation using ... in any resulting publications.
Library free for redistribution provided you retain the author attributions above.

The following packages are required for installation before use: numpy, pandas, csv, matplotlib
"""

from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

# save the data file as df
df = pd.read_csv('grading-data-6-17-22.csv')

# TODO: separate the research code into classes that can be called to perform the specific section of the code:


def dataCleanup(df):
    # Data Cleaning - splitting sem/year, dropping Administrative depts, and creating a new CRN
    df.replace(" ", np.nan, inplace=True)
    df['finGradN'] = df['finGradN'].astype('float')

    df.drop(df[df['ProgCode'] == 'Administrative CBA'].index,  inplace=True)
    df.drop(df[df['ProgCode'] == 'Administrative FCRH'].index, inplace=True)

    df[['sem', 'year']] = df['term'].str.split(' ', 1, expand=True)

    df['year'] = df['year'].astype('int')

    df.loc[df['sem'] == 'Summer', 'sem'] = 0
    df.loc[df['sem'] == 'Spring', 'sem'] = 1
    df.loc[df['sem'] == 'Fall', 'sem'] = 2
    df['sem'] = df['sem'].astype('int')

    df.rename(columns={'CRN': 'oldCRN'}, inplace=True)

    df['CRN'] = df['oldCRN'] + df['sem'] + df['year']


# perform necessary data cleanup
df = dataCleanup(df)

# Compute weighted average


def avgWeighted(df, value, weight):
    return (df[weight] * df[value]).sum() / df[weight].sum()

# average & std grades of all courses


def UniversityCoursesMean(df):
    print("This is the the GPA of all courses in the university: " +
          avgWeighted(df, 'finGradN', 'credHrs'))
    print("This is the Standard Deviation of all courses GPA: " +
          df['finGradN'].std())

# average & std grades of all students taking courses in specific department


def DepartmentCoursesMean(df, dept):
    deptMean = df.loc[df['ProgCode'] == dept, 'finGradN'].mean()
    stdDept = df.loc[df['ProgCode'] == dept, 'finGradN'].std()
    print("This is" + dept + "department courses mean grade: " + deptMean)
    print("This is" + dept + "department courses grade standard deviation: " + stdDept)

# average & std dev of grades of all students of a specific major (all courses in major department or not)


def MajorDegreeMean(df, major):
    majorMean = df.loc[df['major'] == major, 'finGradN'].mean()
    stdMajor = df.loc[df['major'] == major, 'finGradN'].std()
    print("This is" + major + "majors mean grade: " + majorMean)
    print("This is" + major + "majors grade standard deviation: " + stdMajor)

# average & std dev of grades of all courses in the specific major's department that students with that specific major take


def MajorDeptMean(df, major, dept):
    DMajorMean = df.loc[(df['major'] == major) & (
        df['ProgCode'] == dept), 'finGradN'].mean()
    stdDMajor = df.loc[(df['major'] == major) & (
        df['ProgCode'] == dept), 'finGradN'].std()
    print("This is" + major +
          "majors mean grade in its department courses: " + DMajorMean)
    print("This is" + major +
          "majors grade standard deviation in its department courses: " + stdDMajor)

# average GPA, std dev, lowest and highest grades of a specific faculty.


def FacultyAnalysis(df, fac):
    FacMean = df.loc[df['facultyID'] == fac, 'finGradN'].mean()
    stdFac = df.loc[df['facultyID'] == fac, 'finGradN'].std()
    facLow = df.loc[df['facultyID'] == fac, 'finGradN'].min()
    facHigh = df.loc[df['facultyID'] == fac, 'finGradN'].max()
    print("This is" + fac + "instructor's GPA (" + FacMean + "), student's std. dev. grades (" +
          stdFac + "), and his lowest and highest grades assigned ("+facLow+", "+facHigh+")")


# MAIN:
# initialize tool
print("######################################################")
print("Welcome to Fordham's EDM Lab Grading Data Mining Tool!")
print("######################################################")

loop = True
while loop == True:
    print("Please type of the options below so our tool knows what to do.")
    print("type 'help' to see possible functions")
    # gets user input to call specific class
    request = input

    if request == "help":
        print(
            "AllCourseMean --> compute the GPA of all courses in the univeristy, and the grades standard deviation.\n"
            "DeptCourseMean --> compute the GPA of all courses in the department, and the grades standard deviation.\n"
            "MajorDegreeMean --> compute the GPA and standard deviation of all students that are majoring in a specific major taking any course (related or unrelated to their major).\n"
            "MajorDeptMean --> compute the GPA and standard deviation of all students that are majoring in a specific major taking any course in their major's department.\n"
            "FacultyAnalysis --> Compute the GPA over all faculty's courses, grades standard deviation, and lowest and higher grade."
        )

    if request == "AllCourseMean":
        UniversityCoursesMean(df)

    if request == "DeptCourseMean":
        # TODO: check if it is actually a valid ProgCode
        dept = input("Which department? Use a valid 'ProgCode'")
        DepartmentCoursesMean(df, dept)

    if request == "MajorDegreeMean":
        # TODO: check if it is actually a valid major
        major = input("Which major? Use a valid 'major'")
        MajorDegreeMean(df, major)

    if request == "MajorDeptMean":
        # TODO: check if it is actually a valid major
        major = input("Which major? Use a valid 'major'")
        # TODO: check if it is actually a valid ProgCode
        dept = input("From which department? Use a valid 'ProgCode'")
        MajorDeptMean(df, major, dept)

    if request == "FacultyAnalysis":
        # TODO: check if it is actually a valid facultyID
        faculty = input("Which faculty? Use a valid 'facultyID'")
        FacultyAnalysis(df, faculty)

    rep = input("Do you want to perform any other analysis? (yes/no)")
    if rep == 'no':
        loop = False

    # generate table of student grade distribution of all courses
    # generate table of student grade distribution of all courses
    # extract a list of all unique departments, majors, instructors, courses, CRNs, and students
    # compute the number of enrollments for each and create a table |departments, # of enrollments|
    # create a table |major, unique students|
    # creates a thorough course table; information: Course, Enrollments, Sections, Faculty, Students, weighted GPA and std deviation.
    # creates a thorough major table; information: Major, Enrollments (all course enrollments of students in that major), Sections, Courses, and weighted GPA.
    # creates a thorough department table; information: Department, Enrollments (all students enrolled in courses within that department), Sections, Courses, Instructors, and weighted GPA.
    # creates a thorough instructor table; information: Instructor, Enrollments (number of students taught), Sections taught, Courses taught, Courses title, terms taught, years of teaching in the institution, and weighted GPA.

    # TODO: separate the research code into classes that can be called to create the specific illustrations of the data:
        # department grades bar chart (y=gpa, x=department) for departments with enrollments > 600
        # department size bar chart (y=enrollments, x=department) for departments with enrollments > 600
        # bar chart that shows number of enrollments and department average grades simultaneously.
        # instructor Grade Distribution (histogram) -- frequency of grades
        # instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections
        # total number of students in a department vs. grades in that department scatter plot, for departments with enrollments > 600
        # gpa vs major size (number of enrollments) scatter plot
        # gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments
        # major vs enrollments bar chart, for majors with > 10,000 enrollments
        # distribution of grades bar chart for courses with > 70 sections
        # instructor Enrollment Distribution histogram
        # instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200

    # TODO: add mapping of courses x majors to tool
    # TODO: Course Level Report (courseLevel.csv)
