#STEP 3: Tool

import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

#Graph font size
plt.rcParams.update({'font.size': 14})

# save the data file as df
df = pd.read_csv('data-processed-ready.csv')

#TODO: print this out to a file so the user can visit and look at the entire lists
# get useful list of all unique departments, majors, instructors, courses, CRNs, and students
uniqueDept = df['ProgCode'].unique()
uniqueMjr = df['major'].unique()
uniqueInst = df['facultyID'].unique()
uniqueCrs = df['crsTitle'].unique()
uniqueCRN = df['CRN'].unique()
uniqueStud = df['SID'].unique()


#TODO: print out the following to the user without any inputs necessary.

# Compute weighted average
def avgWeighted(df, value, weight):
    return (df[weight] * df[value]).sum() / df[weight].sum()

# generate table of student grade distribution of all courses
def AllCoursesGradeDist(df):
    studGradeDistribution = df['finGradC'].value_counts()
    print("\nThis is the Student Grade Distribution over all courses: ")
    print(studGradeDistribution)

# Instructor Grade Distribution table
def GradeDist(df):
    it = pd.read_csv('instTable.csv')
    ranges = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
              3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0]
    # Number of instructors in each GPA range
    instGradeDist = it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count()
    instPer = ((it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)
                                    ).count()) / (len(it['GPA W']))) * 100  # Percentage
    
    print("\nThis is the Student Grade Distribution over all instructors: ")
    print(instGradeDist)
    print("in percentages: ")
    print(instPer)

# average & std grades of all courses
def UniversityCoursesMean(df):
    print("\nThis is the the GPA of all courses in the university: ")
    print(avgWeighted(df, 'finGradN', 'credHrs'))
    print("This is the Standard Deviation of all courses GPA: ")
    print(df['finGradN'].std())

#TODO: output the unique lists fully.
# a list of all unique departments, majors, instructors, courses, CRNs, and students
def unique(df):
    req = input(
        "\nWould you like a list of unique Departments, Majors, Instructor IDs, Courses, CRNs, or Student IDs?\n")
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
    DMajorMean = df.loc[(df['major'] == major) & (
        df['ProgCode'] == dept), 'finGradN'].mean()
    stdDMajor = df.loc[(df['major'] == major) & (
        df['ProgCode'] == dept), 'finGradN'].std()
    print("\nThis is " + major + " majors mean grade in its department courses: ")
    print(DMajorMean)
    print("This is " + major +
          " majors grade standard deviation in its department courses: ")
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


# MAIN:
# initialize tool
#TODO: reword some thing so that the tool is more easy to use.
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
            print(
                "This is not a valid Major. If you need to see a list of valid majors, type UniqueList.")
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
            print(
                "This is not a valid Major. If you need to see a list of valid majors, type UniqueList.")
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


# RESEARCH CODE:
# Function to create a list of conssecutive numbers spaced out as needed (to use when creating bins for a graph)
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
def coloring(dt):
    # department grades bar chart (y=gpa, x=department) for departments with enrollments > 600
    barsColor = []
    #clustering departments per area of study 
    arts = {'Theatre', 'Visual Arts', 'Music', 'Dance', 'Julliard Exchange'}
    comm = {'Comm & Media Stud.', 'Comm. & Culture', 'New Media/Dig. Dsgn', 'Digital Tech/Media', 'Film & Television', 'Journalism', 'Marketing'}
    hum = {'Anthropology', 'Afr. & Afr. Amer Stud.', 'Art History', 'English', 'History', 'Philosophy', 'Theology', 'Irish Stud.', 'Classic Lang & Civ.', 'Amer Catholic Stud.', 'Medieval Stud.', 'Latin Amer & Latino Stud.', 'Comparative Lit.', 'American Stud.', 'Linguistics'}
    lang = {'French', 'German', 'Japanese', 'Russian', 'Arabic', 'Latin', 'Greek', 'Italian', 'Mandarin Chinese', 'Spanish', 'Modern Languages', 'HEBW'}
    sciTec = {'Biological Sci.', 'Chemistry', 'Physics', 'Comp & Info Sci.', 'Math', 'Natural Sci.', 'Environmental Sci.', 'Integrative Neuroscience', 'Information Systems'}
    soSci = {'Economics', 'Political Sci.', 'Psychology', 'Sociology', 'Social Work', 'Peace&Justice Stud.', 'Human. Affairs', 'Human. Stud.', 'Ethics Education', 'WG&S Stud.', "Women's Stud.", 'Middle East Studies', 'International Stud.', 'Urban Stud.',
 'Environmental Policy', 'Environmental Stud.', 'Management'}
    dt.sort_values('GPA W', inplace=True)
    uniqueDept = dt['Department'].unique()
    for dpt in uniqueDept:
        if dpt in arts:
            color = '#e6ae6e' #orangy
        elif dpt in hum:
            color = '#e6ae6e' #orangy
        elif dpt in lang:
            color = '#e6ae6e' #orangy
        elif dpt in comm:
            color = '#94bff7' #light blue
        elif dpt in soSci:
            color = '#94bff7' #sky blue
        elif dpt in sciTec:
            color = '#18979e' #teal
        else:
            color = '#000000' #black
        barsColor.append(color)
    
    return barsColor
    

def DeptGPA(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.drop(DeptTable[DeptTable['Enrollments']<600].index, inplace = True)
    DeptTable.reset_index()
    DeptTable.sort_values('GPA W', inplace=True)
    barsColor = coloring(DeptTable)
    da = DeptTable.plot.bar(x='Department', y='GPA W', figsize=(20,3), color=barsColor, legend=False, width=.8)
    da.set_ylabel("GPA")
    da.set_xlabel(None)
    plt.axhline(DeptTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.axis([None, None, 2.7, 3.8])
    
    colors={'Arts, Humanities, and Language':'#e6ae6e', 'Communication and Social Science':'#94bff7', 'STEM':'#18979e'}   
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    da.legend(handles, labels)
    da.yaxis.grid()
    plt.savefig('Figure2.3.jpg', bbox_inches='tight')

# department size bar chart (y=enrollments, x=department) for departments with enrollments > 600
def DeptSize(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.sort_values('Enrollments', inplace=True)
    de = DeptTable.plot.bar(x='Department', y='Enrollments', figsize=(
        20, 5), color='#f5a142', legend=False)
    de.yaxis.grid()
    de.set_xlabel("Department")
    de.set_ylabel("Department Enrollments")
    plt.axhline(DeptTable['Enrollments'].mean(),
                color='red', linestyle='dashed', linewidth=2)
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
    DeptTable.plot.bar(x='Department', y='GPA W', ax=ax1,
                       figsize=(20, 5), color='#18979e')
    DeptTable.plot.bar(x='Department', y='Enrollments', ax=ax2,
                       figsize=(20, 5), color='#f5a142', alpha=0.8)
    plt.legend(['Enrollments'], loc='best', bbox_to_anchor=(0.9, 0.5, 0, 0.5))
    plt.savefig('DeptAvgEnrolTrunc.jpg', bbox_inches='tight')

    corr = np.corrcoef(DeptTable['Enrollments'], DeptTable['GPA W'])
    print("This is the Correlation Coefficient between Enrollments and GPA: " + corr)

#Scatter plot: total number of students in a department vs. grades in that department enrollments > 600
def DeptStudGPA(df):
    DeptTable = pd.read_csv('deptTable.csv')
    DeptTable.drop(DeptTable[DeptTable['Enrollments']<600].index, inplace = True)
    DeptTable.drop(DeptTable[DeptTable['Enrollments']>26000].index, inplace = True)
    DeptTable.reset_index()
    dotsColor = coloring(DeptTable)
    dt = DeptTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,4), color=dotsColor, s=50)
    plt.yticks(np.arange(2.8, 3.8, step=0.1))
    plt.axhline(DeptTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    dt.set_xlabel("Department Enrollments")
    dt.set_ylabel("GPA")
    colors={'Humanities':'#e6ae6e', 'Communication':'#94bff7', 'STEM':'#18979e'}   
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    dt.legend(handles, labels)
    dt.yaxis.grid()
    plt.savefig('Figure3.2.jpg', bbox_inches='tight')


bins = createList(2, 4, 0.05)
# instructor Grade Distribution (histogram) -- frequency of grades
def InstGPA(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('GPA W', inplace=True)
    it = InstTable.plot.hist(x='Instructor', y='GPA W', figsize=(
        20, 5), bins=bins, color='#4b8745', legend=False)
    it.set_xlabel("Weighted GPA")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['GPA W'].mean(), color='red',
                linestyle='dashed', linewidth=2)
    plt.xticks(bins, rotation='vertical')
    plt.axis([2.0, 4.0, None, None])
    it.yaxis.grid()
    # Display number of sections taught per instructor
    plt.savefig('InstGradeHist.jpg', bbox_inches='tight')

# instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections
def InstGPATrunc(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('GPA W', inplace=True)
    InstTable.drop(InstTable[InstTable['Sections']<5].index, inplace = True)
    InstTable.reset_index()
    InstTable.to_csv('instHistTrunc.csv', encoding='utf-8-sig')
    it = InstTable.plot.hist(x='Instructor', y='GPA W', figsize=(13,3), bins=bins, color='steelblue', legend=False)
    it.set_xlabel("GPA")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(bins, rotation='vertical')
    plt.axis([2.1, 4.0, None, None])
    it.yaxis.grid()
    plt.savefig('InstGPATrunc.jpg', bbox_inches='tight')

# instructor Enrollment Distribution histogram
def InstEnroll(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('Enrollments', inplace=True)
    enrollList = createList(0, 3700, 50)
    it = InstTable.plot.hist(x='Instructor', y='Enrollments', figsize=(
        20, 5), bins=enrollList, color='#4b8745', legend=False)
    it.set_xlabel("Enrollment Range")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['Enrollments'].mean(),
                color='red', linestyle='dashed', linewidth=2)
    plt.xticks(enrollList, rotation='vertical')
    plt.axis([0, 3700, None, None])
    it.yaxis.grid()
    plt.savefig('InstEnrolHist.jpg', bbox_inches='tight')

# instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200
def InstEnrollTrunc(df):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('Enrollments', inplace=True)
    InstTable.drop(InstTable[InstTable['Enrollments']
                   < 200].index, inplace=True)
    InstTable.reset_index()
    InstTable.to_csv('instTableTrunc.csv', encoding='utf-8-sig')
    enrollList = createList(200, 3700, 50)
    it = InstTable.plot.hist(x='Instructor', y='Enrollments', figsize=(
        18, 5), bins=enrollList, color='#f5a142', legend=False)
    it.set_xlabel("Enrollment Range")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['Enrollments'].mean(),
                color='red', linestyle='dashed', linewidth=2)
    plt.xticks(enrollList, rotation='vertical')
    plt.axis([200, 3700, None, None])
    it.yaxis.grid()
    plt.savefig('InstEnrollHistTrunc200.jpg', bbox_inches='tight')

# gpa vs major size (number of enrollments) scatter plot
def MjrGPA(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mj = mjrTable.plot.scatter(
        x='Enrollments', y='GPA W', figsize=(10, 5), color='#3c6e37', s=50)
    mj.set_xlabel("Major Enrollments")
    mj.set_ylabel("Weighted GPA")
    mj.yaxis.grid()
    plt.savefig('MjrAvgScat.jpg', bbox_inches='tight')

# gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments
def MjrGPATrunc(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.drop(mjrTable[mjrTable['Enrollments']
                  < 10000].index, inplace=True)
    mjrTable.reset_index()
    mj = mjrTable.plot.scatter(
        x='Enrollments', y='GPA W', figsize=(10, 5), color='#e08114', s=50)
    mj.set_xlabel("Major Enrollments")
    mj.set_ylabel("Weighted GPA")
    mj.yaxis.grid()
    plt.savefig('MjrAvgScatTrunc.jpg', bbox_inches='tight')

# major vs enrollments bar chart, for majors with > 10,000 enrollments
def MjrEnroll(df):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.sort_values('Enrollments', inplace=True)
    mjrTable.drop(mjrTable[mjrTable['Enrollments']
                  < 10000].index, inplace=True)
    mjrTable.reset_index()
    mj = mjrTable.plot.bar(x='Major', y='Enrollments', figsize=(
        15, 5), color='#f5a142', legend=False)
    mj.set_xlabel("Majors")
    mj.set_ylabel("Enrollments")
    mj.yaxis.grid()
    plt.savefig('MjrEnrolBarTrunc.jpg', bbox_inches='tight')

# distribution of grades bar chart for courses with > 70 sections
#Bar Chart of distribution of Grades for courses with >= 70 sections 
def CourseGPA(df):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)
    crsTable.drop(crsTable[crsTable['Sections']<70].index, inplace = True)
    crsTable.to_csv('crsTableTrunc.csv', encoding='utf-8-sig')
    barsColor = coloring(crsTable)
    ct = crsTable.plot.bar(x='Course', y='GPA W', figsize=(13,5), color=barsColor, legend=False, width=.7)
    ct.set_ylabel("GPA")
    ct.set_xlabel("Courses")
    plt.axhline(crsTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.axis([None, None, 2.6, 3.8])
    colors={'Arts, Humanities, and Language':'#e6ae6e', 'Communication and Social Science':'#94bff7', 'STEM':'#18979e', 'Tutorial':'#ac82f5'}   
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    ct.legend(handles, labels)
    ct.yaxis.grid()
    plt.savefig('Figure4.jpg', bbox_inches='tight')
    bins = createList(2, 4, 0.05)

#Bar Chart of distribution of Grades for courses with > 70 sections Sorted by GPA
def CourseGPAv1(df):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)
    crsTable.drop(crsTable[crsTable['Sections']<70].index, inplace = True)
    crsTable.to_csv('crsTableTrunc.csv', encoding='utf-8-sig')
    barsColor = coloring(crsTable)

    ct = crsTable.plot.bar(x='Course', y='GPA W', figsize=(13,5), color='#18979e', legend=False, width=.7)
    ct.set_ylabel("GPA")
    ct.set_xlabel("Courses")
    plt.axhline(crsTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.axis([None, None, 2.5, 4.0])
    ct.yaxis.grid()
    plt.savefig('gpaCourseBarTrunc.jpg', bbox_inches='tight')

    bins = createList(2, 4, 0.05)

#Bar Chart of distribution of Grades for courses with > 70 sections Sorted by enrollment
def CourseGPAv2(df):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)
    crsTable.drop(crsTable[crsTable['Sections']<70].index, inplace = True)
    crsTable.to_csv('crsTableTrunc.csv', encoding='utf-8-sig')
    barsColor = coloring(crsTable)

    ct = crsTable.plot.bar(x='Course', y='Students', figsize=(13,5), color='#f5a142', legend=False, width=.7)
    ct.set_ylabel("Number of Students")
    ct.set_xlabel("Courses")
    plt.axhline(crsTable['Students'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    ct.yaxis.grid()
    plt.savefig('EnrollCourseBarTrunc.jpg', bbox_inches='tight')

# bar chart that shows number of enrollments and course average grades simultaneously.
def CourseGPAv1v2(df):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)
    crsTable.drop(crsTable[crsTable['Sections']<70].index, inplace = True)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.axis([None, None, 2.5, 4.0])
    ax1.set_ylabel('GPA')
    ax2.set_ylabel('Course Enrollments')
    crsTable.plot.bar(x='Course', y='GPA W', ax=ax1, figsize=(20,5), color='#18979e', width=.7)
    crsTable.plot.bar(x='Course', y='Students', ax=ax2, figsize=(20,5), color='#ffce61', alpha=0.8, width=.7)
    plt.legend(['Students'], loc='best', bbox_to_anchor=(0.9, 0.5, 0, 0.5))
    plt.savefig('CourseGPAEnrollTrunc.jpg', bbox_inches='tight')
        
    corr = np.corrcoef(crsTable['Students'], crsTable['GPA W'])
    print(corr)

#TODO: Maybe merge two loops
#TODO: Print out to a file all the results that are printed out to the terminal
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

    wantGraphs = input(
        "Would you like to generate any other illustration or graph of the data? (yes/no)  ")
    if wantGraphs == 'no':
        Bloop = False

print("\n###############################################################")
print("Thank you for using Fordham's EDM Lab Grading Data Mining Tool!")
print("###############################################################\n")

#TODO: print the complete unique lists out to a file so the user can visit and look at the entire lists
#TODO: print out the some information to the user without any inputs necessary.
#TODO: reword some things so that the tool is more easy to use.
#TODO: make some reorganization so that the tool is more easy to use.
#TODO: Maybe merge two loops
#TODO: Print out to a file all the results that are printed out to the terminal.
#TODO: Each terminal section should be saved into a file name "datetime-log.txt"
#make descriptive names
#TODO: When generating a file, tell the user the name of the file and where it is being saved.

#TODO: In te future --> Make a user interface outside of terminal.

