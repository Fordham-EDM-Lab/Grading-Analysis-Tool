course_analysis_options = {
    "Course vs GPA": False,
    "Course vs Enrollment": False,
    "Course vs Section #": False,
    "Enrollment vs GPA": False,
    "Course vs Standard Deviation": False,
    "GPA vs Standard Deviation": False,
}

major_analysis_options = {
    "Major vs GPA": False,
    "Major vs Enrollment": False,
    "Major vs Course #": False,
    "Major vs Section #": False,
    "GPA vs Enrollment": False,
    "Standard Deviation vs Enrollment": False,
}

section_analysis_options = {
    "Section vs GPA": False,
    "Section vs Class Size": False,
    "GPA vs Class Size": False,
    "Section vs Standard Deviation": False,
    "Enrollment vs Standard Deviation": False,
    "GPAW vs Standard Deviation": False,
}

instructor_analysis_options = {
    "Instructor vs GPA": False,
    "Instructor vs Enrollment": False,
    "Enrollment vs GPA": False,
    "GPA vs Standard Deviation": False,
    "GPAW vs CoV(%)": False,
    "Instructor vs Section #": False,
    "Instructor vs Course #": False,
    "Instructor vs Standard Deviation": False,
}

department_analysis_options = {
    "Department vs GPA": False,
    "Department vs Enrollment": False,
    "Department vs Course #": False,
    "Department vs Section #": False,
    "Standard Deviation vs Enrollment": False,
    "Enrollment vs GPA": False,
    "GPA vs Standard Deviation": False
}

studentlevel_analysis_options = {
    "Student Level vs Enrollments":False,
    "Student Level vs GPA":False,
    "Student Level vs Courses": False,

}

courselevel_analysis_options = {
    "Course Level vs Enrollments":False,
    "Course Level vs GPA":False,
    "Course Level vs Course #":False
}

studentcourse_analysis_options = {
    "Student-Course vs Enrollment":False,
    "Student-Course vs GPA":False,
}

student_analysis_options = {
    "GPA groups vs Student Count": False,
    "Student Course # Taken vs Student Average GPA": False,
}



def reset_all_false():
    options = [studentcourse_analysis_options, courselevel_analysis_options, studentlevel_analysis_options, 
               department_analysis_options, instructor_analysis_options, section_analysis_options,
               major_analysis_options, course_analysis_options, student_analysis_options, studentcourse_analysis_options]
    
    for option in options:
            option.update({key: False for key in option})

def is_option_analysis(item: str) -> bool:
    options = [studentcourse_analysis_options, courselevel_analysis_options, studentlevel_analysis_options,
               department_analysis_options, instructor_analysis_options, section_analysis_options,
               major_analysis_options, course_analysis_options, student_analysis_options, studentcourse_analysis_options]
    for option in options:
        if item in option:
            return True
    return False

def change_analysis_value(item: str, value: bool):
    options = [studentcourse_analysis_options, courselevel_analysis_options, studentlevel_analysis_options,
               department_analysis_options, instructor_analysis_options, section_analysis_options,
               major_analysis_options, course_analysis_options, student_analysis_options, studentcourse_analysis_options]
    for option in options:
        if item in option:
            option[item] = value

def output_analysis_values(item: str):
    options = [studentcourse_analysis_options, courselevel_analysis_options, studentlevel_analysis_options,
               department_analysis_options, instructor_analysis_options, section_analysis_options,
               major_analysis_options, course_analysis_options, student_analysis_options, studentcourse_analysis_options]
    for option in options:
        if item in option:
            return option[item]
    return ''



