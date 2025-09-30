import json, os
from typing import Dict, List
from student import Student
from course import Course, OnlineCourse, OfflineCourse

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_students() -> Dict[int, Student]:
    rows = load_json(STUDENTS_FILE)
    students = {}
    for r in rows:
        students[r["student_id"]] = Student(
            student_id=r["student_id"],
            name=r["name"],
            email=r["email"],
            enrolled_courses=r.get("enrolled_courses", [])
        )
    return students

def save_students(students: Dict[int, Student]):
    rows = [s.to_dict() for s in students.values()]
    save_json(STUDENTS_FILE, rows)

def load_courses():
    rows = load_json(COURSES_FILE)
    courses = {}
    for r in rows:
        t = r.get("type")
        if t == "online":
            c = OnlineCourse(r["course_id"], r["title"], r["duration_weeks"], r["price"], r.get("platform",""))
        elif t == "offline":
            c = OfflineCourse(r["course_id"], r["title"], r["duration_weeks"], r["price"], r.get("location",""))
        else:
            c = Course(r["course_id"], r["title"], r["duration_weeks"], r["price"])
        courses[r["course_id"]] = c
    return courses

def save_courses(courses: Dict[int, Course]):
    rows = []
    for c in courses.values():
        if hasattr(c, "to_dict"):
            rows.append(c.to_dict())
        else:
            rows.append({
                "course_id": c.course_id,
                "title": c.title,
                "duration_weeks": c.duration_weeks,
                "price": c.price,
                "type": "generic"
            })
    save_json(COURSES_FILE, rows)

def next_student_id(students: Dict[int, Student]) -> int:
    return max(students.keys(), default=0) + 1

def next_course_id(courses: Dict[int, Course]) -> int:
    return max(courses.keys(), default=0) + 1
