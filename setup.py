from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="GradeAnalysisTool",
    version="1.0",
    packages=find_packages(where="src"),  # Finds all packages inside src/
    package_dir={"": "src"},  # Specifies src as the package root
    install_requires=required,  # Install dependencies from requirements.txt
    entry_points={
        "gui_scripts": [
            "grade-analysis=gradeAnalysisGUI:main",  # Creates a runnable command
        ],
    },
    include_package_data=True,  # Ensures data files inside packages are included
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
