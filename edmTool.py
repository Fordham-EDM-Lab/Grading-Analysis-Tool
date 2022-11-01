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

    df['CRN'] = df['oldCRN'].astype(string) + df['sem'].astype(string) + df['year'].astype(string)


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

# TODO: add mapping of courses x majors to tool
# TODO: Course Level Report (courseLevel.csv)
# TODO: when creating tables, make sure to generate a file that contains them!

# separate the research code into classes that can be called to perform the specific section of the code:
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
    DMajorMean = df.loc[(df['major'] == major) & (df['ProgCode'] == dept), 'finGradN'].mean()
    stdDMajor = df.loc[(df['major'] == major) & (df['ProgCode'] == dept), 'finGradN'].std()
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

# a list of all unique departments, majors, instructors, courses, CRNs, and students
def unique(df):
    req = input("Would you like a list of unique: Departments, Majors, Instructor IDs, Courses, CRNs, or Student IDs")
    if (req == 'Departments'):
        print(uniqueDept)
    if (req == 'Majors'):
        print(uniqueMjr)
    if (req == 'Instructor IDs'):
        print(uniqueInst)
    if (req == 'Courses'):
        print(uniqueCrs)
    if (req == 'CRNs'):
        print(uniqueCRN)
    if (req == 'Student IDs'):
        print(uniqueStud)
    else:
        print("This is not a valid option.")

# generate table of student grade distribution of all courses
def AllCoursesGradeDist(df):
    print(studGradeDistribution = df['finGradC'].value_counts())

# Compute the number of enrollments using class size
def enrollments(df, classSize):
    return (df[classSize]).sum()

# Create a table with number of enrollments per department 
def DeptEnroll(df):
    print(df.groupby(df['ProgCode']).apply(enrollments, 'class_size'))

# Create a table |major, # of unique students|
def StudMjrCount(df):
    print(df['major'].value_counts())

#Instructor Grade Distribution table
def GradeDist(df):
    it = pd.read_csv('instTable.csv')
    ranges = [2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0]
    instGradeDist = it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count() #Number of instructors in each GPA range
    instPer = ((it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count())/ (len(it['GPA W']))) *100 #Percentage
    print(instGradeDist)
    print(instPer)

# MAIN:
# initialize tool
print("######################################################")
print("Welcome to Fordham's EDM Lab Grading Data Mining Tool!")
print("######################################################")

Aloop = True
while Aloop == True:
    print("Please type your request so our tool knows what to do.")
    print("type 'help' to see possible functions.")
    # gets user input to call specific function
    requestA = input

    if requestA == "help":
        print(
            "AllCourseMean --> compute the GPA of all courses in the univeristy, and the grades standard deviation.\n"
            "DeptCourseMean --> compute the GPA of all courses in the department, and the grades standard deviation.\n"
            "MajorDegreeMean --> compute the GPA and standard deviation of all students that are majoring in a specific major taking any course (related or unrelated to their major).\n"
            "MajorDeptMean --> compute the GPA and standard deviation of all students that are majoring in a specific major taking any course in their major's department.\n"
            "FacultyAnalysis --> Compute the GPA over all faculty's courses, grades standard deviation, and lowest and higher grade.\n"
            "UniqueList --> get a list of all unique departments, majors, instructors, courses, CRNs, and students\n"
            "AllCoursesGradeDist --> generate table of student grade distribution of all courses\n"
            "DeptEnroll --> Create a table with number of enrollments per department\n"
            "StudMjrCount --> Create a table with number of students per major\n"
            "Skip --> you want to create specific graphs and illustrations of the data\n"
            "GradeDist --> create a table with instructor weighted GPA distrbution\n"
        )

    if requestA == "AllCourseMean":
        UniversityCoursesMean(df)

    if requestA == "DeptCourseMean":
        # TODO: check if it is actually a valid ProgCode
        dept = input("Which department? Use a valid 'ProgCode'")
        DepartmentCoursesMean(df, dept)

    if requestA == "MajorDegreeMean":
        # TODO: check if it is actually a valid major
        major = input("Which major? Use a valid 'major'")
        MajorDegreeMean(df, major)

    if requestA == "MajorDeptMean":
        # TODO: check if it is actually a valid major
        major = input("Which major? Use a valid 'major'")
        # TODO: check if it is actually a valid ProgCode
        dept = input("From which department? Use a valid 'ProgCode'")
        MajorDeptMean(df, major, dept)

    if requestA == "FacultyAnalysis":
        # TODO: check if it is actually a valid facultyID
        faculty = input("Which faculty? Use a valid 'facultyID'")
        FacultyAnalysis(df, faculty)

    if requestA == "UniqueList":
        unique(df)

    if requestA == "AllCoursesGradeDist":
        AllCoursesGradeDist(df)

    if requestA == "DeptEnroll":
        DeptEnroll(df)
    
    if requestA == 'StudMjrCount':
        StudMjrCount(df)
    
    if requestA == 'GradeDist':
        GradeDist(df)

    if requestA == 'Skip':
        Aloop = False
    
    else:
        print("This is not a valid request. Type 'help' if you need valid options.\n")

    rep = input("Do you want to perform any other analysis? (yes/no)")
    if rep == 'no':
        Aloop = False

#RESEARCH CODE:
#TODO: save each into a file instead of printing it out.
# separate the research code into classes that can be called to create the specific illustrations of the data:
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
    wantGraphs = input("Would you like to generate a illustration or graph of the data? (yes/no)")
    if wantGraphs == 'no':
        Bloop = False

    print("Please type your request so our tool knows what to do.")
    print("type 'help' to see possible graphs and illustrations.")
    # gets user input to call specific function
    requestB = input

    if requestB == "help":
        print(
            "DeptGPA --> department grades bar chart (y=gpa, x=department) for departments with enrollments > 600\n"
            "DeptSize --> department size bar chart (y=enrollments, x=department) for departments with enrollments > 600\n"
            "DeptEnrollGPA --> bar chart that shows number of enrollments and department average grades simultaneously.\n"
            "DeptStudGPA --> total number of students in a department vs. grades in that department scatter plot, for departments with enrollments > 600\n"
            "InstGPA --> instructor Grade Distribution (histogram) -- frequency of grades\n"
            "InstGPATrunc --> instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections\n"
            "InstEnroll --> instructor Enrollment Distribution histogram\n"
            "InstEnrollTrunc --> instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200\n"
            "MjrGPA --> gpa vs major size (number of enrollments) scatter plot\n"
            "MjrGPATrunc --> gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments\n"
            "MjrEnroll --> major vs enrollments bar chart, for majors with > 10,000 enrollments\n"
            "CourseGPA --> distribution of grades bar chart for courses with > 70 sections\n"
        )

    if requestB == "DeptGPA":
        DeptGPA(df)

    if requestB == "DeptSize":
        DeptSize(df)

    if requestB == "DeptEnrollGPA":
        DeptEnrollGPA(df)

    if requestB == "DeptStudGPA":
        DeptStudGPA(df)

    if requestB == "InstGPA":
        InstGPA(df)

    if requestB == "InstGPATrunc":
        InstGPATrunc(df)

    if requestB == "InstEnroll":
        InstEnroll(df)

    if requestB == "InstEnrollTrunc":
        InstEnrollTrunc(df)

    if requestB == "MjrGPA":
        MjrGPA(df)

    if requestB == "MjrGPATrunc":
        MjrGPATrunc(df)

    if requestB == "MjrEnroll":
        MjrEnroll(df)

    if requestB == "CourseGPA":
        CourseGPA(df)
    
    else:
        print("This is not a valid request. Type 'help' if you need valid options.\n")

