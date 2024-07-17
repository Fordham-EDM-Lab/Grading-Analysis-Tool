# Grading-Analysis-Tool
This is an Educational Data Mining tool. It reads data from an university and makes analysis of its contents. Created by Mario Marku, Luisa Rosa, with Dr.Daniel Leeds, Dr.Gary Weiss, and Hyun Jeong at Fordham University.

The main goal is to analyze instructor grading in a more sophisticated way. In the same way that students have freedom when selecting university courses, instructors can have different grading criteria and policies. Usually, professors assign grades with great discretion. Grading can impact how hard a student prepares for an exam and the effort put into the class. It is essential to understand these different grading patterns.

Our publicly available python-based educational data mining tool helps to identify instructor and department grading patterns, consistently having high (or low) grading over many years, courses, and instructors. It performs detailed data analysis and generates understandable instructor grading assessments.

Library free for use, required citation using ... in any resulting publications.
Library free for redistribution provided you retain the author attributions above.

The following packages are required for installation before use: numpy, pandas, csv, matplotlib

"FordhamProcessor.py" is used by our university only to clean and prepare the data for analysis. The data input should meet some requirements before initializing the tool. --> TODO: A document explaining the requirements for the input data will be uploaded soon.
"CreateTables.py" is necessary so that the tool can perform efficiently without reloading every time it is used (wasting about 20 minutes). A user should run this file if it is the first time they will use this tool OR if there were any changes made to the data input file. Otherwise, the user can run the tool without any pre-processing.
"Tool.py" is the actual data analysis tool. It performs the calculations and delivers conclusions about the data.
--> TODO: Tool still needs to be updated so that the user interface is more intuitive, include a notification that a file was saved in the current folder, and save each terminal session into a .txt file so that the results are outputted to the user are saved for future reference.
