#STEP 1: Data Cleaning tool for Fordham Undergraduate csv Data.

import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from dataclasses import dataclass, field


# save the data file as df
df = pd.read_csv('grading-data-6-17-22.csv')

@dataclass
class BannerTerm:
    year: int
    term: str
    fullterm: int = field(init=False)

    term_map = {
        'Fall': 10,
        'Spring': 15,
        'Winter': 20,
        'Summer': 30
    }

    def __post_init__(self):
        if self.term not in self.term_map:
            raise ValueError(f"Invalid term '{self.term}'")
        self.fullterm = int(f"{self.year}{self.term_map[self.term]}")


def fix_gradterm(grad_term):
    if pd.isna(grad_term):
        return ''
    else:
        return str(int(grad_term))

def grade_string(row):
    row['finGradC'] = str(row['finGradC']).upper()
    return row


def get_fullterm(row):
    banner_term = BannerTerm(year=int(row['year']), term=row['sem'])
    return banner_term.fullterm


def dataCleanup(df):
    # Data Cleaning - splitting sem/year, dropping Administrative depts, creating a new CRN, and creating "CourseCode" joining the ProgCode with NumCode
    df.replace(" ", np.nan, inplace=True)
    df['finGradN'] = df['finGradN'].astype('float')

    df.drop(df[df['ProgCode'] == 'Administrative CBA'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Administrative FCRH'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Honors Program - FCLS'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Honors Program - FCRH'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Honors Program - FCLC'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Graduate Course Credit'].index, inplace=True)
    df.drop(df[df['ProgCode'] == 'Graduate Course Credit'].index, inplace=True)

    df = df.reset_index()

#     # Making Department Names shorter
#     df['ProgCode'].replace(['Theatre', 'Visual Arts', 'Music', 'Comm and Media Studies', 'Dance',
#                             'Mathematics', 'Anthropology', 'Natural Science', 'Sociology',
#                             'Environmental Science', 'Art History', 'Irish Studies', 'Chemistry',
#                             'Theology', 'Social Work (undergraduate)', 'African & African Amer Studies',
#                             'History', 'English', 'Spanish', 'Political Science', 'Interdisciplinary',
#                             'Economics', 'Psychology', 'Biological Sciences',
#                             'Classical Lang & Civilization', 'French', 'Independent Study', 'Philosophy',
#                             'Italian', 'Physics', 'American Catholic Studies',
#                             'Computer and Info Science', 'Humanitarian Affairs', 'Humanitarian Studies',
#                             'Latin', 'Greek', 'Peace and Justice Studies',
#                             'Communication & Culture', 'New Media & Digital Design',
#                             'Digital Tech & Emerging Media', 'Integrative Neuroscience',
#                             'Medieval Studies', 'Film & Television', 'Center for Ethics Education',
#                             'Journalism', 'Latin Amer and Latino Studies', 'Mandarin Chinese',
#                             'Symposium', 'Modern Languages', 'Women, Gender, & Sexuality St',
#                             'Comparative Literature', 'American Studies', "Women's Studies",
#                             'Middle East Studies', 'International Studies', 'Urban Studies',
#                             'Environmental Policy', 'GSB Management', 'Environmental Studies', 'Juilliard Exchange',
#                             'German', 'Japanese', 'GSB Marketing', 'Russian', 'Arabic',
#                             'GSB Information Systems', 'Linguistics', 'HEBW'], ['Theatre', 'Visual Arts', 'Music', 'Comm & Media Stud.', 'Dance',
#  'Math', 'Anthropology', 'Natural Sci.', 'Sociology',
#  'Env. Science', 'Art History', 'Irish Stud.', 'Chemistry',
#  'Theology', 'Social Work', 'Afr. & Afr. Amer Stud.',
#  'History', 'English', 'Spanish', 'Political Sci.', 'Interdisc.',
#  'Economics', 'Psychology', 'Biological Sci.',
#  'Classic Lang & Civ.', 'French', 'Independent Stud.', 'Philosophy',
#  'Italian', 'Physics', 'Amer Catholic Stud.',
#  'Comp & Info Sci.', 'Human. Affairs', 'Human. Stud.',
#  'Latin', 'Greek', 'Peace&Justice Stud.',
#  'Comm. & Culture', 'New Media/Dig. Dsgn',
#  'Digital Tech/Media', 'Integ. Neuroscience',
#  'Medieval Stud.', 'Film & Television', 'Ethics Educ.',
#  'Journalism', 'Latin Amer&Latino Stud.', 'Mandarin Chinese',
#  'Symposium', 'Modern Languages', 'WG&S Stud.',
#  'Comparative Lit.', 'American Stud.', "Women's Stud.",
#  'Middle East Stud.', 'International Stud.', 'Urban Stud.',
#  'Environmental Policy', 'Management', 'Environmental Stud.', 'Juilliard Exc.',
#  'German', 'Japanese', 'Marketing', 'Russian', 'Arabic',
#  'Info Systems', 'Linguistics', 'HEBW'], inplace=True)

#     # Making Major Names shorter
#     df['major'].replace(['DANCE', 'ANTHROPOLOGY', 'ART HISTORY', 'Visual Arts', 'Sociology',
#                          'Theatre', 'Psychology', 'Environmental Science', 'English', 'COMMUNICATIONS',
#                          'AMERICAN STUDIES', 'History', 'CLASSICAL LANG', 'BIOLOGICAL SCI',
#                          'FRENCH LANG & LIT', 'POLITICAL SCIENCE', 'International Studies',
#                          'BUSINESS ADMIN', 'GENERAL SCIENCE', 'PHILOSOPHY', 'Economics',
#                          'NATURAL SCI/INTERDISC', 'COMPUTER SCIENCE', 'Individualized Major',
#                          'SOCIAL SCIENCE', 'NSCI', 'Social Work', 'ITALIAN',
#                          'International Political Economy', 'Chemistry', 'MEDIEVAL STUDIES', 'MUSIC',
#                          'MIDDLE EAST STUDIES', 'THEOLOGY RELIG STUDIES', 'Mathematics',
#                          'URBAN STUDIES', 'FINANCE', 'INTERDISC MATH & ECON', 'Environmental Policy',
#                          'LATIN AMERICAN AND LATINO STUDIES', 'Public Accountancy',
#                          'AFRO-AMER STUDIES', 'PHYSICS', 'Organizational Leadership',
#                          'RELIGIOUS STUDIES', 'MARKETING', 'INFORMATION SCIENCE', 'PUAC',
#                          'Applied Accounting and Finance', 'CLASSICAL CIVILIZ', 'COMPERATIVE LIT',
#                          "WOMEN'S STUDIES", 'HUST', 'NEUR', 'JOUR', 'FRENCH STUDIES', 'ACCOUNTING',
#                          'SPANISH LANG & LIT', 'Engineering Physics',
#                          'Mgmt of Info and Communication Systems', 'Accounting Info Services',
#                          'Business', 'ENST', 'ITALIAN STUDIES', 'Information Systems', 'NMDD', 'COMC',
#                          'GLBU', 'DTEM', 'INTS', 'MTCS', 'FITV', 'SPANISH STUDIES', 'GERMAN',
#                          'Legal & Policy Studies', 'PSNM', 'COMPU SYS/MGMT APP', 'MEDIA STUDIES',
#                          'GERMAN STUDIES', 'Childhood Inclusive Education',
#                          'Organizational Leadership-Westchester'], ['Dance', 'Anthropology', 'Art History', 'Visual Arts', 'Sociology',
#  'Theatre', 'Psychology', 'Env. Sciences', 'English', 'Comm.',
#  'American Stud.', 'History', 'Classical Lang.', 'Biological Sci.',
#  'French Lang & Lit.', 'Political Sci.', 'International Stud.',
#  'Business Adm.', 'General Sci.', 'Philosophy', 'Economics',
#  'Natural Sci.', 'Computer Sci.', 'Indv. Major',
#  'Social Sci.', 'NSCI', 'Social Work', 'Italian',
#  'Int. Political Econ', 'Chemistry', 'Medieval Stud.', 'Music',
#  'Middle East Stud.', 'Theology Stud.', 'Math',
#  'Urban Stud.', 'Finance', 'Interdisc. Math & Econ', 'Env. Policy',
#  'Latin & Latino Amer. Stud.', 'Public Acc.',
#  'Afro-Amer. Stud.', 'Physics', 'Org. Leadership',
#  'Religious Stud.', 'Marketing', 'Info Science', 'Professional & Cont. Stud.',
#  'Applied Acc. and Finance', 'Classical Civiliz.', 'Comp. Lit.',
#  "Women's Stud.", 'Humanitarian Stud.', 'Int. Neuroscience', 'Journalism', 'French Stud.', 'Accounting',
#  'Spanish Lang. & Lit.', 'Eng. Physics',
#  'Info and Comm. Sys. Mgmt.', 'Acc. Info Services',
#  'Business', 'Env. Stud.', 'Italian Stud.', 'Info. Systems', 'NMDD', 'Comm. & Culture',
#  'GLBU', 'DTEM', 'International Stud.', 'Math & Comp. Sci.', 'Film & TV', 'Spanish Stud.', 'German',
#  'Legal & Policy Stud.', 'PSNM', 'Comp. Syst./Mgmt App', 'Media Stud.',
#  'German Studies', 'Childhood Inclusive Education',
#  'Org. Leadership-Westchester'], inplace=True)
    
#      #clean courses:
#     #Making Course Names Shorter
#     df['crsTitle'].replace(['GENERAL CHEM LAB I', 'CALCULUS I', 'FINITE MATHEMATICS', 'INTRMEDIATE SPANISH I', 'BASIC MACROECONOMICS', 'MATH FOR BUSINESS: CALCULUS', 'MUSIC HISTORY INTRO', 'PHIL OF HUMAN NATURE', 'FAITH & CRITICAL REASON', 'BASIC MICROECONOMICS', 'COMPUTER SCIENCE I', 'UNDRSTND HIST CHNGE: MOD EUR', 'COMPOSITION I', 'INTERMEDIATE FRENCH I', 'INTERMEDIATE SPANISH II', 'UNDRSTND HIST CHNGE: AMER HIST', 'STATISTICS', 'MATH FOR BUSINESS: FINITE', 'PHILOSOPHY OF HUMAN NATURE', 'SPANISH LANG & LITERATURE', 'PHILOSOPHICAL ETHICS', 'FAITH AND CRITICAL REASON', 'INTRO TO POLITICS', 'STATISTICS I', 'COMPOSITION II', 'INTRODUCTION TO SOCIOLOGY', 'INVITATION TO THEATRE', 'TEXTS AND CONTEXTS', 'TEXTS & CONTEXTS', 'PHYSICS II LAB', 'TUTORIAL'],['GenChem Lab I', 'Calculus I', 'Finite Math', 'Intermed. Spanish I', 'Basic MacroEcon', 'BusinessMath: Calculus', 'Music Hist Intro', 'Phil of Human Nature', 'Faith & Critical Reason', 'Basic MicroEcon', 'Comp. Sci. I', 'UHC: Modrn Europe', 'Comp. I', 'Intermed. French I', 'Intermed. Spanish II', 'UHC: Amer Hist', 'Stats I', 'Business Math: Finite', 'Phil of Human Nature', 'Spaish Lang & Lit', 'Phil Ethics', 'Faith & Citical Reason', 'Intro to Politics', 'Stats I', 'Comp II', 'Intro to Sociology', 'Inv. to theatre', 'Texts and Contexts', 'Texts & Contexts', 'Physics II Lab', 'Tutorial'], inplace=True)

    # creates a new CRN: CRN + last two digits of year + one digit based on semester
    # e.g. oldCRN 11135, Summer 2010 course -> CRN: 11135102
    df[['sem', 'year']] = df['term'].str.split(' ', expand=True)

    df['year'] = df['year'].astype('int')
    df['Semester'] = df.apply(get_fullterm, axis=1)


    df.loc[df['sem'] == 'Summer', 'sem'] = '0'
    df.loc[df['sem'] == 'Spring', 'sem'] = '1'
    df.loc[df['sem'] == 'Fall', 'sem'] = '2'
    df['sem'] = df['sem'].astype('int')

    df.rename(columns={'CRN': 'oldCRN'}, inplace=True)


    df['oldCRN'] = df['oldCRN'].astype(str)
    df['year'] = df['year'].astype(str)
    df['CRN'] = df['oldCRN'] + df['year'].str[-2:] + df['sem'].astype(str)

    # creating "CourseCode" joining the ProgCode with NumCode
    df['NumCode'] = df['NumCode'].fillna(0)
    df['NumCode'] = df['NumCode'].astype(int)
    df['CourseCode'] = df['ProgCode'].astype(str) + ' ' + df['NumCode'].astype(str)


    df.apply(grade_string, axis=1)

# Rename columns
    rename_map = {
        'finGradN': 'FinNumericGrade',
        'finGradC': 'FinLetterGrade',
        'major': 'Major',
        'ProgCode': 'Department',
        'crsTitle': 'CourseTitle',
        'CRN': 'UniqueCourseID',
        'credHrs': 'CredHrs',
        'facultyID': 'FacultyID',
        'NumCode': 'CourseNum'
    }
    df.rename(columns=rename_map, inplace=True)

    # Verify column existence before applying string operations

    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop('index', inplace=True, axis=1)
    df.drop('sem', inplace=True, axis=1)
    df.drop('year', inplace=True, axis=1)
    df.drop('oldCRN', inplace=True, axis=1)
    df.drop('STU_DegreeSeek', inplace=True, axis=1)
    df.drop('schedType', inplace=True, axis=1)
    df.drop('campus', inplace=True, axis=1)
    df.drop('GradTerm', inplace=True, axis=1)

    return df



# perform necessary data cleanup
df = dataCleanup(df)

#save cleaned files into dataframe
df.to_csv('data-processed-ready.csv', index=False)