
import pandas as pd
import gradeAnalysisFunc as gaf
import random
import requests
from tabulate import tabulate
import io



def create_random_dataframe(num_rows=10000):
    def get_major_df():
        url = 'https://fivethirtyeight.datasettes.com/fivethirtyeight/college-majors~2Fmajors-list.csv?_size=max'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            major_df = pd.read_csv(io.StringIO(response.text))
            return major_df
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
    major_df = get_major_df()

    def get_course_df():
        url = 'https://waf.cs.illinois.edu/discovery/course-catalog.csv'
        try:
            response = requests.get(url)
            response.raise_for_status()
            course_df = pd.read_csv(io.StringIO(response.text))
            return course_df
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
    course_df = get_course_df()

    def RANDOM_sid():
        n = []
        for i in range(1000):
            num = str((random.randrange(100, 999, 1)))
            n.append('S' + num)
        return n

    def RANDOM_FID():
        n = []
        for i in range(500):
            num = str((random.randrange(10, 99, 1)))
            n.append('F' + num)
        return n

    def RANDOM_term():
        n = []
        for i in range(100):
            year = str((random.randrange(2005, 2025, 1)))
            term = str((random.randrange(10, 30, 10)))
            n.append(year + term)
        return n

    def RANDOM_cid():
        n = []
        for i in range(1000):
            n.append(random.randrange(100, 999, 1))
        return n

    def RANDOM_coursenum():
        n = []
        for i in range(1000):
            n.append(random.randrange(100, 999, 100))
        return n

    def RANDOM_coursecode(dept_list: list):
        n = []
        for i in range(1000):
            num = str((random.randrange(100, 999, 100)))
            dept = random.choice(dept_list)
            n.append(dept + ' ' + num)
        return n

    department_list = [
        "Theatre", "Visual Arts", "Music", "Comm and Media Studies", "Dance",
        "Mathematics", "Anthropology", "Natural Science", "Sociology",
        "Environmental Science", "Art History", "Irish Studies", "Chemistry",
        "Theology", "African & African Amer Studies",
        "History", "English", "Spanish", "Political Science", "Interdisciplinary",
        "Economics", "Psychology", "Biological Sciences",
        "Classical Lang & Civilization", "French", "Independent Study", "Philosophy",
        "Italian", "Physics", "American Catholic Studies",
        "Computer and Info Science", "Humanitarian Affairs", "Humanitarian Studies",
        "Latin", "Greek", "Peace and Justice Studies", "Communication & Culture",
        "New Media & Digital Design", "Digital Tech & Emerging Media",
        "Integrative Neuroscience", "Medieval Studies", "Film & Television",
        "Center for Ethics Education", "Journalism",
        "Latin Amer and Latino Studies", "Mandarin Chinese", "Symposium",
        "Modern Languages", "Women, Gender, & Sexuality St",
        "Comparative Literature", "American Studies", "Women's Studies",
        "Middle East Studies", "International Studies", "Urban Studies",
        "Environmental Policy", "Environmental Studies",
        "German", "Japanese", "Russian",
        "Arabic", "Linguistics",
    ]

    major_list = random.sample(list(major_df['Major'].unique()), 50)
    course_list = random.sample(list(course_df['Name'].unique()), 100)
    credit_list = [1, 2, 3, 4]
    letter_grade_dict = {
        'A': 4.0,
        'A-': 3.67,
        'B+': 3.33,
        'B': 3.00,
        'B-': 2.67,
        'C+': 2.33,
        'C': 2.0,
        'C-': 1.67,
        'D': 1.0,
        'F': 0.0
    }
    term_list = ['Fall', 'Spring', 'Summer']
    class_size_list = ['12', '18', '24', '36', '108']
    sid_list = RANDOM_sid()
    fid_list = RANDOM_FID()
    term_num = RANDOM_term()
    course_id_list = RANDOM_cid()
    course_num_list = RANDOM_coursenum()
    course_code = RANDOM_coursecode(department_list)
    student_level_list = ['Freshman', 'Sophmore', 'Junior', 'Senior']
    data = {
        'SID': random.choices(sid_list, k=num_rows),
        'Department': random.choices(department_list, k=num_rows),
        'CourseNum': random.choices(course_num_list, k=num_rows),
        'CredHrs': random.choices(credit_list, k=num_rows),
        'term': random.choices(term_num, k=num_rows),
        'ClassSize': random.choices(class_size_list, k=num_rows),
        'FacultyID': random.choices(fid_list, k=num_rows),
        'CourseTitle': random.choices(course_list, k=num_rows),
        'contact_hrs': [random.randint(1, 4) for _ in range(num_rows)],  # Generate random contact hours
        'StudentLevel': random.choices(student_level_list, k=num_rows),
        'Major': random.choices(major_list, k=num_rows),
        'FinLetterGrade': random.choices(list(letter_grade_dict.keys()), k=num_rows),
        'Semester': random.choices(term_list, k=num_rows),
        'UniqueCourseID': random.choices(course_id_list, k=num_rows),
        'CourseCode': random.choices(course_code, k=num_rows)
    }

    df = pd.DataFrame(data)

    # Calculate FinNumericGrade based on FinLetterGrade
    df['FinNumericGrade'] = df['FinLetterGrade'].map(letter_grade_dict)

    return df

def run_cmd(num_rows):
    create_random_dataframe(num_rows)
