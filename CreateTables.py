#STEP 2: Creating tables from Cleaned University Data to enhance tool's running time

import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import pathlib

# save the data file as df
df = pd.read_csv('data-processed-ready.csv')

# get useful list of all unique departments, majors, instructors, courses, CRNs, and students
uniqueDept = df['ProgCode'].unique()
uniqueMjr = df['major'].unique()
uniqueInst = df['facultyID'].unique()
uniqueCrs = df['crsTitle'].unique()
uniqueCRN = df['CRN'].unique()
uniqueStud = df['SID'].unique()

# creates a thorough course table; information: Course, Enrollments, Sections, Faculty, Students, weighted GPA and std deviation.
# Cleaned Course Table: (courseTable.csv)
with open('courseTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Course', 'Enrollments', 'Sections',
                       'Faculty', 'Students', 'GPA W', 'Deviation'])
    len_cols = len(df['crsTitle'].unique())
    for i in range(len_cols):
        # Number of Enrollments (how many total students were taught overall sections, all courses)
        def crsEnrollments(df, course):
            secs = df.loc[df['crsTitle'] == course, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        crsEnroll = crsEnrollments(df, uniqueCrs[i])

        # Number of Sections
        def crsSections(df, course):
            return df.loc[df['crsTitle'] == course, 'CRN'].unique()
        crsSec = len(crsSections(df, uniqueCrs[i]).tolist())

        # Number of distinct instructors
        def crsInst(df, course, inst):
            return df.loc[df['crsTitle'] == course, inst].unique()
        crsFac = len(crsInst(df, uniqueCrs[i], 'facultyID').tolist())

        # Number of Students that took course
        def crsStud(df, course, stud):
            return df.loc[df['crsTitle'] == course, stud].unique()
        studNum = len(crsInst(df, uniqueCrs[i], 'SID').tolist())

        # Average GPA W - weighted
        def crsWeighted(df, course, value, weight):
            gpaw = (df.loc[df['crsTitle'] == course, weight] * df.loc[df['crsTitle']
                    == course, value]).sum() / df.loc[df['crsTitle'] == course, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = crsWeighted(df, uniqueCrs[i], 'finGradN', 'credHrs')

        # Standard Deviation
        def crsSTD(df, course, gpa):
            crsstd = df.loc[df['crsTitle'] == course, gpa].std()
            return float("{0:.3f}".format(crsstd))
        stdD = crsSTD(df, uniqueCrs[i], 'finGradN')

        my_writer.writerow(
            [uniqueCrs[i], crsEnroll, crsSec, crsFac, studNum, AvgW, stdD])

# creates a thorough major table; information: Major, Enrollments (all course enrollments of students in that major), Sections, Courses, and weighted GPA.
# Cleaned Major Table: (majorTable.csv)
with open('majorTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(
        ['Major', 'Enrollments', 'Sections', 'Courses', 'GPA W'])
    len_cols = len(df['major'].unique())
    for i in range(len_cols):
        # Number of Enrollments (how many total students were taught overall sections, all courses)
        def mjrEnrollments(df, major):
            secs = df.loc[df['major'] == major, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        mjrEnroll = mjrEnrollments(df, uniqueMjr[i])

        # Number of Sections
        def mjrSections(df, major):
            return df.loc[df['major'] == major, 'CRN'].unique()
        mjrSec = len(mjrSections(df, uniqueMjr[i]).tolist())

        # Number of distinct courses
        def mjrCourses(df, major, course):
            return df.loc[df['major'] == major, course].unique()
        mjrCourse = len(mjrCourses(df, uniqueMjr[i], 'crsTitle').tolist())

        # Average GPA W - weighted
        def mjrWeighted(df, major, value, weight):
            gpaw = (df.loc[df['major'] == major, weight] * df.loc[df['major'] ==
                    major, value]).sum() / df.loc[df['major'] == major, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = mjrWeighted(df, uniqueMjr[i], 'finGradN', 'credHrs')

        my_writer.writerow([uniqueMjr[i], mjrEnroll, mjrSec, mjrCourse, AvgW])

# creates a thorough department table; information: Department, Enrollments (all students enrolled in courses within that department), Sections, Courses, Instructors, and weighted GPA.
# Cleaned Department Table: (deptTable.csv)
with open('deptTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Department', 'Enrollments',
                       'Sections', 'Courses', 'Instructors', 'GPA W'])
    len_cols = len(uniqueDept)
    for i in range(len_cols):
        # Number of Enrollments
        def enrollments(df, dept):
            secs = df.loc[df['ProgCode'] == dept, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        enrollNum = enrollments(df, uniqueDept[i])

        # Number of Sections
        def sections(df, dept):
            return df.loc[df['ProgCode'] == dept, 'CRN'].unique()
        secNum = len(sections(df, uniqueDept[i]).tolist())

        # Number of distinct courses
        def courses(df, dept):
            return df.loc[df['ProgCode'] == dept, 'crsTitle'].unique()
        courseNum = len(courses(df, uniqueDept[i]).tolist())

        # Average GPA W - weighted
        def avgDeptWeighted(df, dept, value, weight):
            gpaw = (df.loc[df['ProgCode'] == dept, weight] * df.loc[df['ProgCode']
                    == dept, value]).sum() / df.loc[df['ProgCode'] == dept, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = avgDeptWeighted(df, uniqueDept[i], 'finGradN', 'credHrs')

        # Number of unique faculty per dept
        def uniqueFac(df, dept):
            return df.loc[df['ProgCode'] == dept, 'facultyID'].unique()
        facultyNum = len(uniqueFac(df, uniqueDept[i]))

        my_writer.writerow(
            [uniqueDept[i], enrollNum, secNum, courseNum, facultyNum, AvgW])

# creates a thorough instructor table; information: Instructor, Enrollments (number of students taught), Sections taught, Courses taught, Courses title, terms taught, years of teaching in the institution, and weighted GPA.
# Cleaned Instructor Table: (instTable.csv)
with open('instTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Instructor', 'Enrollments', 'Sections',
                       'Courses', 'GPA W', 'Terms', 'Years', 'Courses Title'])
    len_cols = len(df['facultyID'].unique())
    for i in range(len_cols):
        # Number of Enrollments (how many total students were taught overall sections, all courses)
        def instEnrollments(df, inst):
            secs = df.loc[df['facultyID'] == inst, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        instEnroll = instEnrollments(df, uniqueInst[i])

        # Number of Sections
        def instSections(df, inst):
            return df.loc[df['facultyID'] == inst, 'CRN'].unique()
        instSec = len(instSections(df, uniqueInst[i]).tolist())

        # Number of distinct courses
        def instCourses(df, inst, course):
            return df.loc[df['facultyID'] == inst, course].unique()
        instCourse = len(instCourses(df, uniqueInst[i], 'crsTitle').tolist())

        # Average GPA W - weighted
        def avgWeighted(df, inst, value, weight):
            gpaw = (df.loc[df['facultyID'] == inst, weight] * df.loc[df['facultyID']
                    == inst, value]).sum() / df.loc[df['facultyID'] == inst, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = avgWeighted(df, uniqueInst[i], 'finGradN', 'credHrs')

        # Period Taught - How many terms they have taught
        def instTerms(df, inst, year):
            last = df.loc[df['facultyID'] == inst, year].max()
            first = df.loc[df['facultyID'] == inst, year].min()
            return 'From: ', first, ' to: ', last
        periodTT = instTerms(df, uniqueInst[i], 'term')

        # Period Taught in years
        def instYears(df, inst, year):
            last = df.loc[df['facultyID'] == inst, year].max()
            first = df.loc[df['facultyID'] == inst, year].min()
            return last - first, ' years'
        periodTY = instYears(df, uniqueInst[i], 'year')

        # Courses Taught - Which courses instructor has taught
        coursesT = instCourses(df, uniqueInst[i], 'crsTitle').tolist()

        my_writer.writerow([uniqueInst[i], instEnroll, instSec,
                           instCourse, AvgW, periodTT, periodTY, coursesT])
        
