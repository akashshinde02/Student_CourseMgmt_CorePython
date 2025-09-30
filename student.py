from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Student:
    student_id: int
    name: str
    email: str
    enrolled_courses: List[int]

    def to_dict(self):
        return asdict(self)
