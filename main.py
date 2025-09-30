"""
Console-Based Student Course Management System
Features:
- Register students
- Add/list courses (online/offline)
- Enroll student into course
- List students and their enrollments
- Save/load data to data/*.json
- Demonstrates variables, control flow, functions, OOP, error handling, file IO
"""

from student import Student
from course import Course, OnlineCourse, OfflineCourse
import utils
import sys

def print_header():
    print("="*60)
    print(" Student Course Management System (Console) ".center(60, "="))
    print("="*60)

def pause():
    input("\nPress Enter to continue...")

def list_courses(courses):
    if not courses:
        print("No courses available.")
        return
    print("\nAvailable Courses:")
    for cid, c in courses.items():
        typ = getattr(c, "platform", getattr(c, "location", "N/A"))
        ctype = "Online" if getattr(c,"platform",None) else ("Offline" if getattr(c,"location",None) else "Generic")
        print(f"ID: {cid} | {c.title} | {c.duration_weeks} weeks | ₹{c.price} | {ctype} | {typ}")

def add_course(courses):
    try:
        title = input("Course title: ").strip()
        duration = int(input("Duration (weeks): "))
        price = float(input("Price (INR): "))
        ctype = input("Type (online/offline/generic): ").strip().lower()
        cid = utils.next_course_id(courses)
        if ctype == "online":
            platform = input("Platform (eg. Zoom, Google Meet): ").strip()
            c = OnlineCourse(cid, title, duration, price, platform)
        elif ctype == "offline":
            location = input("Location (eg. Pune Center): ").strip()
            c = OfflineCourse(cid, title, duration, price, location)
        else:
            c = Course(cid, title, duration, price)
        courses[cid] = c
        utils.save_courses(courses)
        print("Course added successfully.")
    except ValueError as e:
        print("Invalid number entered. Please try again.")

def register_student(students):
    try:
        name = input("Student name: ").strip()
        email = input("Student email: ").strip()
        sid = utils.next_student_id(students)
        s = Student(sid, name, email, [])
        students[sid] = s
        utils.save_students(students)
        print(f"Student registered with ID: {sid}")
    except Exception as e:
        print("Error registering student:", e)

def enroll_student(students, courses):
    try:
        sid = int(input("Enter student ID: "))
        if sid not in students:
            print("Student not found.")
            return
        cid = int(input("Enter course ID to enroll: "))
        if cid not in courses:
            print("Course not found.")
            return
        student = students[sid]
        if cid in student.enrolled_courses:
            print("Student already enrolled in this course.")
            return
        student.enrolled_courses.append(cid)
        utils.save_students(students)
        print("Enrollment successful.")
    except ValueError:
        print("Please enter valid numeric IDs.")

def list_students(students, courses):
    if not students:
        print("No students registered.")
        return
    print("\nRegistered Students:")
    for sid, s in students.items():
        enrolled = [courses[cid].title for cid in s.enrolled_courses if cid in courses]
        print(f"ID: {sid} | {s.name} | {s.email} | Enrolled: {', '.join(enrolled) if enrolled else 'None'}")

def seed_sample_data(courses, students):
    if courses:
        return
    # Add sample courses
    c1 = OnlineCourse(utils.next_course_id(courses), "Python Basics", 6, 4999.0, "Zoom")
    courses[c1.course_id] = c1
    c2 = OfflineCourse(utils.next_course_id(courses), "Data Structures (Offline)", 8, 6999.0, "Pune Center")
    courses[c2.course_id] = c2
    utils.save_courses(courses)
    # Add sample student
    s1 = Student(utils.next_student_id(students), "Aman Kumar", "aman@example.com", [c1.course_id])
    students[s1.student_id] = s1
    utils.save_students(students)

def main():
    print_header()
    courses = utils.load_courses()
    students = utils.load_students()
    seed_sample_data(courses, students)

    while True:
        print("\nMenu:")
        print("1. List courses")
        print("2. Add course")
        print("3. Register student")
        print("4. Enroll student in course")
        print("5. List students")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            list_courses(courses)
            pause()
        elif choice == "2":
            add_course(courses)
            pause()
        elif choice == "3":
            register_student(students)
            pause()
        elif choice == "4":
            enroll_student(students, courses)
            pause()
        elif choice == "5":
            list_students(students, courses)
            pause()
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1-6.")

if __name__ == "__main__":
    main()
