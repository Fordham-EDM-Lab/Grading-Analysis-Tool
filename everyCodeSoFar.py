#last updated: 08/2022

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned-data-6-17-22.csv')

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

# Compute average grade and standard deviation over all courses
AllCourseMean = df['finGradN'].mean()
stdAllCourse = df['finGradN'].std()

# Compute average grade over all courses (weighted)
def avgWeighted(df, value, weight):
    return (df[weight] * df[value]).sum() / df[weight].sum()

# Compute average grade and standard deviation for all CISC department courses
CISCMean = df.loc[df['ProgCode'] == 'Computer and Info Science', 'finGradN'].mean()
stdCISC = df.loc[df['ProgCode'] == 'Computer and Info Science', 'finGradN'].std()

# Computer average grade and standard deviation for all English department course
EnglishMean = df.loc[df['ProgCode'] == 'English', 'finGradN'].mean()
stdEnglish = df.loc[df['ProgCode'] == 'English', 'finGradN'].std()

# Compute average grade and standard deviation for all CISC majors taking any course
CISCMajorsMean = df.loc[df['major'] == 'COMPUTER SCIENCE', 'finGradN'].mean()
stdCISCMajor = df.loc[df['major'] == 'COMPUTER SCIENCE', 'finGradN'].std()

# Computer average grade and standard deviation for all CISC majors taking CISC department courses
CISCMajorsCoursesMean = df.loc[(df['major'] == 'COMPUTER SCIENCE') & (
    df['ProgCode'] == 'Computer and Info Science'), 'finGradN'].mean()
stdCISCMajorCourses = df.loc[(df['major'] == 'COMPUTER SCIENCE') & (
    df['ProgCode'] == 'Computer and Info Science'), 'finGradN'].std()

# Pick one faculty member that has lots of courses and compute the average GPA over all of their courses, standard deviation, low and high grade.
# Faculty Memeber = F19932
FacultyMean = df.loc[df['facultyID'] == 'F19932', 'finGradN'].mean()
stdFaculty = df.loc[df['facultyID'] == 'F19932', 'finGradN'].std()
facHigh = df.loc[df['facultyID'] == 'F19932', 'finGradN'].max()
facLow = df.loc[df['facultyID'] == 'F19932', 'finGradN'].min()

# Generate a table and maybe histogram of the student grade distribution (F, D, C-, C, … A)
studGradeDistribution = df['finGradC'].value_counts()

# Generate a table and maybe histogram of the professor grade distribution (F, D, C-, C, … A)
profGradeDistribution = df.loc[df['facultyID'] == 'F19932', 'finGradC'].value_counts()

# Extract a list of all unique departments, majors, instructors, courses, CRNs, and Students
uniqueDept = df['ProgCode'].unique()
uniqueMjr = df['major'].unique()
uniqueInst = df['facultyID'].unique()
uniqueCrs = df['crsTitle'].unique()
uniqueCRN = df['CRN'].unique()
uniqueStud = df['SID'].unique()

# Compute the number of enrollments for each and create a table |departments, # of enrollments|
def enrollments(df, classSize):
    return (df[classSize]).sum()


DeptEnroll = df.groupby(df['ProgCode']).apply(enrollments, 'class_size')

# Create a table |major, unique students|
mjrStud = df['major'].value_counts()

# Creates course, major, department, and instructor tables
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

#Trunc: Bar chart for department grades (y=gpa, x=department)  enrollments > 600
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

#Bar chart that shows number of enrollments and department average grades simultaneously. 
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.axis([None, None, 2.5, 4.0])

ax1.set_ylabel('Weighted GPA')
ax2.set_ylabel('Department Enrollments')

DeptTable.plot.bar(x='Department', y='GPA W', ax=ax1, figsize=(20,5), color='#18979e')
DeptTable.plot.bar(x='Department', y='Enrollments', ax=ax2, figsize=(20,5), color='#f5a142', alpha=0.8)
plt.savefig('DeptAvgEnrolTrunc.jpg', bbox_inches='tight')

#Color code dept averages and create a bar graph

#Dept: bar chart dept vs dept size (number of enrollments) enrollments > 600
DeptTable.sort_values('Enrollments', inplace=True)
de = DeptTable.plot.bar(x='Department', y='Enrollments', figsize=(20,5), color='#f5a142', legend=False)

de.yaxis.grid()
de.set_xlabel("Department")
de.set_ylabel("Department Enrollments")
plt.savefig('DeptEnrolBarTrunc.jpg', bbox_inches='tight')

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

bins = createList(2, 4, 0.05)

#Inst: Instructor Grade Distribution (histogram) -- frequency of grades
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

#Scatter plot: total number of students in a department vs. grades in that department enrollments > 600
DeptTable.drop(DeptTable[DeptTable['Enrollments']<600].index, inplace = True)
DeptTable.reset_index()
dt = DeptTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#e08114', s=50)

dt.set_xlabel("Department Enrollments")
dt.set_ylabel("Weighted GPA")
dt.yaxis.grid()
plt.savefig('StudAvgScatTrunc.jpg', bbox_inches='tight')

#Scatter plot: gpa vs major size (number of enrollments) 
mjrTable = pd.read_csv('majorTable.csv')
mj = mjrTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#3c6e37', s=50)

mj.set_xlabel("Major Enrollments")
mj.set_ylabel("Weighted GPA")
mj.yaxis.grid()
plt.savefig('MjrAvgScat.jpg', bbox_inches='tight')

#Trunc: Scatter plot gpa vs major size (number of enrollments) > 10,000 enrollments
mjrTable = pd.read_csv('majorTable.csv')

mjrTable.drop(mjrTable[mjrTable['Enrollments']<10000].index, inplace = True)
mjrTable.reset_index()

mj = mjrTable.plot.scatter(x='Enrollments', y='GPA W', figsize=(10,5), color='#e08114', s=50)

mj.set_xlabel("Major Enrollments")
mj.set_ylabel("Weighted GPA")
mj.yaxis.grid()
plt.savefig('MjrAvgScatTrunc.jpg', bbox_inches='tight')

#Bar chart for Major vs enrollments > 10,000 enrollments
#Total students taking courses in the major
mjrTable = pd.read_csv('majorTable.csv')
mjrTable.sort_values('Enrollments', inplace=True)
mjrTable.drop(mjrTable[mjrTable['Enrollments']<10000].index, inplace = True)
mjrTable.reset_index()

mj = mjrTable.plot.bar(x='Major', y='Enrollments', figsize=(15,5), color='#f5a142', legend=False)

mj.set_xlabel("Majors")
mj.set_ylabel("Enrollments")
mj.yaxis.grid()
plt.savefig('MjrEnrolBarTrunc.jpg', bbox_inches='tight')

#Grade distributions 
it = pd.read_csv('instTable.csv')
ranges = [2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0]

#Number of instructors in each GPA range
instGradeDist = it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count()
  
#Percentage
instPer = ((it['GPA W'].groupby(pd.cut(it['GPA W'], ranges)).count())/ (len(it['GPA W']))) *100

#Bar Chart of distribution of Grades for courses with > 70 sections 
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

bins = createList(2, 4, 0.05)

#Instructor Grade Distribution (histogram) TRUNC (excluding inst teaching < 10 sections) -- frequency of grades
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

#Display number of sections taught per instructor 
plt.savefig('InstGradeHistTrunc.jpg', bbox_inches='tight')

#Inst: Instructor Enrollment Distribution (histogram) -- enrollment range
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

#Trunc: Instructor Enrollment Distribution (histogram) TRUNC (enrollements > 200) -- enrollment range
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

#TODO: mapping courses x majors

#TODO: Course Level Report (courseLevel.csv)
#ct = pd.read_csv('crsTableTrunc.csv')
#with open('courseLevel.csv', 'w', newline='') as csvfile:
    #my_writer = csv.writer(csvfile)
    #my_writer.writerow(['SID', 'Letter Grades', 'Section', 'Faculty'])
    #len_cols = len(df['SID'].unique())
    #for i in range(len_cols):
        #Calculate student Letter Grade in course
            #Calculate each Grade percentage
            #Create bar chart to illustrate
        #Determine section student was in (use CRN)
            #Show grade distribution in each section(x-axis: Section, y-axis: grade, color-code: different grade %)
        #Determine instructor student was taught by (use facultyID)
            #Show grade distribution for each instructor(x-axis: Inst, y-axis: grade, color-code: different grade %)
            #Calculate grade average for each instructor

#TODO: Student Average Table: (studMeanTable.csv)
#with open('studMeanTable.csv', 'w', newline='') as csvfile:
    #my_writer = csv.writer(csvfile)
    #my_writer.writerow(['SID', 'Mean GPA', 'Deviation'])
    #len_cols = len(df['SID'].unique())
    #for i in range(len_cols):
        #Calculate student GPA average over all courses taken
        #def calcMean(df, stud, gpa):
            #avg = df.loc[df['SID'] == stud, gpa].mean()
            #return float("{0:.3f}".format(avg))

        #MeanGpa = calcMean(df, uniqueStud[i], 'finGradN')

        #Calculate student std deviation over all courses taken
        #def calcStd(df, stud, gpa):
            #std = df.loc[df['SID'] == stud, gpa].std()
            #return float("{0:.3f}".format(std))

        #GPAstdDevs = calcMean(df, uniqueStud[i], 'finGradN')
        
        #my_writer.writerow([uniqueStud[i], MeanGpa, GPAstdDevs])
