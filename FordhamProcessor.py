#STEP 1: Data Cleaning tool for Fordham Undergraduate csv Data.

import string
from timeit import repeat
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from dataclasses import dataclass, field
import sys
sys.path.append("/home/mariom/Work/EDMLab/Grading-Analysis-Tool")
import gradeAnalysisFunc as gaf


# save the data file as df
df = pd.read_csv('raw-data-11-15-24.csv')

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

def filter_dataframe(
    df: pd.DataFrame,
    min_threshold: int,
    max_threshold: int,
    column: str,
    filter_col: str,
):
    agg_df = gaf.pandas_df_agg(df, column)
    agg_df = gaf.drop_courses_by_threshold(
        agg_df, filter_col, min_threshold, max_threshold
    )
    index_list = list(agg_df[column])
    ret_df = drop_rows_given_list(df, column, index_list)
    return ret_df

def drop_rows_given_list(df: pd.DataFrame, column: str, index: list) -> pd.DataFrame:
    df = df[~df[column].isin(index)]
    return df


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
        'STU_ulevel': 'StudentLevel',
        'class_size': 'ClassSize',
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


    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FAITH AND CRITICAL REASON' if x == 'FAITH & CRITICAL REASON' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FREEDOM AND RESPONSIBILITY' if x in ['FREEDOM & RESPONSIBILITY (EP4)',
                                                        'FREEDOM & RESPONSIBILITY'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Philosophy 4484' if x == 'Philosophy 3184' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FRENCH LANGUAGE AND LITERATURE' if x == 'FRENCH LANGUAGE AND LITERATUR' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FROM ROCK-N-ROLL TO HIP-HOP' if x == 'FROM ROCK & ROLL TO HIP HOP' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENDER, BODIES, SEXUALITY' if x == 'GENDER, BODIES, AND SEXUALITY' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Sociology 3400' if x == 'Sociology 4400' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENDER, CRIME, JUSTICE' if x == 'GENDER, CRIME, AND JUSTICE' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENDER, POWER & JUSTICE' if x == 'GENDER, POWER, & JUSTICE' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Philosophy 4407' if x == 'Philosophy 3107' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENDER, RACE, CLASS' if x == 'GENDER, RACE, AND CLASS' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENETICS WITHOUT LAB' if x == 'GENETICS W/O LAB' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GLOBAL CONFLICT: WARS/RELIGION' if x == 'GLOBAL CONFL: WARS/RELIGION' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GLOBAL ENVIRONMENT AND JUSTICE' if x == 'GLOBAL ENVIRONMENT & JUSTICE' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'HINDU LITERATURE AND ETHICS' if x == 'HINDU LIT & ETHICS' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'HISPANICS IN THE USA' if x == 'HISPANICS/LATINOS IN THE USA' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'HISTORY OF ENGLISH LANGUAGE' if x == 'HISTORY OF ENG LANG' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'HUMAN FUNCTION AND DYSFUNCTION' if x == 'HUMAN FUNCTION & DYSFUNCTION' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'IMMUNOLOGY' if x in ['IMMUNOLOGY LECTURE', 'IMMUNOLOGY WITHOUT LAB', 'IMMUNOLOGY LAB'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Natural Science 2022' if x in ['Natural Science 2822', 'Natural Science 2122',
                                                  'Natural Science 2012'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INDEPENDENT STUDY' if x in ['INDEPENDENT STUDY (1-4 CREDITS', 'INDEPENDENT STUDY CHOREOGRAPHY',
                                               'INDEPENDENT STUDY-ORGANIC CHEM'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INFANT AND CHILD DEVELOPMENT' if x == 'INFANT & CHILD DEVELOPMENT' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INFANT&CHILD DEV CONTEXT;PROG' if x == 'INFANT&CHILD DEV CONTEXT;PROGS' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTERNATIONAL ECONOMICS' if x == 'INTERNATIONAL ECONOMIC POLICY' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Economics 3346' if x == 'Economics 3244' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MEN AND MASCULINITIES' if x == 'MEN & MASCULINITIES' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MINDS, MACHINES, AND SOCIETY' if x in ['MINDS MACHINES & SOCIETY (EP4)',
                                                          'MINDS MACHINES & SOCIETY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MODERN DRAMA AS MORAL CRUCIBLE' if x == 'MODERN DRAMA-MORAL CRUCIBLE' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'English 4149' if x == 'English 3531' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MONEY AND BANKING' if x == 'MONEY & BANKING' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MULTIVARIABLE CALCULUS II' if x == 'MULTIVARIATE CALCULUS II' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MUSIC HISTORY INTRODUCTION' if x == 'MUSIC HISTORY INTRO' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MUSICAL THEATRE INTENSIVE' if x == 'MUSICAL THEATRE WORKSHOP' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Theatre 3066' if x == 'Theatre 3065' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'N. AMERICAN ENVIRONMENTAL HIST' if x == 'N. AMERICAN ENVIRONMENTAL HIS' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'NETWORK AND CLIENT SERVER' if x == 'NETWORK & CLIENT SERVER' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'NEW WAVE IMMIGRANT FICTION' if x in ['NEW WAVE IMMIGRAT FICTION',
                                                        'NEW WAVE IMMIGRANT LITERATURE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ORGANIC CHEMISTRY LAB I' if x in ['ORGANIC LAB I FOR CHEM MAJORS', 'ORGANIC LABORATORY I'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Chemistry 2541' if x == 'Chemistry 2531' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ORGANIC CHEMISTRY LAB II' if x in ['ORGANIC LAB II FOR CHEM MAJORS', 'ORGANIC LABORATORY II'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Chemistry 2542' if x == 'Chemistry 2532' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PERSUASION AND ATTITUDE CHANGE' if x == 'PERSUASION & ATTITUDE CHANGE' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PHILOSOPHICAL ETHICS' if x in ['PHILOSOPHICAL  ETHICS', 'PHILOSOPHICAL ETHICS (EP3)'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PHYSICAL CHEMISTRY LAB I' if x == 'PHYSICAL CHEM LAB I' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PHYSICAL CHEMISTRY LAB II' if x == 'PHYSICAL CHEM LAB II' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "PHYSICAL SCIENCS:TODAY'S WORLD" if x == "PHYSICAL SCIENCS:TODAY'S WORL" else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PHYSICS OF LIGHT AND COLOR' if x == 'PHYSICS OF LIGHT & COLOR' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'POPULAR MUSIC AS COMMUNICATION' if x == 'POPULAR MUSIC AS COMMUN' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'Communication & Culture 3235' if x == 'Comm and Media Studies 3571' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PRECALCULUS' if x == 'PRE-CALCULUS' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PSYCHOLOGY AND HUMAN VALUES' if x == 'PSYCHOLOGY & HUMAN VALUES' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CLINICAL CHILD PSYCHOLOGY' if x == 'CLINICAL CHILD PSYCH' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'STRUCTURES OF COMPUTER SCIENCE' if x in ['STRUCTURES OF COMP SCI', 'STRUCTURES OF COMP SCIENCE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'TEXTS AND CONTEXTS' if x in ['TEXT & CONTEXTS', 'Texts & Contexts', 'TEXTS & CONTEXT', 'TEXTS & CONTEXTS'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'COMPUTER SCIENCE II LAB' if x == 'COMPUTER SCIENCE LAB II' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'COMPUTER SCIENCE I LAB' if x == 'COMPUTER SCIENCE LAB I' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'DISCRETE STRUCTURES II LAB' if x == 'DISCRETE STRUCTURE II  LAB' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SEMINAR AND RESEARCH IV' if x == 'SEMINAR & RESEARCH IV' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SEMINAR AND RESEARCH III' if x == 'SEMINAR & RESEARCH III' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SEMINAR AND RESEARCH II' if x == 'SEMINAR & RESEARCH II' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SEMINAR AND RESEARCH I' if x == 'SEMINAR & RESEARCH I' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GENERAL CHEMISTRY LAB I' if x == 'GENERAL CHEM LAB I' else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTORY BIOLOGY LAB II' if x in ['INTRODUCTORY BIO LAB II', 'INTRO BIO LAB II'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTORY BIOLOGY LAB I' if x in ['INTRODUCTORY BIO LAB I', 'INTRO BIO LAB I'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTORY BIOLOGY II' if x in ['INTRO BIOLOGY II'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTORY BIOLOGY I' if x in ['INTRO BIOLOGY I'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTION TO BIOLOGY II' if x in ['INTRO TO BIOLOGY II'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTION TO BIOLOGY I' if x in ['INTRO TO BIOLOGY I'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ECOLOGY: A HUMAN APPROACH' if x in ['ECOLOGY:A HUMAN APPROACH'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MUSEUM METHODS' if x in ['MUSEUM -- METHODS'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ARABIC LANGUAGE & LITERATURE I' if x in ['ARABIC LANGUAGE & LITERATURE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'TUTORIAL IN ANTHROPOLOGY' if x in ['TUTORIAL IN ANTHRO'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'LANGUAGE, GENDER, AND POWER' if x in ['LANGUAGE, GENDER & POWER'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CULTURE AND CULTURE CHANGE' if x in ['CULTURE & CULTURE CHANGE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'NEW WORLD ARCHAEOLOGY' if x in ['NEW WORLD ARCHAELOLOGY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ANCIENT CULTURES OF THE BIBLE' if x in ['ANC CULT OF THE BIBLE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'MAGIC, SCIENCE, AND RELIGION' if x in ['MAGIC,SCIENCE & RELIGION'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTION TO ARCHAEOLOGY' if x in ['INTRO TO ARCHAEOLOGY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRO TO CULTURAL ANTHROPOLOGY' if x in ['INTRO TO CULTURAL ANTHROPOLOG'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CATHOLICISM AND DEMOCRACY' if x in ['CATHOLICISM & DEMOCRACY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SOCIAL WELFARE AND SOCIETY' if x in ['SOCIAL WELFARE & SOCIETY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'AFFIRMATIVE ACTION: AMER DREAM' if x in ['AFFIRMATIVE ACTION: AMER DREA'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CARIBBEAN PEOPLES AND CULTURE' if x in ['CARIB PEOPLES & CULTURE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CONTEMPORARY AFRICAN IMMIGRATION' if x in ['CONTEMPORARY AFRICAN IMMIGRAT', 'CONTEMPORARY AFRICAN IMMIGRATI'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'BUFFALO SOLDIERS: RACE AND WAR' if x in ['BUFFALO SOLDIERS: RACE & WAR'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'AFRICAN AMERICAN HISTORY II' if x in ['AFRICAN AMERICAN HIST II'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'UNDRSTND HIST CHANGE: AFRICA' if x in ['UNDRSTND HIST CHNGE: AFRICA'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'DOCUMENTARY PHOTOGRAPHY: JAPAN' if x in ['DOCUMENTARY PHOTOGRAPHY:JAPAN'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'GRAPHIC DESIGN II' if x in ['GRAPHIC DESIGN CONCEPT', 'GRAPHIC DESIGN CONCEPTS'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'Book Design & Printed Page' if x in ['DESIGNING BKS,ZINES&CHAPB', 'DESIGNING BKS, ZINES & CHAPBKS'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'LARGE-FORMAT PHOTOGRAPHY' if x in ['LARGE FORMAT PHOTOGRAPHY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'EUCHARIST, JUSTICE, AND LIFE' if x in ['EUCHARIST, JUSTICE, LIFE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FUTURE OF MARRIAGE 21ST CENT' if x in ['MARRIAGE IN 21ST CENTURY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'CHRISTIAN THOUGHT& PRACTICE II' if x in ['CHRISTIAN THOUGHT& PRACTICE I'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'THE BIBLE AND SOCIAL JUSTICE' if x in ['BIBLE AND SOCIAL JUSTICE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'AUGUSTINE, AQUINAS, AND LUTHER' if x in ['AUGUSTINE, AQUINAS & LUTHER'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'BYZANTINE CHRISTIANITY' if x in ['BYZANTINE CHISTIANITY'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTION TO NEW TESTAMENT' if x in ['INTRO TO NEW TESTAMENT'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'THE TORAH' if x in ['THE TORAH (Sacred Texts&Trad)'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'INTRODUCTION TO OLD TESTAMENT' if x in ['INTRO TO OLD TESTAMENT'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'ACTING FOR THE CAMERA I' if x in ['ACTING FOR THE CAMERA'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SET DESIGN I' if x in ['SET DESIGN'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'FRENCH THEATRE AND PERFORMANCE' if x in ['FRENCH THEATRE & PERFORMACE', 'FRENCH THEATRE/ PERFORMANCE'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'PROJECTION DESIGN I' if x in ['PROJECTION DESIGN'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: 'SOUND DESIGN I' if x in ['SOUND DESIGN'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ACTOR'S VOCAL TECHNIQUE II" if x in ["ACTOR'S VOCAL TECH II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ACTOR'S VOCAL TECHNIQUE I" if x in ["ACTOR'S VOCAL TECH I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SONG AS SCENE I" if x in ["SONG AS SCENE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "STAGE MANAGEMENT I" if x in ["STAGE MANAGEMENT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "COSTUME DESIGN I" if x in ["COSTUME DESIGN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "STAGE MAKEUP AND HAIR I" if x in ["STAGE MAKEUP AND HAIR"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO FASHION DESIGN" if x in ["INTRO TO FASHION DESIGN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CERVANTES AND DON QUIXOTE" if x in ["CERVANTES & DON QUIXOTE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SPANISH-AMERICAN WOMEN WRITERS" if x in ["SPAN-AMER WOMEN WRITERS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "NEW YORK IN LATINO LIT & FILM" if x in ["NEW YORK IN LATINO LIT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MODERN HISPANIC THEATER" if x in ["MODERN HISPANIC THEATRE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "DILEMMAS OF THE MODERN SELF" if x in ["DILEMMAS OF MODERN SELF"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "URBAN ISSUES AND POLICIES" if x in ["URBAN ISSUES & POLICIES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "U.S. PRISON COMMUNITY" if x in ["MASS INCARCERATION"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SOC ISS DOCUMENTARY FILMMAKING" if x in ["SOC ISS DOCUMENTARY FILMMAKIN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WORK, FAMILY AND GENDER" if x in ["WORK, FAMILY, AND GENDER"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONTEMPORARY FAMILY ISSUES" if x in ["CONTEMP FAMILY ISSUES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RACE, RACISM, AND WHITENESS" if x in ["RACE, RACISM, & WHITNESS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "DEVELOPMENT AND GLOBALIZATION" if x in ["DEVELOP & GLOBALIZATION"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: '"RACE" AND "MIXED RACE"' if x in ['ACE" AND "MIXED RACE""', 'RACE AND "MIXED RACE"'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "METHODS SOCIAL RESEARCH II" if x in ["METHODS SOCIAL RESRCH II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "METHODS SOCIAL RESEARCH I" if x in ["METHODS SOCIAL RESRCH I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "DRUGS, LAW, AND SOCIETY" if x in ["DRUGS, LAW & SOCIETY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RELIGION AND SOCIAL CHANGE" if x in ["RELIGION & SOCIAL CHANGE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO SOCIOLOGY" if x in ["INTRO TO SOCIOLOGY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RUSSIAN LANGUAGE & LITERATURE" if x in ["ADVANCED RUSSIAN I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HONORS THESIS IN PSYCHOLOGY II" if x in ["HONORS THESIS IN PSYC II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HONORS THESIS IN PSYCHOLOGY I" if x in ["HONORS THESIS IN PSYC I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "LAW AND PSYCHOLOGY" if x in ["LAW & PSYCHOLOGY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MULTICULTURAL PSYCHOLOGY" if x in ["MULTICULTURAL ISSUES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SPORTS PSYCHOLOGY" if x in ["SPORT PSYCHOLOGY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ADOLESCENT & ADULT DEVELOPMENT" if x in ["ADOLESCENT & ADULT DEVELOPMEN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SENSATION AND PERCEPTION LAB" if x in ["SENSATION & PERCEPTION LAB"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SEM: THE WORLD OF DEMOCRACY" if x in ["SEM:THE WORLD OF DEMOCRACY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "FREUD,POLITICS,SEXUALITY" if x in ["SEM:FREUD, POLITICS, SEXUALITY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CHINA AND U.S. IN GLOBAL ERA" if x in ["CHINA & US IN GLOBAL ERA"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "POLITICS OF THE EUROPEAN UNION" if x in ["POL OF THE EUR UNION"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "POLITICAL ECONOMY OF POVERTY" if x in ["POL ECON OF POVERTY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONFLICT ANALYSIS/RESOLUTION" if x in ["CONFLICT ANALYSIS / RSLTN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "UN AND POLITICAL LEADERSHIP" if x in ["UN & POLITICAL LEADERSHIP"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "LIBERALISM AND ITS CRITICS" if x in ["LIBERALISM & ITS CRITICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "AMERICAN POLITICAL THOUGHT" if x in ["AMER. POLITICAL THOUGHT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RACIAL AND ETHNIC POLITICS" if x in ["RACIAL & ETHNIC POLITICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CIVIL RIGHTS AND LIBERTIES" if x in ["CIVIL RIGHTS & LIBERTIES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRO TO POLITICAL PHILOSOPHY" if x in ["INTRO TO POLITICAL THEORY", 'INTRO TO POLITICAL PHIL'] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRO TO AMERICAN LEGAL SYSTEM" if x in ["INTRODUCTION TO LAW"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO URBAN POLITICS" if x in ["INTRO TO URBAN POLITICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO POLITICS" if x in ["INTRO TO POLITICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "THERMO AND STAT PHYSICS" if x in ["THERMO & STAT PHYSICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MATH METHODS IN PHYSICS II" if x in ["MATH METH IN PHYSICS II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MATH METHODS IN PHYSICS I" if x in ["MATH METH IN PHYSICS I", "MATH METHODS IN PHYSICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRO TO INVENTIONS & PATENTS" if x in ["INTRO TO INVENTIONS&PATENTS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ENGINEERING STATICS & DYNAMICS" if x in ["STATICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO PHYSICS II" if x in ["INTRO PHYSICS II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO PHYSICS I" if x in ["INTRO PHYSICS I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO ASTRONOMY" if x in ["INTRO ASTRONOMY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EVIL, VICE, AND SIN" if x in ["EVIL, VICE AND SIN"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WAR AND PEACE: JUST WAR THEORY" if x in ["WAR & PEACE: JUST WAR THEORY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ENVIRONMENTAL ETHICS" if x in ["ENVIRONMENTAL ETHICS (EP4,VAL)"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HAPPINESS AND WELL-BEING" if x in ["HAPPINESS & WELL-BEING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HUMANITY'S VALUE" if x in ["HUMANITY'S VALUE (EP4/VALUES)"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "AFRICAN AMERICAN PHILOSOPHY" if x in ["AFRICAN AMERICAN PHIL"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONTEMPORARY FRENCH PHILOSOPHY" if x in ["CONTEMPORARY FRENCH PHIL"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RELATIVISM AND PHILOSOPHY" if x in ["RELATIVISM & PHILOSOPHY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "PHILOSOPHY OF HUMAN NATURE" if x in ["PHIL OF HUMAN NATURE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ADVANCED MICROBIOLOGY" if x in ["BACTERIOLOGY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ANIMAL PHYSIOLOGY" if x in ["VERTEBRATE PHYSIOLOGY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ENVIRONMENT: SCI, LAW & POLICY" if x in ["ENVIRONMENT: SCI, LAW & POLIC"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RESEARCH DESIGN AND ANALYSIS" if x in ["RESEARCH DESIGN & ANALYSIS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GLOBAL ECOLOGY" if x in ["GLOBAL ECOLOGY LECTURE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONCEPTS IN BIOLOGY II" if x in ["CONCEPTS IN BIOLOGY LECTURE II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONCEPTS IN BIOLOGY I" if x in ["CONCEPTS IN BIOLOGY LECTURE I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GENERAL BIOLOGY LAB II" if x in ["GENERAL BIO LAB II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GENERAL BIOLOGY LAB I" if x in ["GENERAL BIO LAB I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GENERAL BIOLOGY II" if x in ["GENERAL BIOLOGY LECTURE II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GENERAL BIOLOGY I" if x in ["GENERAL BIOLOGY LECTURE I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO GAME NARRATIVE" if x in ["DIGITAL STORYTELLING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MUSIC THEORY III" if x in ["MUSCNSHIPIII:CHROMATIC HARMONY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MUSIC THEORY II" if x in ["MUSCNSHIP II:DIATONIC HARMONY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MUSIC THEORY I" if x in ["MUSCNSHIP I:COUNTERPOINT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "PIANO LAB" if x in ["KEYBOARD LAB"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EAR-TRAINING AND SIGHT-SINGING" if x in ["EAR TRAINING", "EAR-TRAINING&SIGHT-SINGING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO MUSIC THEORY" if x in ["INTRODUCTION TO MUSICIANSHIP"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WORLD MUSIC AND DANCE" if x in ["WORLDS OF MUSIC"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "JAZZ: A HISTORY IN SOUND" if x in ["JAZZ, A HISTORY IN SOUND"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MUSIC FOR DANCERS I" if x in ["MUSIC FOR DANCERS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO MUSIC HISTORY" if x in ["MUSIC HISTORY INTRODUCTION"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "VILLAINS,VAMPS AND VAMPIRES" if x in ["VILLIANS,VAMPS AND VAMPIRES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ARAB CULTURE AND NEWS MEDIA" if x in ["ARAB CULTURE & NEWS MEDIA"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SEMINAR: MIDDLE EAST" if x in ["SEM:MIDDLE EAST"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MATH FOR BUSINESS: PRECALCULUS" if x in ["MATH FOR BUSINESS:PRECALCULUS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO MANDARIN I" if x in ["INTRO TO MANDARIN I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRO TO INTERNATIONAL STUDIES" if x in ["INTRO TO INTERNATIONAL STUDIE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "AUTOBIOGRAPHIES" if x in ["AUTOBIOGRAPHY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "PRE-COLLEGE SKILLS DEVELOPMENT" if x in ["PRE-COLL SKILLS DEVELOP"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SEM: COLD WAR SCIENCE & TECH" if x in ["SEM : COLD WAR SCIENCE & TECH"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HYSTERIA/SEXUALITY/UNCONSCIOUS" if x in ["HYSTERIA/SEXUALITY/UNCONSCIOU"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SEM: HISTORY AND FILM" if x in ["HISTORY AND FILM (Core ICC)"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ANTISEMITISM" if x in ["ANTISEMITISM (EP4/vALUES)"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "HISTORY OF U.S. SEXUALITY" if x in ["HISTORY OF US SEXUALITY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RISE OF AMERICAN SUBURB" if x in ["RISE OF AMERICAN SUBURB (ICC)"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "U.S. IMMIGRATION/ETHNICITY" if x in ["US IMMIGRATION/ETHNICITY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "U.S. BETWEEN WARS: 1919-1941" if x in ["US BETWEEN WARS 1919-41"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "AFRICAN-AMERICAN HISTORY I" if x in ["AFRICAN-AMERICAN HIST I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CIVIL WAR ERA: 1861-1877" if x in ["CIVIL WAR ERA, 1861-1877"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EUROPE: 1900-1945: TOTAL WAR" if x in ["EUROPE 1900-1945: TOTAL WAR"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "IRELAND: 1688-1923" if x in ["IRELAND, 1688-1923"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "BRITAIN: 1867-PRESENT" if x in ["BRITAIN, 1867-PRESENT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EUROPEAN WOMEN: 1800-PRESENT" if x in ["EUROPEAN WOMEN 1800-PRESENT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EUROPEAN WOMEN: 1500-1800" if x in ["EUROPEAN WOMEN 1500-1800"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "TUDOR AND STUART ENGLAND" if x in ["TUDOR & STUART ENGLAND"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WORKER IN AMERICAN LIFE" if x in ["WORKER IN AMER LIFE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EUROPE IN CRISIS: 1880-1914" if x in ["EUROPE IN CRISIS 1880-1914"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "UNDER HIST CHG:EAST ASIAN HIST" if x in ["UNDER HIST CHG:EAST ASIAN HIS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "UNDRSTND HIST CHNGE:ANC GREECE" if x in ["UNDRSTND HIST CHNGE:ANC GREEC"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "UNDRSTND HIST CHNGE: AMER HIST" if x in ["UNDRSTND HIST CHNGE: AMER HIS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "UNDRSTND HIST CHG:ERLY MOD EUR" if x in ["UNDRSTND HIST CHG:ERLY MOD EU"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "BORDERS AND CROSSINGS" if x in ["BORDERS & CROSSINGS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WRITERS AND LAWBREAKERS" if x in ["WRITERS & LAWBREAKERS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "GRAMMAR AND PHONETICS" if x in ["COMPREHENSIVE GRAMMAR DRILL"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO FRENCH I" if x in ["Introduction to French I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WRITING TELEVISION SITCOMS" if x in ["WRITING TV SITCOMS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ENVIRONMENTAL SCIENCE RESEARCH" if x in ["ENVIRONMENTAL SCI RESEACH", "ENVIRONMENTAL SCI RESEARCH"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "JAZZ AGE, LIT & CULTURE" if x in ["SEM : JAZZ AGE, LIT & CULTURE"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "RACE AND HOLLYWOOD FILM" if x in ["RACE AND REPRESENTATION"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "JOYCE'S ULYSSES" if x in ["SEM: JOYCE'S ULYSSES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MODERN & POST MODERN POETRY" if x in ["MODERN POETRY", "MODERNIST POETRY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "AMERICAN DREAM IN LITERATURE" if x in ["AMERICAN DREAM IN LIT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "EARLY MODERN LIT 1579-1625" if x in ["EARLY MOD POTRY&DRAM 1579-1625"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "PLAYS AND PLAYERS, 1700-1800" if x in ["PLAYS & PLAYERS, 1700-1800"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MEDIEVAL LITERATURE: 1000-1330" if x in ["MEDIEVAL LIT 1000-1330"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "MEDIEVAL TOLERANCE/INTOLERANCE" if x in ["MEDIEVAL TOLERANCE/INTOLERANC"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO OLD ENGLISH" if x in ["INTRO TO OLD ENGLISH"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "DIGITAL CREATIVE WRITING" if x in ["SEM: DIGITAL CREATIVE WRITING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ETHICS AND ECONOMICS" if x in ["ETHICS & ECONOMICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "COMPARATIVE ECONOMIC SYSTEMS" if x in ["COMPARATIVE ECON SYSTEMS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTERNATIONAL ECONOMICS" if x in ["INT'L ECONOMIC POLICY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "WORLD POVERTY" if x in ["WORLD POVERTY(SERVICE LEARNING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ECONOMY OF LATIN AMERICA" if x in ["ECON OF LATIN AMERICA"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ECON AND BUSINESS FORECASTING" if x in ["ECON & BUSIN FORECASTING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "STATISTICAL DECISION MAKING" if x in ["STATS DECISION MAKING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "THE WEALTH OF WORDS:ECON & LIT" if x in ["THE WEALTH OF WORDS:ECON & LI"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SENIOR PROJECT IN PERFORMANCE" if x in ["SENIOR PROJECT IN PERFOR", "SENIOR PROJECT IN PERFOM"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ANATOMY AND KINESIOLOGY II" if x in ["ANATOMY & KINESIOLOGY II"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ANATOMY AND KINESIOLOGY I" if x in ["ANATOMY & KINESIOLOGY I"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "THE DIRECTOR'S VISION" if x in ["THE FILM DIRECTOR"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "FREEDOM OF EXPRESSION" if x in ["VER CENSORSHIP/FREE OF EXPRES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "ADV TV PRODUCTION- BRONXNET" if x in ["BRONX NET"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "JOURNALISM WORKSHOP" if x in ["JOURNALISM W/S: PHOTOGRAPHY", "JOURNALISM W/S: REPORTING", "JOURNALISM WORKSHOP: PHOTO", "JOURNALISM WORKSHOP: LAYOUT", "JOURNALISM W/S: LAYOUT"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRO TO MEDIA INDUSTRIES" if x in ["MEDIA INDUSTRIES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CONTEMPORARY CUBAN CULTURE" if x in ["CUBA: REVOL, LIT & FILM"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "SEMINAR AND DIRECTED STUDY" if x in ["SEMINAR & DIRECTED STUDY"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "CYBERSPACE: ISSUES AND ETHICS" if x in ["CYBERSPACE - ETHICS & ISSUES"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INFORMATION RETRIEVAL SYSTEMS" if x in ["INFO RETRIEVAL SYSTEMS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "DATABASE SYSTEMS" if x in ["DATA BASE SYSTEMS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTERNET AND WEB PROGRAMMING" if x in ["INTERNET & WEB PROGRAMMING"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INTRODUCTION TO ROBOTICS" if x in ["INTRO TO ROBOTICS"] else x)
    df['CourseTitle'] = df['CourseTitle'].apply(
        lambda x: "INFOR & DATA MANAGEMENT" if x in ["INFO & DATA MANAGEMENT"] else x)

    df['Department'] = df['Department'].apply(
        lambda x: "Hebrew" if x in ["HEBW"] else x)
    df['Department'] = df['Department'].apply(
        lambda x: "Environmental Law" if x in ["Environmental Policy"] else x)
    df['Department'] = df['Department'].apply(
        lambda x: "Humanitarian Studies" if x in ["Humanitarian Affairs"] else x)


    df['StudentLevel'] = df['StudentLevel'].apply(
        lambda x: "Freshman" if x in ["Continuing Freshman", "First-Time Freshman"] else x)


    df['FinLetterGrade'] = df['FinLetterGrade'].apply(
        lambda x: "F" if x in ["WF", "AF"] else x)


    df = df[df['FinLetterGrade'].isin(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C','C-', 'D', 'F', 'P'])]


    df_crsc = pd.read_csv("crs-to-dept.csv")

 # Ensure other values are returned unchanged

    # Step 1: Filter out unwanted departments
    df = df[
        ~df["Department"].isin(
            [
                "Women's Studies",
                "Service Learning",
                "Humanitarian Affairs",
                "Administrative Study Aboard",
                "Administrative FCLC",
                "Administrative GSAS",
                "GSB Information Systems",
                "GSB Management",
                "GSB Marketing",
            ]
        )
    ]


    # Step 2: Apply general_changes to the "Department" column

    # Step 3: Merge with df_crsc to add CRC column


    df = df.drop(columns="CourseCode")


    df = df.merge(df_crsc[["Department", "CourseCode"]], on="Department", how="left")


    #
    # # Step 4: Create the "CourseCode" column by conca
    df["CourseCode"] = df["CRC"].astype(str) + " " + df["CourseNum"].astype(str)

    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 3980' if x == 'THEA 3985' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'AFAM 1600' if x == 'AFAM 1601' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'AFAM 3002' if x == 'AFAM 2100' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 3564' if x == 'THEA 3563' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 3455' if x == 'THEA 3450' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 3420' if x == 'THEA 3430' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 2805' if x == 'THEA 2800' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'THEA 2210' if x == 'THEA 2211' else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'PHYS 3100' if x in ['PHYS 3101'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'ENVS 4502' if x in ['ENVS 4501'] else x)
    df['CourseCode'] = df['CourseCode'].apply(
        lambda x: 'DANC 4811' if x in ['DANC 4810'] else x)


    # # Step 5: Merge with df_des to add the course descriptions
    df_des = pd.read_csv("/home/mariom/Work/Fordham/labs/Fall24/final-project-CF/scraped_desc/pross-course-desc.csv")
    df = df.merge(df_des[["CourseCode", "Description"]], on="CourseCode", how="left")


    df["Description"] = df["Description"].fillna(df["CourseCode"])


    df.drop('Unnamed: 0', inplace=True, axis=1) if 'Unnamed: 0' in df.columns else None
    df.drop('index', inplace=True, axis=1)
    df.drop('sem', inplace=True, axis=1)
    df.drop('year', inplace=True, axis=1)
    df.drop('oldCRN', inplace=True, axis=1)
    df.drop('STU_DegreeSeek', inplace=True, axis=1)
    df.drop('schedType', inplace=True, axis=1)
    df.drop('campus', inplace=True, axis=1)
    df.drop('GradTerm', inplace=True, axis=1)
    df.drop('CRC', inplace=True, axis=1)

    return df

# perform necessary data cleanup
df = dataCleanup(df)

#save cleaned files into dataframe
df.to_csv('processed-data-11-25-24.csv', index=False)