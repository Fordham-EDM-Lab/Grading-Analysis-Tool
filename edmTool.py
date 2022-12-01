"""
This is an Educational Data Mining tool. It reads data from an university and makes analysis of its contents. Created by Luisa Rosa (lrosa6@fordham.edu), with Dr.Daniel Leeds, Dr.Gary Weiss, and Ashley Saliasi at Fordham University.

Library free for use, required citation using ... in any resulting publications.
Library free for redistribution provided you retain the author attributions above.

The following packages are required for installation before use: numpy, pandas, csv, matplotlib
"""

import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

# save the data file as df
df = pd.read_csv('grading-data-6-17-22.csv')

def dataCleanup(df):
    # Data Cleaning - splitting sem/year, dropping Administrative depts, creating a new CRN, and creating "CourseCode" joining the ProgCode with NumCode
    df.replace(" ", np.nan, inplace=True)
    df['finGradN'] = df['finGradN'].astype('float')

    df.drop(df[df['ProgCode'] == 'Administrative CBA'].index,  inplace=True)
    df.drop(df[df['ProgCode'] == 'Administrative FCRH'].index, inplace=True)

    # creates a new CRN: CRN + last two digits of year + one digit based on semester
        # e.g. oldCRN 11135, Summer 2010 course -> CRN: 11135102
    df[['sem', 'year']] = df['term'].str.split(' ', 1, expand=True)

    df['year'] = df['year'].astype('int')

    df.loc[df['sem'] == 'Summer', 'sem'] = 0
    df.loc[df['sem'] == 'Spring', 'sem'] = 1
    df.loc[df['sem'] == 'Fall', 'sem'] = 2
    df['sem'] = df['sem'].astype('int')

    df.rename(columns={'CRN': 'oldCRN'}, inplace=True)

    df['CRN'] = df['oldCRN'] + df['sem'] + df['year']

    #creating "CourseCode" joining the ProgCode with NumCode
    df['NumCode'] = df['NumCode'].fillna(0)
    df['NumCode'] = df['NumCode'].astype(int)
    df['CourseCode'] = df['ProgCode'].astype(str) + df['NumCode'].astype(str)

    return df


# perform necessary data cleanup
df = dataCleanup(df)

#get useful list of all unique departments, majors, instructors, courses, CRNs, and students
uniqueDept = df['ProgCode'].unique()
uniqueMjr = df['major'].unique()
uniqueInst = df['facultyID'].unique()
uniqueCrs = df['crsTitle'].unique()
uniqueCRN = df['CRN'].unique()
uniqueStud = df['SID'].unique()

# creates a thorough course table; information: Course, Enrollments, Sections, Faculty, Students, weighted GPA and std deviation.
#Cleaned Course Table: (courseTable.csv)
with open('courseTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Course', 'Enrollments', 'Sections', 'Faculty', 'Students', 'GPA W', 'Deviation'])
    len_cols = len(df['crsTitle'].unique())
    for i in range(len_cols):
        #Number of Enrollments (how many total students were taught overall sections, all courses)
        def crsEnrollments(df, course):
            secs = df.loc[df['crsTitle'] == course, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        crsEnroll = crsEnrollments(df, uniqueCrs[i])

        #Number of Sections
        def crsSections(df, course):
            return df.loc[df['crsTitle'] == course, 'CRN'].unique()
        crsSec = len(crsSections(df, uniqueCrs[i]).tolist())

        #Number of distinct instructors
        def crsInst(df, course, inst):
            return df.loc[df['crsTitle'] == course, inst].unique()
        crsFac = len(crsInst(df, uniqueCrs[i], 'facultyID').tolist()) 
        
        #Number of Students that took course
        def crsStud(df, course, stud):
            return df.loc[df['crsTitle'] == course, stud].unique()
        studNum = len(crsInst(df, uniqueCrs[i], 'SID').tolist())

        #Average GPA W - weighted
        def crsWeighted(df, course, value, weight):
            gpaw = (df.loc[df['crsTitle'] == course, weight] * df.loc[df['crsTitle'] == course, value]).sum() / df.loc[df['crsTitle'] == course, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = crsWeighted (df, uniqueCrs[i], 'finGradN', 'credHrs')
        
        #Standard Deviation
        def crsSTD(df, course, gpa):
            crsstd = df.loc[df['crsTitle'] == course, gpa].std()
            return float("{0:.3f}".format(crsstd))
        stdD = crsSTD(df, uniqueCrs[i], 'finGradN')      
        
        my_writer.writerow([uniqueCrs[i], crsEnroll, crsSec, crsFac, studNum, AvgW, stdD])

# creates a thorough major table; information: Major, Enrollments (all course enrollments of students in that major), Sections, Courses, and weighted GPA.
#Cleaned Major Table: (majorTable.csv)
with open('majorTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Major', 'Enrollments', 'Sections', 'Courses', 'GPA W'])
    len_cols = len(df['major'].unique())
    for i in range(len_cols):
        #Number of Enrollments (how many total students were taught overall sections, all courses)
        def mjrEnrollments(df, major):
            secs = df.loc[df['major'] == major, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        mjrEnroll = mjrEnrollments(df, uniqueMjr[i])

        #Number of Sections
        def mjrSections(df, major):
            return df.loc[df['major'] == major, 'CRN'].unique()
        mjrSec = len(mjrSections(df, uniqueMjr[i]).tolist())

        #Number of distinct courses
        def mjrCourses(df, major, course):
            return df.loc[df['major'] == major, course].unique()
        mjrCourse = len(mjrCourses(df, uniqueMjr[i], 'crsTitle').tolist()) 

        #Average GPA W - weighted
        def mjrWeighted(df, major, value, weight):
            gpaw = (df.loc[df['major'] == major, weight] * df.loc[df['major'] == major, value]).sum() / df.loc[df['major'] == major, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = mjrWeighted (df, uniqueMjr[i], 'finGradN', 'credHrs')

        my_writer.writerow([uniqueMjr[i], mjrEnroll, mjrSec, mjrCourse, AvgW])

# creates a thorough department table; information: Department, Enrollments (all students enrolled in courses within that department), Sections, Courses, Instructors, and weighted GPA.
#Cleaned Department Table: (deptTable.csv)
with open('deptTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Department', 'Enrollments', 'Sections', 'Courses', 'Instructors', 'GPA W'])
    len_cols = len(uniqueDept)
    for i in range(len_cols):
        #Number of Enrollments
        def enrollments(df, dept):
            secs = df.loc[df['ProgCode'] == dept, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        enrollNum = enrollments(df, uniqueDept[i])

        #Number of Sections
        def sections(df, dept):
            return df.loc[df['ProgCode'] == dept, 'CRN'].unique()
        secNum = len(sections(df, uniqueDept[i]).tolist())

        #Number of distinct courses
        def courses(df, dept):
            return df.loc[df['ProgCode'] == dept, 'crsTitle'].unique()
        courseNum = len(courses(df, uniqueDept[i]).tolist()) 

        #Average GPA W - weighted
        def avgDeptWeighted(df, dept, value, weight):
            gpaw = (df.loc[df['ProgCode'] == dept, weight] * df.loc[df['ProgCode'] == dept, value]).sum() / df.loc[df['ProgCode'] == dept, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = avgDeptWeighted (df, uniqueDept[i], 'finGradN', 'credHrs')
        
        #Number of unique faculty per dept
        def uniqueFac(df, dept):
            return df.loc[df['ProgCode'] == dept, 'facultyID'].unique()
        facultyNum = len(uniqueFac(df, uniqueDept[i]))
        
        my_writer.writerow([uniqueDept[i], enrollNum, secNum, courseNum, facultyNum, AvgW])

# creates a thorough instructor table; information: Instructor, Enrollments (number of students taught), Sections taught, Courses taught, Courses title, terms taught, years of teaching in the institution, and weighted GPA.
#Cleaned Instructor Table: (instTable.csv)
with open('instTable.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile)
    my_writer.writerow(['Instructor', 'Enrollments', 'Sections', 'Courses', 'GPA W', 'Terms', 'Years', 'Courses Title'])
    len_cols = len(df['facultyID'].unique())
    for i in range(len_cols):
        #Number of Enrollments (how many total students were taught overall sections, all courses)
        def instEnrollments(df, inst):
            secs = df.loc[df['facultyID'] == inst, 'CRN'].unique()
            return df.loc[secs, 'class_size'].sum()
        instEnroll = instEnrollments(df, uniqueInst[i])

        #Number of Sections
        def instSections(df, inst):
            return df.loc[df['facultyID'] == inst, 'CRN'].unique()
        instSec = len(instSections(df, uniqueInst[i]).tolist())

        #Number of distinct courses
        def instCourses(df, inst, course):
            return df.loc[df['facultyID'] == inst, course].unique()
        instCourse = len(instCourses(df, uniqueInst[i], 'crsTitle').tolist()) 

        #Average GPA W - weighted
        def avgWeighted(df, inst, value, weight):
            gpaw = (df.loc[df['facultyID'] == inst, weight] * df.loc[df['facultyID'] == inst, value]).sum() / df.loc[df['facultyID'] == inst, weight].sum()
            return float("{0:.3f}".format(gpaw))
        AvgW = avgWeighted (df, uniqueInst[i], 'finGradN', 'credHrs')

        #Period Taught - How many terms they have taught
        def instTerms(df, inst, year):
            last = df.loc[df['facultyID'] == inst, year].max()
            first = df.loc[df['facultyID'] == inst, year].min()
            return 'From: ', first, ' to: ', last
        periodTT = instTerms(df, uniqueInst[i], 'term')

        #Period Taught in years
        def instYears(df, inst, year):
            last = df.loc[df['facultyID'] == inst, year].max()
            first = df.loc[df['facultyID'] == inst, year].min()
            return last - first, ' years'
        periodTY = instYears(df, uniqueInst[i], 'year')

        #Courses Taught - Which courses instructor has taught
        coursesT = instCourses(df, uniqueInst[i], 'crsTitle').tolist()

        my_writer.writerow([uniqueInst[i], instEnroll, instSec, instCourse, AvgW, periodTT, periodTY, coursesT])


# Compute weighted average
def avgWeighted(df, value, weight):
    return (df[weight] * df[value]).sum() / df[weight].sum()

# average & std grades of all courses
def UniversityCoursesMean(df):
    print("\nThis is the the GPA of all courses in the university: ")
    print(avgWeighted(df, 'finGradN', 'credHrs'))
    print("This is the Standard Deviation of all courses GPA: ")
    print(df['finGradN'].std())

# average & std grades of all students taking courses in specific department
def DepartmentCoursesMean(df, dept):
    deptMean = df.loc[df['ProgCode'] == dept, 'finGradN'].mean()
    stdDept = df.loc[df['ProgCode'] == dept, 'finGradN'].std()
    print("\nThis is " + dept + " department courses mean grade: ")
    print(deptMean)
    print("This is " + dept + " department courses grade standard deviation: ")
    print(stdDept)

# average & std dev of grades of all students of a specific major (all courses in major department or not)
def MajorDegreeMean(df, major):
    majorMean = df.loc[df['major'] == major, 'finGradN'].mean()
    stdMajor = df.loc[df['major'] == major, 'finGradN'].std()
    print("\nThis is " + major + " majors mean grade: ")
    print(majorMean)
    print("This is " + major + " majors grade standard deviation: ")
    print(stdMajor)

# average & std dev of grades of all courses in the specific major's department that students with that specific major take
def MajorDeptMean(df, major, dept):
    DMajorMean = df.loc[(df['major'] == major) & (df['ProgCode'] == dept), 'finGradN'].mean()
    stdDMajor = df.loc[(df['major'] == major) & (df['ProgCode'] == dept), 'finGradN'].std()
    print("\nThis is " + major + " majors mean grade in its department courses: ")
    print(DMajorMean)
    print("This is " + major + " majors grade standard deviation in its department courses: ")
    print(stdDMajor)

# average GPA, std dev, lowest and highest grades of a specific faculty.
def FacultyAnalysis(df, fac):
    FacMean = df.loc[df['facultyID'] == fac, 'finGradN'].mean()
    stdFac = df.loc[df['facultyID'] == fac, 'finGradN'].std()
    facLow = df.loc[df['facultyID'] == fac, 'finGradN'].min()
    facHigh = df.loc[df['facultyID'] == fac, 'finGradN'].max()
    print("\nThis is " + fac + " Faculty Analysis.")
    print("Instructor's GPA: ")
    print(FacMean)
    print("Student's std. dev. grades: ")
    print(stdFac)
    print("Lowest and highest grades assigned: ")
    print(facLow)
    print(facHigh)

# a list of all unique departments, majors, instructors, courses, CRNs, and students
def unique(df):
    req = input("\nWould you like a list of unique Departments, Majors, Instructor IDs, Courses, CRNs, or Student IDs?\n")
    if (req == 'Departments'):
        print("\nThese are all Departments:")
        print(uniqueDept)
    elif (req == 'Majors'):
        print("\nThese are all Majors:")
        print(uniqueMjr)
    elif (req == 'Instructor IDs'):
        print("\nThese are all Instructor IDs:")
        print(uniqueInst)
    elif (req == 'Courses'):
        print("\nThese are all Courses:")
        print(uniqueCrs)
    elif (req == 'CRNs'):
        print("\nThese are all CRNs:")
        print(uniqueCRN)
    elif (req == 'Student IDs'):
        print("\nThese are all Student IDs:")
        print(uniqueStud)
    else:
        print("This is not a valid option.")

# generate table of student grade distribution of all courses
def AllCoursesGradeDist(df):
    studGradeDistribution = df['finGradC'].value_counts()
    print("\nThis is the Student Grade Distribution over all courses: ")
    print(studGradeDistribution)

# Compute the number of enrollments using class size
def enrollments(df, classSize):
    return (df[classSize]).sum()

# Create a table with number of enrollments per department 
def DeptEnroll(df):
    print("\nThis is the number of enrollments per university department: ")
    print(df.groupby(df['ProgCode']).apply(enrollments, 'class_size'))

# Create a table |major, # of unique students|
def StudMjrCount(df):
    print("\nThis is the number of unique students enrolled in a major: ")
    print(df['major'].value_counts())

#Instructor Grade Distribution table
def GradeDist(df):
    it = pd.read_csv('instTable.csv')
    ranges = [2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0]
    instGradeDist = it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count() #Number of instructors in each GPA range
    instPer = ((it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count())/ (len(it['GPA W']))) *100 #Percentage
    print("\nThis is the Student Grade Distribution over all instructors: ")
    print(instGradeDist)
    print("in percentages: ")
    print(instPer)


# MAIN:
# initialize tool
print("\n\n######################################################")
print("Welcome to Fordham's EDM Lab Grading Data Mining Tool!")
print("######################################################\n")

Aloop = True
while Aloop == True:
    print("\nWhich function would you like to run? Type 'help' to see possible functions.")
    # gets user input to call specific function
    requestA = input("Please type your request so our tool knows what to do: ")

    if requestA == "help":
        print(
            "\nGPA --> compute the GPA of all courses in the univeristy, all courses in the department, all students that are majoring in a specific major taking any course (related or unrelated to their major), all students that are majoring in a specific major taking any course in their major's department, and the grades standard deviation. Also, generates a table of student grade distribution of all courses and a a table with instructor weighted GPA distrbution. \n"
            "FacultyAnalysis --> Compute the GPA over all faculty's courses, grades standard deviation, and lowest and higher grade.\n"
            "DeptEnroll --> Create a table with number of enrollments per department\n"
            "StudMjrCount --> Create a table with number of students per major\n"
            "UniqueList --> get a list of all unique departments, majors, instructors, courses, CRNs, and students\n"
            "Skip --> you want to create specific graphs and illustrations of the data\n"
            "All --> run all commands above\n"
        )

    elif requestA == "GPA":
        dept = input("\nWhich department? Use a valid Department\n")
        major = input("Which major? Use a valid Major\n")
        if dept not in uniqueDept:
            print("This is not a valid Department. If you need to see a list of valid departments, type UniqueList.")
        elif major not in uniqueMjr:
            print("This is not a valid Major. If you need to see a list of valid majors, type UniqueList.")
        else:
            UniversityCoursesMean(df)
            AllCoursesGradeDist(df)
            GradeDist(df)
            DepartmentCoursesMean(df, dept)
            MajorDegreeMean(df, major)
            MajorDeptMean(df, major, dept)

    elif requestA == "FacultyAnalysis":
        faculty = input("\nWhich faculty? Use a valid Faculty ID.\n")
        if faculty not in uniqueInst:
            print("This is not a valid Faculty ID. If you need to see a list of valid instructors, type UniqueList.")
        else:
            FacultyAnalysis(df, faculty)

    elif requestA == "DeptEnroll":
        DeptEnroll(df)
    
    elif requestA == 'StudMjrCount':
        StudMjrCount(df)

    elif requestA == "UniqueList":
        unique(df)

    elif requestA == 'Skip':
        Aloop = False

    elif requestA == "All":
        dept = input("\nWhich department? Use a valid Department.\n")
        major = input("Which major? Use a valid Major.\n")
        faculty = input("Which faculty? Use a valid Faculty ID.\n")
        if dept not in uniqueDept:
            print("This is not a valid Department. If you need to see a list of valid departments, type UniqueList.")
        elif major not in uniqueMjr:
            print("This is not a valid Major. If you need to see a list of valid majors, type UniqueList.")
        elif faculty not in uniqueInst:
            print("This is not a valid Faculty ID. If you need to see a list of valid instructors, type UniqueList.")
        else:
            UniversityCoursesMean(df)
            DepartmentCoursesMean(df, dept)
            MajorDegreeMean(df, major)
            MajorDeptMean(df, major, dept)
            FacultyAnalysis(df, faculty)
            AllCoursesGradeDist(df)
            DeptEnroll(df)
            StudMjrCount(df)
            GradeDist(df)
    
    else:
        print("This is not a valid request. Type 'help' if you need valid options.\n")

    if Aloop == True:
        rep = input("\nDo you want to perform any other analysis? (yes/no)  ")
        if rep == 'no':
            Aloop = False


#RESEARCH CODE:
#Function to create a list of conssecutive numbers spaced out as needed (to use when creating bins for a graph)
def createList(r1, r2, space):
    if (r1 == r2):
        return 0
    else:
        cl = []
        while(r1 < r2+1): 
            cl.append(r1)
            r1 += space
        return cl

# department grades bar chart (y=gpa, x=department) for departments with enrollments > 600
def DeptGPA(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.drop(DeptTable[DeptTable['Enrollments']<600].index, inplace = True)
    DeptTable.reset_index()
    DeptTable.sort_values('GPA W', inplace=True)
    da = DeptTable.plot.bar(x='Department', y='GPA W', figsize=(20,5), color='#18979e', legend=False)
    da.set_xlabel("Department")
    da.set_ylabel("Weighted GPA")
    plt.axis([None, None, 2.5, 4.0])
    da.yaxis.grid()
    plt.savefig('DeptAvgBarTrunc.jpg', bbox_inches='tight')

# department size bar chart (y=enrollments, x=department) for departments with enrollments > 600
def DeptSize(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.sort_values('Enrollments', inplace=True)
    de = DeptTable.plot.bar(x='Department', y='Enrollments', figsize=(20,5), color='#f5a142', legend=False)
    de.yaxis.grid()
    de.set_xlabel("Department")
    de.set_ylabel("Department Enrollments")
    plt.savefig('DeptEnrolBarTrunc.jpg', bbox_inches='tight')   

# bar chart that shows number of enrollments and department average grades simultaneously.
def DeptEnrollGPA(df):
    DeptTable = pd.read_csv('deptTable.csv')
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.axis([None, None, 2.5, 4.0])
    ax1.set_ylabel('Weighted GPA')
    ax2.set_ylabel('Department Enrollments')
    DeptTable.plot.bar(x='Department', y='GPA W', ax=ax1, figsize=(20,5), color='#18979e')
    DeptTable.plot.bar(x='Department', y='Enrollments', ax=ax2, figsize=(20,5), color='#f5a142', alpha=0.8)
    plt.savefig('DeptAvgEnrolTrunc.jpg', bbox_inches='tight')

# total number of students in a department vs. grades in that department scatter plot, for departments with enrollments > 600
def DeptStudGPA(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.drop(DeptTable[DeptTable['Enrollments']<600].index, inplace = True)
    DeptTable.reset_index()
    dt = DeptTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#e08114', s=50)
    dt.set_xlabel("Department Enrollments")
    dt.set_ylabel("Weighted GPA")
    dt.yaxis.grid()
    plt.savefig('StudAvgScatTrunc.jpg', bbox_inches='tight')

bins = createList(2, 4, 0.05)
# instructor Grade Distribution (histogram) -- frequency of grades
def InstGPA(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('GPA W', inplace=True)
    it = InstTable.plot.hist(x='Instructor', y='GPA W', figsize=(20,5), bins=bins, color='#4b8745', legend=False)
    it.set_xlabel("Weighted GPA")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(bins, rotation='vertical')
    plt.axis([2.0, 4.0, None, None])
    it.yaxis.grid()
    #Display number of sections taught per instructor 
    plt.savefig('InstGradeHist.jpg', bbox_inches='tight')

# instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections
def InstGPATrunc(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('GPA W', inplace=True)
    InstTable.drop(InstTable[InstTable['Sections']<10].index, inplace = True)
    InstTable.reset_index()
    InstTable.to_csv('instHistTrunc.csv', encoding='utf-8-sig')
    it = InstTable.plot.hist(x='Instructor', y='GPA W', figsize=(20,5), bins=bins, color='#f5a142', legend=False)
    it.set_xlabel("Weighted GPA")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(bins, rotation='vertical')
    plt.axis([2.0, 4.0, None, None])
    it.yaxis.grid()
    plt.savefig('InstGradeHistTrunc.jpg', bbox_inches='tight')

# instructor Enrollment Distribution histogram
def InstEnroll(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('Enrollments', inplace=True)
    enrollList = createList(0,3700, 50)
    it = InstTable.plot.hist(x='Instructor', y='Enrollments', figsize=(20,5), bins=enrollList, color='#4b8745', legend=False)
    it.set_xlabel("Enrollment Range")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['Enrollments'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(enrollList, rotation='vertical')
    plt.axis([0, 3700, None, None])
    it.yaxis.grid()
    plt.savefig('InstEnrolHist.jpg', bbox_inches='tight')

# instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200
def InstEnrollTrunc(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('Enrollments', inplace=True)
    InstTable.drop(InstTable[InstTable['Enrollments']<200].index, inplace = True)
    InstTable.reset_index()
    InstTable.to_csv('instTableTrunc.csv', encoding='utf-8-sig')
    enrollList = createList(200,3700, 50)
    it = InstTable.plot.hist(x='Instructor', y='Enrollments', figsize=(18,5), bins=enrollList, color='#f5a142', legend=False)
    it.set_xlabel("Enrollment Range")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['Enrollments'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(enrollList, rotation='vertical')
    plt.axis([200, 3700, None, None])
    it.yaxis.grid()
    plt.savefig('InstEnrollHistTrunc200.jpg', bbox_inches='tight')

# gpa vs major size (number of enrollments) scatter plot
def MjrGPA(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mj = mjrTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#3c6e37', s=50)
    mj.set_xlabel("Major Enrollments")
    mj.set_ylabel("Weighted GPA")
    mj.yaxis.grid()
    plt.savefig('MjrAvgScat.jpg', bbox_inches='tight')

# gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments
def MjrGPATrunc(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.drop(mjrTable[mjrTable['Enrollments']<10000].index, inplace = True)
    mjrTable.reset_index()
    mj = mjrTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#e08114', s=50)
    mj.set_xlabel("Major Enrollments")
    mj.set_ylabel("Weighted GPA")
    mj.yaxis.grid()
    plt.savefig('MjrAvgScatTrunc.jpg', bbox_inches='tight')

# major vs enrollments bar chart, for majors with > 10,000 enrollments
def MjrEnroll(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.sort_values('Enrollments', inplace=True)
    mjrTable.drop(mjrTable[mjrTable['Enrollments']<10000].index, inplace = True)
    mjrTable.reset_index()
    mj = mjrTable.plot.bar(x='Major', y='Enrollments', figsize=(15,5), color='#f5a142', legend=False)
    mj.set_xlabel("Majors")
    mj.set_ylabel("Enrollments")
    mj.yaxis.grid()
    plt.savefig('MjrEnrolBarTrunc.jpg', bbox_inches='tight')

# distribution of grades bar chart for courses with > 70 sections
def CourseGPA(df):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)
    crsTable.drop(crsTable[crsTable['Sections']<70].index, inplace = True)
    crsTable.to_csv('crsTableTrunc.csv', encoding='utf-8-sig')
    ct = crsTable.plot.bar(x='Course', y='GPA W', figsize=(20,5), color='#f5a142', legend=False)
    ct.set_ylabel("Weighted GPA for 30 most taken courses")
    ct.set_xlabel("Courses")
    plt.axis([None, None, 2.5, 4.0])
    ct.yaxis.grid()
    plt.savefig('crsGradeBarTrunc.jpg', bbox_inches='tight')

Bloop = True
while Bloop == True:
    print("\nWhat graphs and illustrations would you like to create? Type 'help' to see possible options.")
    # gets user input to call specific function
    requestB = input("Please type your request so our tool knows what to do: ")

    if requestB == "help":
        print(
            "\nDeptAnalysis --> bar chart of department grades, department size, number of enrollments and department GPA. Also, generates a scatter plot of total number of students in a department and grades in that department. All illustrations have a threshold of departments with enrollments > 600.\n"
            "InstAnalysis --> instructor Grade Distribution (histogram) -- frequency of grades and a threshold version, excluding inst teaching < 10 sections; instructor Enrollment Distribution (histogram), and a threshold version where number of students taught(enrollements) > 200.\n"
            "MjrAnalysis --> gpa vs major size (number of enrollments) scatter plot, and a threshold version for majors with > 10,000 enrollments; and major vs enrollments bar chart, for majors with > 10,000 enrollments\n"
            "CrsAnalysis--> distribution of grades bar chart for courses with > 70 sections\n"
            "All --> run all commands above\n"
        )

    elif requestB == "DeptAnalysis":
        DeptGPA(df)
        DeptSize(df)
        DeptEnrollGPA(df)
        DeptStudGPA(df)

    elif requestB == "InstAnalysis":
        InstGPA(df)
        InstGPATrunc(df)
        InstEnroll(df)
        InstEnrollTrunc(df)

    elif requestB == "MjrAnalysis":
        MjrGPA(df)
        MjrGPATrunc(df)
        MjrEnroll(df)

    elif requestB == "CourseAnalysis":
        CourseGPA(df)

    elif requestB == "All":
        DeptGPA(df)
        DeptSize(df)
        DeptEnrollGPA(df)
        DeptStudGPA(df)
        InstGPA(df)
        InstGPATrunc(df)
        InstEnroll(df)
        InstEnrollTrunc(df)
        MjrGPA(df)
        MjrGPATrunc(df)
        MjrEnroll(df)
        CourseGPA(df)

    else:
        print("This is not a valid request. Type 'help' if you need valid options.\n")

    wantGraphs = input("Would you like to generate any other illustration or graph of the data? (yes/no)  ")
    if wantGraphs == 'no':
        Bloop = False

print("\n###############################################################")
print("Thank you for using Fordham's EDM Lab Grading Data Mining Tool!")
print("###############################################################\n")
