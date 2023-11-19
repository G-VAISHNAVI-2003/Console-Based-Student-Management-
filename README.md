# Console-Based-Student-Management-system

## Overview
This Python Student Management System interacts with a MySQL database, offering CRUD operations, search, display, and filtering. It features a user-friendly console interface, JSON/CSV data export, and utilizes MySQL Connector and Tabulate for efficient data handling and presentation.

## Features
- **Insert:** Add new student records with details such as full name, age, date of birth, class, and subject-wise marks.
- **Display:** View all student records along with calculated averages, percentages, and grades.
- **Search:** Find students based on criteria such as full name, date of birth, or class.
- **Update:** Modify student information, including full name, age, date of birth, or class.
- **Delete:** Remove a student record, including associated subject-wise marks.
- **Filter:** Retrieve students based on age range, class, or grade.

## Database Setup
- Ensure you have MySQL installed.
- Create a database named `student_management`.
- Update the database connection details in the script (`host`, `user`, `password`) to match your MySQL setup.

## Dependencies
- MySQL Connector: `pip install mysql-connector-python`
- Tabulate: `pip install tabulate`

## How to Use
1. Run the script.
2. Choose an operation from the menu (Insert, Display, Search, Update, Delete, Filter, Exit).
3. Follow the prompts to input or retrieve information.
4. View the results on the console and check for any exported JSON/CSV files in the project directory.

## Exported Files
- Student records are exported to `student_records.json` and `student_records.csv` during display.
- Filtered student records are exported to `filtered_student_records.json` and `filtered_student_records.csv` during filtering.

## Note
- This system assumes a MySQL database named `student_management` is set up and accessible.

## Sample Result
![py5](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/ba69505a-ef22-461d-9037-94d92beb4995)
![py4](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/64c65809-fda0-46be-bf7b-41e0a2c2766c)
![py3](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/04f69bb1-1688-48e4-9bea-18929dd7bc24)
![py2](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/9a3a2444-517e-4107-8a26-a1809dbfd7e8)
![py1](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/5030723b-c249-4c26-9767-6bbbd55dbbc1)
![image](https://github.com/G-VAISHNAVI-2003/Console-Based-Student-Management-/assets/139878536/f261ab65-a2fb-4b05-bc60-943ce85d68a7)


