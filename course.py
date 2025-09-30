from dataclasses import dataclass, asdict

@dataclass
class Course:
    course_id: int
    title: str
    duration_weeks: int
    price: float

    def to_dict(self):
        return asdict(self)

class OnlineCourse(Course):
    def __init__(self, course_id, title, duration_weeks, price, platform):
        super().__init__(course_id, title, duration_weeks, price)
        self.platform = platform

    def to_dict(self):
        d = super().to_dict()
        d["platform"] = self.platform
        d["type"] = "online"
        return d

class OfflineCourse(Course):
    def __init__(self, course_id, title, duration_weeks, price, location):
        super().__init__(course_id, title, duration_weeks, price)
        self.location = location

    def to_dict(self):
        d = super().to_dict()
        d["location"] = self.location
        d["type"] = "offline"
        return d
