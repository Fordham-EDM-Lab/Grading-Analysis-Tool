"""
This is an Educational Data Mining tool. It reads data from an university and makes analysis of its contents. Created by Luisa Rosa (lrosa6@fordham.edu), with Dr.Daniel Leeds, Dr.Gary Weiss, and Ashley Saliasi at Fordham University.

Library free for use, required citation using ... in any resulting publications.
Library free for redistribution provided you retain the author attributions above.

The following packages are required for installation before use: numpy, pandas, csv, matplotlib
"""

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned-data-6-17-22.csv')

def main():
    #TODO: initiate the tool 
    print("Welcome to the Grading Data Mining Tool!")
    print("Please type of the options below so our tool knows what to do.")

    #TODO: gets user input to call specific class
    request = input("AllCourseMean --> compute the GPA of all courses in the univeristy, and the standard deviation.")
    if request == "AllCourseMean":
        dataCleanup(df)
        UniversityCoursesMean(df)



#TODO: separate the research code into classes that can be called to perform the specific section of the code:
#data cleanup class
def dataCleanup(df):
    #Data Cleaning - splitting sem/year, dropping Administrative depts, and creating a new CRN
    df.replace(" ", np.nan, inplace=True)
    df['finGradN'] = df['finGradN'].astype('float')

    df.drop(df[df['ProgCode'] == 'Administrative CBA'].index,  inplace = True)
    df.drop(df[df['ProgCode'] == 'Administrative FCRH'].index, inplace = True)

    df[['sem', 'year']] = df['term'].str.split(' ', 1, expand = True)

    df['year'] = df['year'].astype('int')

    df.loc[df['sem'] == 'Summer', 'sem'] = 0
    df.loc[df['sem'] == 'Spring', 'sem'] = 1
    df.loc[df['sem'] == 'Fall', 'sem'] = 2
    df['sem'] = df['sem'].astype('int')

    df.rename(columns={'CRN':'oldCRN'}, inplace = True)
        
    df['CRN']= df['oldCRN'] + df['sem'] + df['year']

#average & std grades of all courses
def UniversityCoursesMean(df):
    # Compute average grade over all courses (weighted)
    def avgWeighted(df, value, weight):
        return (df[weight] * df[value]).sum() / df[weight].sum()
    stdAllCourse = df['finGradN'].std()

    print("This is the the GPA of all courses in the university: " + avgWeighted(df, 'finGradN', 'credHrs'))
    print("This is the Standard Deviation of all courses GPA: " + stdAllCourse)
 

    #generate table of student grade distribution of all courses 
    #generate table of student grade distribution of all courses
    #extract a list of all unique departments, majors, instructors, courses, CRNs, and students
    #compute the number of enrollments for each and create a table |departments, # of enrollments|
    #create a table |major, unique students|
    #creates a thorough course table; information: Course, Enrollments, Sections, Faculty, Students, weighted GPA and std deviation.
    #creates a thorough major table; information: Major, Enrollments (all course enrollments of students in that major), Sections, Courses, and weighted GPA.
    #creates a thorough department table; information: Department, Enrollments (all students enrolled in courses within that department), Sections, Courses, Instructors, and weighted GPA.
    #creates a thorough instructor table; information: Instructor, Enrollments (number of students taught), Sections taught, Courses taught, Courses title, terms taught, years of teaching in the institution, and weighted GPA.    

    #TODO: separate the research code into classes that can be called to perform the specific section using user input:
        #TODO: average & std grades of all students taking courses that belong to specific department
        #TODO: average & std grades of all courses students with that specific major take
        #TODO: average & std of all courses students that have a major in that specific department take
        #TODO: average & std grade of all courses in the specific major that students with that specific major take
        #TODO: average GPA, std, lowwest and highest grades of a specific faculty.
        #TODO: generate table of student grade distribution of specific department 
        #TODO: generate table of student grade distribution of specific major
        #TODO: generate table of student grade distribution of specific instructor
        
    #TODO: separate the research code into classes that can be called to create the specific illustrations of the data:
        #department grades bar chart (y=gpa, x=department) for departments with enrollments > 600
        #department size bar chart (y=enrollments, x=department) for departments with enrollments > 600
        #bar chart that shows number of enrollments and department average grades simultaneously. 
        #instructor Grade Distribution (histogram) -- frequency of grades
        #instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections 
        #total number of students in a department vs. grades in that department scatter plot, for departments with enrollments > 600
        #gpa vs major size (number of enrollments) scatter plot
        #gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments
        #major vs enrollments bar chart, for majors with > 10,000 enrollments
        #distribution of grades bar chart for courses with > 70 sections 
        #instructor Enrollment Distribution histogram
        #instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200 
    
    #TODO: add mapping of courses x majors to tool
    #TODO: Course Level Report (courseLevel.csv)