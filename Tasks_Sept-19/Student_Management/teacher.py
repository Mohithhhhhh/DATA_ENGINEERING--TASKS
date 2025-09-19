from person import Person

class Teacher(Person):
    def __init__(self, id, name, subject, salary):
        super().__init__(name, age=None)  # Age not provided in CSV
        self.id = id
        self.subject = subject
        self.salary = salary
    
    def get_details(self):
        """Return formatted string with teacher info"""
        return f"ID: {self.id}, Name: {self.name}, Subject: {self.subject}, Salary: ₹{self.salary}"
    
    def __str__(self):
        return self.get_details()