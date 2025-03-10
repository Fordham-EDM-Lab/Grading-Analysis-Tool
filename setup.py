from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="GradeAnalysisTool",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=required,
    entry_points={
        "gui_scripts": [
            # Notice: the folder name is now grade_analysis
            "grade-analysis=grade_analysis.gradeAnalysisGUI:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

