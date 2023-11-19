import json
import csv
from datetime import date
from decimal import Decimal
import mysql.connector
from tabulate import tabulate
conn = mysql.connector.connect(host="localhost",user="root",password="",database="student_management")

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, Decimal)):
            return str(obj)
        return super().default(obj)

    
def insert():
    res = conn.cursor()
    Full_name = str(input("Enter the Full name: "))
    Age = (input("Enter the Age: "))
    Date_of_Birth = input("Enter the Date_of_Birth (YYYY-MM-DD): ")
    Class = input("Enter the class: ")

    res = conn.cursor()
    res.execute("INSERT INTO students (Full_name, Age, Date_of_Birth, Class) VALUES (%s, %s, %s, %s)",
                   (Full_name, Age, Date_of_Birth, Class))
    conn.commit()
    
    student_id = res.lastrowid
    subject_list = list(map(str, input("Enter the subjects (space-separated): ").split()))

    for subject in subject_list:
        # Check if the subject already exists
        res.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject,))
        existing_subject = res.fetchone()

        if existing_subject:
            subject_id = existing_subject[0]
        else:
            # Insert the subject if it doesn't exist and retrieve its subject_id
            res.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject,))
            conn.commit()
            subject_id = res.lastrowid

        mark = int(input(f"Enter marks for {subject}: "))
        res.execute("INSERT INTO student_marks (student_id, subject_id, marks) "
                       "VALUES (%s, %s, %s)",
                       (student_id, subject_id, mark))
        conn.commit()

    print("\nRecord inserted Successfully.")
    
    # Close the cursor after executing queries
    res.close()

def display():
    res = conn.cursor()
    res.execute("""
        SELECT 
            s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
            GROUP_CONCAT(sub.subject_name) AS Subjects, 
            GROUP_CONCAT(sm.marks) AS Marks, 
            AVG(sm.marks) AS Average_Marks, 
            AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
            CASE
                WHEN AVG(sm.marks) >= 90 THEN 'A+'
                WHEN AVG(sm.marks) >= 80 THEN 'A'
                WHEN AVG(sm.marks) >= 70 THEN 'B'
                WHEN AVG(sm.marks) >= 60 THEN 'C'
                WHEN AVG(sm.marks) >= 50 THEN 'D'
                ELSE 'F'
            END AS Grade
        FROM students s
        LEFT JOIN student_marks sm ON s.student_id = sm.student_id
        LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
        GROUP BY s.student_id
    """)
    
    records = res.fetchall()

    if not records:
        print("No records found.")
    else:
        headers = ["Student ID", "Full Name", "Age", "Date of Birth", "Class",
                   "Subjects", "Marks", "Average Marks", "Percentage", "Grade"]

        table = [list(record) for record in records]

        print("\nStudent Records:")
        print(tabulate(table, headers, tablefmt="pretty"))

        # Export to JSON with custom encoder
        with open("student_records.json", "w") as json_file:
            json.dump(records, json_file, cls=CustomJSONEncoder)

        # Export to CSV
        with open("student_records.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)
            csv_writer.writerows(table)

    res.close()
    conn.close()

def search():
    # Use a context manager for the cursor
    with conn.cursor() as res:
        print("\nSearch Criteria:")
        print("1. Full Name")
        print("2. Date of Birth")
        print("3. Class")
        print("\n")
        search_choice = int(input("Choose the search criterion (1/2/3): "))
        if search_choice == 1:
            full_name = input("Enter Full Name to search: ")
            res.execute("""
                SELECT 
                    s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                    GROUP_CONCAT(sub.subject_name) AS Subjects, 
                    GROUP_CONCAT(sm.marks) AS Marks, 
                    AVG(sm.marks) AS Average_Marks, 
                    AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                    CASE
                        WHEN AVG(sm.marks) >= 90 THEN 'A+'
                        WHEN AVG(sm.marks) >= 80 THEN 'A'
                        WHEN AVG(sm.marks) >= 70 THEN 'B'
                        WHEN AVG(sm.marks) >= 60 THEN 'C'
                        WHEN AVG(sm.marks) >= 50 THEN 'D'
                        ELSE 'F'
                    END AS Grade
                FROM students s
                LEFT JOIN student_marks sm ON s.student_id = sm.student_id
                LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
                WHERE s.Full_name LIKE %s
                GROUP BY s.student_id
            """, (f"%{full_name}%",))

        elif search_choice == 2:
            dob = input("Enter Date of Birth to search (YYYY-MM-DD): ")
            res.execute("""
                SELECT 
                    s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                    GROUP_CONCAT(sub.subject_name) AS Subjects, 
                    GROUP_CONCAT(sm.marks) AS Marks, 
                    AVG(sm.marks) AS Average_Marks, 
                    AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                    CASE
                        WHEN AVG(sm.marks) >= 90 THEN 'A+'
                        WHEN AVG(sm.marks) >= 80 THEN 'A'
                        WHEN AVG(sm.marks) >= 70 THEN 'B'
                        WHEN AVG(sm.marks) >= 60 THEN 'C'
                        WHEN AVG(sm.marks) >= 50 THEN 'D'
                        ELSE 'F'
                    END AS Grade
                FROM students s
                LEFT JOIN student_marks sm ON s.student_id = sm.student_id
                LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
                WHERE s.Date_of_Birth = %s
                GROUP BY s.student_id
            """, (dob,))

        elif search_choice == 3:
            class_name = input("Enter Class to search: ")
            res.execute("""
                SELECT 
                    s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                    GROUP_CONCAT(sub.subject_name) AS Subjects, 
                    GROUP_CONCAT(sm.marks) AS Marks, 
                    AVG(sm.marks) AS Average_Marks, 
                    AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                    CASE
                        WHEN AVG(sm.marks) >= 90 THEN 'A+'
                        WHEN AVG(sm.marks) >= 80 THEN 'A'
                        WHEN AVG(sm.marks) >= 70 THEN 'B'
                        WHEN AVG(sm.marks) >= 60 THEN 'C'
                        WHEN AVG(sm.marks) >= 50 THEN 'D'
                        ELSE 'F'
                    END AS Grade
                FROM students s
                LEFT JOIN student_marks sm ON s.student_id = sm.student_id
                LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
                WHERE s.Class = %s
                GROUP BY s.student_id
            """, (class_name,))

        else:
            print("Invalid choice.")
            return

        records = res.fetchall()

        if not records:
            print("No matching records found.")
        else:
            headers = ["Student ID", "Full Name", "Age", "Date of Birth", "Class",
                       "Subjects", "Marks", "Average Marks", "Percentage", "Grade"]

            table = [list(record) for record in records]

            print("\nMatching Student Records:")
            print(tabulate(table, headers, tablefmt="pretty"))


def update():
    res = conn.cursor()

    # Prompt user to enter the full name for identification
    full_name = input("Enter the Full Name of the student to update: ")

    # Check if the student with the given full name exists
    res.execute("SELECT * FROM students WHERE Full_name = %s", (full_name,))
    existing_student = res.fetchone()

    if not existing_student:
        print(f"No student found with the name '{full_name}'.")
        return

    print("\nUpdate Options:")
    print("1. Full Name")
    print("2. Age")
    print("3. Date of Birth")
    print("4. Class")
    print("\n")

    update_choice = int(input("Choose the information to update (1/2/3/4): "))

    if update_choice == 1:
        new_full_name = input("Enter the new Full Name: ")
        res.execute("UPDATE students SET Full_name = %s WHERE Full_name = %s", (new_full_name, full_name))

    elif update_choice == 2:
        new_age = input("Enter the new Age: ")
        res.execute("UPDATE students SET Age = %s WHERE Full_name = %s", (new_age, full_name))

    elif update_choice == 3:
        new_dob = input("Enter the new Date of Birth (YYYY-MM-DD): ")
        res.execute("UPDATE students SET Date_of_Birth = %s WHERE Full_name = %s", (new_dob, full_name))

    elif update_choice == 4:
        new_class = input("Enter the new Class: ")
        res.execute("UPDATE students SET Class = %s WHERE Full_name = %s", (new_class, full_name))

    else:
        print("Invalid choice.")
        return

    conn.commit()
    print("Record updated successfully.")

    res.close()

def delete():
    res = conn.cursor()

    print("\nDelete Criteria:")
    print("1. Full Name")
    print("2. Date of Birth")
    print("3. Class")
    print("\n")

    delete_choice = int(input("Choose the delete criterion (1/2/3): "))

    if delete_choice == 1:
        full_name = input("Enter Full Name to delete: ")

        # Delete corresponding records in the child table first
        res.execute("DELETE FROM student_marks WHERE student_id IN (SELECT student_id FROM students WHERE Full_name = %s)", (full_name,))
        conn.commit()

        # Then delete the student from the parent table
        res.execute("DELETE FROM students WHERE Full_name = %s", (full_name,))
        conn.commit()
    print("Record Deleted..")

    res.close()


def filter_function():
    res= conn.cursor()
    print("\nFilter Criteria:")
    print("1. Age")
    print("2. Class")
    print("3. Grade")
    print("\n")

    res= conn.cursor()
    
    filter_choice = int(input("Choose the filter criterion (1/2/3): "))

    if filter_choice == 1:
        min_age = int(input("Enter the minimum age: "))
        max_age = int(input("Enter the maximum age: "))
        res.execute("""
            SELECT 
                s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                GROUP_CONCAT(sub.subject_name) AS Subjects, 
                GROUP_CONCAT(sm.marks) AS Marks, 
                AVG(sm.marks) AS Average_Marks, 
                AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                CASE
                    WHEN AVG(sm.marks) >= 90 THEN 'A+'
                    WHEN AVG(sm.marks) >= 80 THEN 'A'
                    WHEN AVG(sm.marks) >= 70 THEN 'B'
                    WHEN AVG(sm.marks) >= 60 THEN 'C'
                    WHEN AVG(sm.marks) >= 50 THEN 'D'
                    ELSE 'F'
                END AS Grade
            FROM students s
            LEFT JOIN student_marks sm ON s.student_id = sm.student_id
            LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
            WHERE s.Age BETWEEN %s AND %s
            GROUP BY s.student_id
        """, (min_age, max_age))

    elif filter_choice == 2:
        class_name = input("Enter the class to filter: ")
        res.execute("""
            SELECT 
                s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                GROUP_CONCAT(sub.subject_name) AS Subjects, 
                GROUP_CONCAT(sm.marks) AS Marks, 
                AVG(sm.marks) AS Average_Marks, 
                AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                CASE
                    WHEN AVG(sm.marks) >= 90 THEN 'A+'
                    WHEN AVG(sm.marks) >= 80 THEN 'A'
                    WHEN AVG(sm.marks) >= 70 THEN 'B'
                    WHEN AVG(sm.marks) >= 60 THEN 'C'
                    WHEN AVG(sm.marks) >= 50 THEN 'D'
                    ELSE 'F'
                END AS Grade
            FROM students s
            LEFT JOIN student_marks sm ON s.student_id = sm.student_id
            LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
            WHERE s.Class = %s
            GROUP BY s.student_id
        """, (class_name,))

    elif filter_choice == 3:
        grade = input("Enter the grade to filter (A+, A, B, C, D, F): ")
        res.execute("""
            SELECT 
                s.student_id, s.Full_name, s.Age, s.Date_of_Birth, s.Class, 
                GROUP_CONCAT(sub.subject_name) AS Subjects, 
                GROUP_CONCAT(sm.marks) AS Marks, 
                AVG(sm.marks) AS Average_Marks, 
                AVG(sm.marks) / (COUNT(sub.subject_name) * 100) * 100 AS Percentage,
                CASE
                    WHEN AVG(sm.marks) >= 90 THEN 'A+'
                    WHEN AVG(sm.marks) >= 80 THEN 'A'
                    WHEN AVG(sm.marks) >= 70 THEN 'B'
                    WHEN AVG(sm.marks) >= 60 THEN 'C'
                    WHEN AVG(sm.marks) >= 50 THEN 'D'
                    ELSE 'F'
                END AS Grade
            FROM students s
            LEFT JOIN student_marks sm ON s.student_id = sm.student_id
            LEFT JOIN subjects sub ON sm.subject_id = sub.subject_id
            GROUP BY s.student_id
            HAVING Grade = %s
        """, (grade,))

    else:
        print("Invalid choice.")
        return

    records = res.fetchall()

    if not records:
        print("No matching records found.")
    else:
        headers = ["Student ID", "Full Name", "Age", "Date of Birth", "Class",
                   "Subjects", "Marks", "Average Marks", "Percentage", "Grade"]

        table = [list(record) for record in records]

        print("\nFiltered Student Records:")
        print(tabulate(table, headers, tablefmt="pretty"))

        # Export to JSON with custom encoder
        with open("filtered_student_records.json", "w") as json_file:
            json.dump(records, json_file, cls=CustomJSONEncoder)

        # Export to CSV
        with open("filtered_student_records.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)
            csv_writer.writerows(table)

    res.close()


while True:
    print("\n")
    print("---STUDENT MANAGEMENT SYSTEM---")
    print("1.INSERT")
    print("2.SEARCH")
    print("3.UPDATE")
    print("4.DELETE")
    print("5.DISPLAY")
    print("6.FILTER")
    print("7.EXIT")
    print("\n")

    choice = int(input("Enter Your Choice:"))
    if choice == 1:
        insert()
    elif choice == 2:
        search()
    elif choice == 3:
        update()
    elif choice == 4:
       delete()
    elif choice == 5:

        display()
    elif choice == 6:
        filter_function()
    elif choice == 7:
        quit()
    else:
        print(" Invalid option...!!!")



