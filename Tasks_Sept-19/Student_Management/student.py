from person import Person

class Student(Person):
    def __init__(self, id, name, age, grade, marks):
        super().__init__(name, age)
        self.id = id
        self.grade = grade
        self.marks = marks
    
    def get_average(self):
        """Calculate and return average marks"""
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)
    
    def get_highest_subject(self):
        """Return the subject with the highest marks"""
        if not self.marks:
            return None
        return max(self.marks, key=self.marks.get)
    
    def __str__(self):
        return f"ID: {self.id}, {super().__str__()}, Grade: {self.grade}, Average: {self.get_average():.2f}"