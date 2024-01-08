from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.completion import WordCompleter
import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
import plotly.express as px
import csv






plt.rcParams.update({'font.size': 14})

# save the data file as df
df = pd.read_csv('filteredData.csv')

# get useful list of all unique departments, majors, instructors, courses, UniqueCourseID, and students
uniqueDept = df['Department'].unique()
uniqueMjr = df['Major'].unique()
uniqueInst = df['FacultyID'].unique()
uniqueCrs = df['CourseTitle'].unique()
uniqueCRSID = df['UniqueCourseID'].unique()
uniqueStud = df['SID'].unique()


#All this is done to make a csv file with all the unique entries appearing in the given dataset. It is
#not used and is only there for refrence purposes.



def save_unique_entries(df, user_directory):
    uniqueDept = df['Department'].unique()
    uniqueMjr = df['Major'].unique()
    uniqueInst = df['FacultyID'].unique()
    uniqueCrs = df['CourseTitle'].unique()
    uniqueCRSID = df['UniqueCourseID'].unique()
    uniqueStud = df['SID'].unique()

    save_path = os.path.join(user_directory, 'unique_entries.csv')


    with open(save_path, 'w', newline='') as f:
        writer = csv.writer(f)

        # Write headers
        writer.writerow(['These values are purely informational and do not correlate between columns.'])
        writer.writerow(['They are the unique values that appear in the dataset for the given column.'])
        writer.writerow(['Departments:', 'Majors:', 'FacultyIDs:', 'CourseTitles:', 'UniqueCourseIDs:', 'SIDs:'])


        max_length = max(len(uniqueDept), len(uniqueMjr), len(uniqueInst), 
                         len(uniqueCrs), len(uniqueCRSID), len(uniqueStud))

        for i in range(max_length):
            row = [
                uniqueDept[i] if i < len(uniqueDept) else '',
                uniqueMjr[i] if i < len(uniqueMjr) else '',
                uniqueInst[i] if i < len(uniqueInst) else '',
                uniqueCrs[i] if i < len(uniqueCrs) else '',
                uniqueCRSID[i] if i < len(uniqueCRSID) else '',
                uniqueStud[i] if i < len(uniqueStud) else ''
            ]
            writer.writerow(row)

        print("\n\nFile Created:", f" {save_path}\n\n")


def drop_values_by_threshold(df, column, min_threshold=None, max_threshold=None):
    if min_threshold is not None:
        df = df[df[column] >= min_threshold]
    if max_threshold is not None:
        df = df[df[column] <= max_threshold]
    return df


def avgWeighted(df, value, weight):
    return (df[weight] * df[value]).sum() / df[weight].sum()

# generate table of student grade distribution of all courses
def AllCoursesGradeDist(df):
    studGradeDistribution = df['FinLetterGrade'].value_counts()
    print("\nStudent Letter Grade Distribution over all courses: ")
    print(studGradeDistribution.to_string(header=False))

# Instructor Grade Distribution table
def GradeDist(df):
    it = pd.read_csv('instTable.csv')
    ranges = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
              3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0]
    # Number of instructors in each GPA range
    instGradeDist = it['GPA W'].groupby(pd.cut(it['GPA W'], ranges), observed=True).count()
    instPer = ((it['GPA W'].groupby(pd.cut(it['GPA W'], ranges), observed=True).count()) / (len(it['GPA W']))) * 100

    
    print("\nStudent Grade Distribution over all instructors: ")
    print(instGradeDist.to_string(header=False))
    print("\nin percentages: ")
    print(round(instPer, 3).to_string(header=False))

# average & std grades of all courses
def UniversityCoursesMean(df):
    print("\nGPA of all courses in the university:", round(avgWeighted(df, 'FinNumericGrade', 'CredHrs'), 3), "\n")
    #print(round(avgWeighted(df, 'FinNumericGrade', 'CredHrs'), 3))
    print("\nStandard Deviation of all courses GPA:", round(df['FinNumericGrade'].std(), 3), "\n")
    #print(round(df['FinNumericGrade'].std(), 3))

#TODO: output the unique lists fully.
# a list of all unique departments, majors, instructors, courses, UniqueCourseID, and students
def unique(df):
    req = input(
        "\nWould you like a list of unique Departments, Majors, Instructor IDs, Courses, UniqueCourseID, or Student IDs?\n")
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
    elif (req == 'UniqueCourseID'):
        print("\nThese are all UniqueCourseID:")
        print(uniqueCRSID)
    elif (req == 'Student IDs'):
        print("\nThese are all Student IDs:")
        print(uniqueStud)
    else:
        print("This is not a valid option.")

# average & std grades of all students taking courses in specific department
def DepartmentCoursesMean(df, dept):
    deptMean = df.loc[df['Department'] == dept, 'FinNumericGrade'].mean()
    stdDept = df.loc[df['Department'] == dept, 'FinNumericGrade'].std()
    print("\n" + dept + " department courses mean grade:", round(deptMean, 3), "\n")
    #print(deptMean)
    print(dept + " department courses grade standard deviation:", round(stdDept, 3), "\n")
    #print(stdDept)

# average & std dev of grades of all students of a specific major (all courses in major department or not)
def MajorDegreeMean(df, major):
    majorMean = df.loc[df['Major'] == major, 'FinNumericGrade'].mean()
    stdMajor = df.loc[df['Major'] == major, 'FinNumericGrade'].std()
    print("\n" + major + " majors mean grade:", round(majorMean, 3), "\n")
    #print(majorMean)
    print(major + " majors grade standard deviation:", round(stdMajor, 3), "\n")
    #print(stdMajor)

# average & std dev of grades of all courses in the specific major's department that students with that specific major take
def MajorDeptMean(df, major, dept):
    DMajorMean = df.loc[(df['Major'] == major) & (
        df['Department'] == dept), 'FinNumericGrade'].mean()
    stdDMajor = df.loc[(df['Major'] == major) & (
        df['Department'] == dept), 'FinNumericGrade'].std()
    print("\n" + major + " majors mean grade in its department courses:", round(DMajorMean, 3), "\n")
    #print(DMajorMean)
    print(major + " majors grade standard deviation in its department courses:", round(stdDMajor, 3), "\n")
    #print(stdDMajor)

# average GPA, std dev, lowest and highest grades of a specific faculty.
def FacultyAnalysis(df, fac):
    FacMean = df.loc[df['FacultyID'] == fac, 'FinNumericGrade'].mean()
    stdFac = df.loc[df['FacultyID'] == fac, 'FinNumericGrade'].std()
    facLow = df.loc[df['FacultyID'] == fac, 'FinNumericGrade'].min()
    facHigh = df.loc[df['FacultyID'] == fac, 'FinNumericGrade'].max()
    print("\n" + fac + " Faculty Analysis.")
    print("Instructor's GPA:", round(FacMean, 3), "\n")
    #print(FacMean)
    print("Student's std. dev. grades:", round(stdFac, 3), "\n")
    #print(stdFac)
    print("Lowest and highest grades assigned - Lowest:", round(facLow, 3), " Highest:", round(facHigh, 3), "\n")
    # print(facLow)
    # print(facHigh)

# Compute the number of enrollments using class size
def enrollments(df, classSize):
    return round((df[classSize]).sum(), 3)

# Create a table with number of enrollments per department
def DeptEnroll(df):
    print("\nNumber of enrollments per university department: ")
    print(df.groupby(df['Department']).apply(enrollments, 'ClassSize').to_string(header=False))

# Create a table |major, # of unique students|
def StudMjrCount(df):
    print("\nNumber of unique students enrolled in a major: ")
    print(df['Major'].value_counts().to_string(header=False))

# If someone inputs an incomplete name, check to see if it's possible it is a substring of an existing item
def checkMultiple(og, ogList):
    checkList = np.array([])
    for check in ogList:
        if og in check:
            checkList.append(check)
    
    if len(checkList) > 1:
        print("\nWhat you entered is valid for the following items: " + " ")
        print(checkList)
        new_value = input("Enter the specific name for what you are attempting to write down: \n")
        return new_value
    elif len(checkList) == 1:
        return checkList[0]
    elif len(checkList) == 0:
        print("\nThis is an invalid item. If you need to see a list of valid instructors, type UniqueList.")
        return og


# RESEARCH CODE:
# Function to create a list of consecutive numbers spaced out as needed (to use when creating bins for a graph)
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
    


def DeptGPA(user_directory, min_enrollments = None, max_enrollments = None):   
    DeptTable = pd.read_csv('deptTable.csv') 

    DeptTable = drop_values_by_threshold(DeptTable, 'Enrollments', min_enrollments, max_enrollments)

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
    save_path = os.path.join(user_directory, 'Figure2.3.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")

    plt.savefig(save_path, bbox_inches='tight')

# department size bar chart (y=enrollments, x=department) for departments with enrollments > 600
def DeptSize(user_directory,  min_enrollments = None, max_enrollments = None):
    DeptTable = pd.read_csv('deptTable.csv')

    DeptTable = drop_values_by_threshold(DeptTable, 'Enrollments', min_enrollments, max_enrollments)

    DeptTable.sort_values('Enrollments', inplace=True)
    de = DeptTable.plot.bar(x='Department', y='Enrollments', figsize=(
        20, 5), color='#f5a142', legend=False)
    de.yaxis.grid()
    de.set_xlabel("Department")
    de.set_ylabel("Department Enrollments")
    plt.axhline(DeptTable['Enrollments'].mean(),
                color='red', linestyle='dashed', linewidth=2)
    save_path = os.path.join(user_directory, 'DeptEnrolBarTrunc.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")
    plt.savefig(save_path, bbox_inches='tight')

# bar chart that shows number of enrollments and department average grades simultaneously.
def DeptEnrollGPA(user_directory, min_enrollments = None, max_enrollments = None):
    DeptTable = pd.read_csv('deptTable.csv')

    DeptTable = drop_values_by_threshold(DeptTable, 'Enrollments', min_enrollments, max_enrollments)

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
    save_path = os.path.join(user_directory, 'DeptAvgEnrolTrunc.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")
    plt.savefig(save_path, bbox_inches='tight')

    corr = np.corrcoef(DeptTable['Enrollments'], DeptTable['GPA W'])
    print("\nCorrelation Coefficient between Enrollments and GPA:", corr)
    

#Scatter plot: total number of students in a department vs. grades in that department enrollments > 600
def DeptStudGPA(user_directory, min_enrollments = None, max_enrollments = None):
    DeptTable = pd.read_csv('deptTable.csv')
    
    DeptTable = drop_values_by_threshold(DeptTable, 'Enrollments', min_enrollments, max_enrollments)


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
    save_path = os.path.join(user_directory, 'Figure3.2.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")
    plt.savefig(save_path, bbox_inches='tight')


bins = createList(2, 4, 0.05)


# instructor Grade Distribution histogram -- frequency of grades, excluding inst teaching < 10 sections
def InstGPATrunc(df, user_directory, min_sections = None, max_sections = None, csv=False):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('GPA W', inplace=True)

    InstTable = drop_values_by_threshold(InstTable, 'Sections' , min_sections, max_sections)

    InstTable.reset_index()
    if csv:
        save_path = os.path.join(user_directory, 'instTableGPAVsInst.csv')
        print("\n\nFile Created:", f" {save_path}\n\n")

        InstTable.to_csv(save_path, encoding='utf-8-sig')

    it = InstTable.plot.hist(x='Instructor', y='GPA W', figsize=(13,3), bins=bins, color='steelblue', legend=False)
    it.set_xlabel("Weighted GPA")
    it.set_ylabel("Number of Instructors")
    plt.axvline(InstTable['GPA W'].mean(), color='red', linestyle = 'dashed', linewidth=2)
    plt.xticks(bins, rotation='vertical')
    plt.axis([2.1, 4.0, None, None])
    it.yaxis.grid()
    save_path = os.path.join(user_directory, 'InstGPATrunc.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")

    plt.savefig(save_path, bbox_inches='tight')

# instructor Enrollment Distribution histogram for instructors with the number of students taught(enrollements) > 200
def InstEnrollTrunc(df, user_directory, min_enrollments = None, max_enrollments = None, csv=False):
    InstTable = pd.read_csv('instTable.csv')
    InstTable.sort_values('Enrollments', inplace=True)
    
    InstTable = drop_values_by_threshold(InstTable, 'Enrollments' , min_enrollments, max_enrollments)


    InstTable.reset_index()

    if csv:
        save_path = os.path.join(user_directory, 'instTableEnrollVsInst.csv')
        print("\n\nFile Created:", f" {save_path}\n\n")
        InstTable.to_csv(save_path, encoding='utf-8-sig')

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
    save_path = os.path.join(user_directory, 'InstEnrollHistTrunc200.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")

    plt.savefig(save_path, bbox_inches='tight')



# gpa vs major size (number of enrollments) scatter plot for majors with > 10,000 enrollments
def MjrGPATrunc(df, user_directory, min_enrollments = None, max_enrollments = None, csv = False):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.sort_values('Enrollments', inplace=True)
    
    mjrTable = drop_values_by_threshold(mjrTable, 'Enrollments', min_enrollments, max_enrollments)

    if csv:
        save_path = os.path.join(user_directory, 'mjrvsmjrsize.csv')
        print("\n\nFile Created:", f" {save_path}\n\n")
        mjrTable.to_csv(save_path, encoding='utf-8-sig')


    mjrTable.reset_index()
    mj = mjrTable.plot.scatter(
        x='Enrollments', y='GPA W', figsize=(10, 5), color='#e08114', s=50)
    mj.set_xlabel("Major Enrollments")
    mj.set_ylabel("Weighted GPA")
    mj.yaxis.grid()
    save_path = os.path.join(user_directory, 'MjrAvgScatTrunc.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")

    plt.savefig(save_path, bbox_inches='tight')

# major vs enrollments bar chart, for majors with > 10,000 enrollments
def MjrEnroll(df, user_directory, min_enrollments = None, max_enrollments = None, csv = False):
    mjrTable = pd.read_csv('majorTable.csv')
    mjrTable.sort_values('Enrollments', inplace=True)
    
    mjrTable = drop_values_by_threshold(mjrTable, 'Enrollments', min_enrollments, max_enrollments)

    if csv:
        save_path = os.path.join(user_directory, 'mjrvsenroll.csv')
        print("\n\nFile Created:", f" {save_path}\n\n")
        mjrTable.to_csv(save_path, encoding='utf-8-sig')

    mjrTable.reset_index()
    mj = mjrTable.plot.bar(x='Major', y='Enrollments', figsize=(
        15, 5), color='#f5a142', legend=False)
    mj.set_xlabel("Majors")
    mj.set_ylabel("Enrollments")
    mj.yaxis.grid()
    save_path = os.path.join(user_directory, 'MjrEnrolBarTrunc.jpg')
    print("\n\nFile Created:", f" {save_path}\n\n")

    plt.savefig(save_path, bbox_inches='tight')


def CourseGPA(df, user_directory, min_enrollments=None, max_enrollments=None, min_sections=None, max_sections=None, csv=False, useGPA=False, useEnrollments=False):
    crsTable = pd.read_csv('courseTable.csv')
    crsTable.sort_values('GPA W', inplace=True)


    def plot_and_save(df, x, y, color, ylabel, title, filename, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(15, 6))
        ax.set_title(title, fontsize=16)
        ax.set_xlabel('Courses', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        save_path = os.path.join(user_directory, filename)
        plt.savefig(save_path, bbox_inches='tight')
        print("\n\nFile Created:", f" {save_path}\n\n")

    if useGPA and not useEnrollments:
        crsTable = drop_values_by_threshold(crsTable, 'Sections', min_sections, max_sections)
        plot_and_save(crsTable, 'Course', 'GPA W', 'viridis', 'GPA', 'GPA Analysis per Course', 'gpaCourseBarTrunc.jpg')

    if useEnrollments and not useGPA:
        crsTable = drop_values_by_threshold(crsTable, 'Enrollments', min_enrollments, max_enrollments)
        plot_and_save(crsTable, 'Course', 'Students', 'rocket', 'Number of Students', 'Enrollment Analysis per Course', 'EnrollCourseBarTrunc.jpg')
    
    if useEnrollments and useGPA:
        crsTable = drop_values_by_threshold(crsTable, 'Enrollments', min_enrollments, max_enrollments)
        crsTable = drop_values_by_threshold(crsTable, 'Sections', min_sections, max_sections)
        plot_and_save(crsTable, 'Course', 'GPA W', 'viridis', 'GPA', 'GPA Analysis per Course', 'gpaCourseBarTrunc.jpg')

    if csv:
        save_path = os.path.join(user_directory, 'crsTableTrunc.csv')
        crsTable.to_csv(save_path, encoding='utf-8-sig')
        print("\n\nFile Created:", f" {save_path}\n\n")



## Should we use enrollment threshold for class size?


def Level_Inflation(df, user_directory, show_plot = False, csv = False, min_enrollments=None, max_enrollments=None):

    df = drop_values_by_threshold(df, 'ClassSize', min_enrollments, max_enrollments)

    df['CombinedStudentLevel'] = df['StudentLevel'].apply(lambda x: 'Freshman' if x in ['Continuing Freshman', 'First-Time Freshman'] else x)
    gpa = df.groupby('CombinedStudentLevel')['FinNumericGrade'].mean().reset_index()
    gpa.rename(columns={'FinNumericGrade':'Average GPA'}, inplace=True)
    gpa.rename(columns={'CombinedStudentLevel':'Student Level'}, inplace=True)

    ## Custom Sort Student Levels
    level = ['Unclassified', 'Freshman', 'Sophomores', 'Juniors', 'Seniors', 'Graduate Students']
    gpa['Student Level'] = pd.Categorical(gpa['Student Level'], categories=level)
    gpa.sort_values(by = 'Student Level', inplace=True)
    gpa.reset_index(drop=True, inplace=True)

    print(gpa)
    print("")
    
    gpa.plot(x='Student Level', y = 'Average GPA', kind='line', marker='o', color='b', linestyle='-')
    plt.xlabel('Student Level')
    plt.ylabel('Average GPA')
    plt.title('Level Trends')
    plt.grid(True)

    if show_plot:
        fig = px.line(gpa, x='Student Level', y='Average GPA', markers=True, title='GPA vs Class Level')
        fig.update_traces(textposition='top center')
        fig.update_layout(hovermode='closest')

        # Show the interactive plot
        fig.show()

    # Saving the plot as a PDF using matplotlib
    gpa.plot(x='Student Level', y='Average GPA', kind='line', marker='o', color='b', linestyle='-')
    plt.xlabel('Student Level')
    plt.ylabel('Average GPA')
    plt.title('Level Trends')
    plt.grid(True)
    
    pdf_filename = 'output.pdf'
    save_path = os.path.join(user_directory, pdf_filename)

    with PdfPages(save_path) as pdf:
        plt.xticks(rotation = 45)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print("\n\nFile Created:", f" {save_path}\n\n")
    
    if csv:
        save_path = os.path.join(user_directory, 'lvlInflation.csv')
        gpa.to_csv(save_path, encoding='utf-8-sig')
        print("\n\nFile Created:", f" {save_path}\n\n")


def sort_values(value):
    if value >= 1000 and value <2000:
        return '1000'
    elif value >= 2000 and value < 3000:
        return '2000'
    elif value >= 3000 and value < 4000:
        return '3000'
    elif value >= 4000:
        return '4000'
    elif value <= 1000:
        return "Beginner"


def CourseLevelGrade(df, user_directory, heatmap = False, min_enrollments = None, max_enrollments = None ,csv = False):

    df = drop_values_by_threshold(df, 'ClassSize', min_enrollments, max_enrollments)

    df['CombinedStudentLevel'] = df['StudentLevel'].apply(lambda x: 'Freshman' if x in ['Continuing Freshman', 'First-Time Freshman'] else x)

    df['Course Level'] = df ['CourseNum'].apply(sort_values)
    
    gpa = df[~(df['Course Level'] == 'Beginner')].groupby(['CombinedStudentLevel', 'Course Level'])['FinNumericGrade'].mean().reset_index()
    gpa.rename(columns={'FinNumericGrade':'Average GPA'}, inplace=True)
    gpa.rename(columns={'CombinedStudentLevel':'Student Level'}, inplace=True)
    
    gpa['Average GPA'] = gpa['Average GPA'].round(3)
    
    ## Custom Sort Student Levels
    level = ['Unclassified', 'Freshman', 'Sophomores', 'Juniors', 'Seniors', 'Graduate Students']
    gpa['Student Level'] = pd.Categorical(gpa['Student Level'], categories=level)
    gpa.sort_values(by =['Student Level', 'Course Level'], inplace=True)
    gpa.reset_index(drop=True, inplace=True)
    
    print(gpa)
    print("")
    
    pivot = np.round(pd.pivot_table(gpa, index= 'Student Level', columns='Course Level', values='Average GPA', aggfunc='mean', margins=True, margins_name='Total'),3)    

    if heatmap:
        heatmap = pivot
        heatmap = heatmap.drop('Total', axis=0)
        heatmap = heatmap.drop('Total', axis=1)


        data_for_heatmap = heatmap.to_numpy()

        fig, ax = plt.subplots(figsize=(10, 8))

        cax = ax.imshow(data_for_heatmap, cmap='coolwarm', interpolation='nearest')
        fig.colorbar(cax)
        ax.set_xticks(np.arange(len(heatmap.columns)))
        ax.set_yticks(np.arange(len(heatmap.index)))
        ax.set_xticklabels(heatmap.columns)
        ax.set_yticklabels(heatmap.index)
        plt.xticks(rotation=45)
        ax.set_xlabel('Course Level')
        ax.set_ylabel('Student Level')
        ax.set_title('GPA Heatmap: Student Level vs Course Level')

        plt.savefig(f'{user_directory}/heatmap.pdf', bbox_inches='tight')

        save_path = os.path.join(user_directory, 'heatmap.pdf')
        print("\n\nFile Created:", f" {save_path}\n\n")
        

    pdf_filename = 'pivot.pdf'
    save_path = os.path.join(user_directory, pdf_filename)


    with PdfPages(save_path) as pdf:
        fig, ax = plt.subplots(figsize=(8,6))
        ax.axis('off')
        ax.table(cellText=pivot.values, rowLabels=pivot.index, colLabels=pivot.columns, loc='center')
        plt.title('Pivot Table')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    save_path = os.path.join(user_directory, pdf_filename)
    print("\n\nFile Created:", f" {save_path}\n\n")

    if csv:
        save_path = os.path.join(user_directory, 'courseLevelGrade.csv')
        gpa.to_csv(save_path, encoding='utf-8-sig')
        print("\n\nFile Created:", f" {save_path}\n\n")
