import json
import csv
import os
from student import Student
from teacher import Teacher

class SchoolManagementSystem:
    def __init__(self):
        self.students = []
        self.teachers = []
    
    def load_students(self):
        """Load students from JSON file"""
        try:
            with open('students.json', 'r') as file:
                students_data = json.load(file)
                for student_data in students_data:
                    student = Student(
                        student_data['id'],
                        student_data['name'],
                        student_data['age'],
                        student_data['grade'],
                        student_data['marks']
                    )
                    self.students.append(student)
            print("Students loaded successfully!")
        except FileNotFoundError:
            print("Students file not found.")
        except Exception as e:
            print(f"Error loading students: {e}")
    
    def load_teachers(self):
        """Load teachers from CSV file"""
        try:
            with open('teachers.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    teacher = Teacher(
                        int(row['id']),
                        row['name'],
                        row['subject'],
                        float(row['salary'])
                    )
                    self.teachers.append(teacher)
            print("Teachers loaded successfully!")
        except FileNotFoundError:
            print("Teachers file not found.")
        except Exception as e:
            print(f"Error loading teachers: {e}")
    
    def save_students(self):
        """Save students to JSON file"""
        try:
            students_data = []
            for student in self.students:
                student_data = {
                    'id': student.id,
                    'name': student.name,
                    'age': student.age,
                    'grade': student.grade,
                    'marks': student.marks
                }
                students_data.append(student_data)
            
            with open('students.json', 'w') as file:
                json.dump(students_data, file, indent=2)
            print("Students saved successfully!")
        except Exception as e:
            print(f"Error saving students: {e}")
    
    def save_teachers(self):
        """Save teachers to CSV file"""
        try:
            with open('teachers.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'subject', 'salary'])
                for teacher in self.teachers:
                    writer.writerow([teacher.id, teacher.name, teacher.subject, teacher.salary])
            print("Teachers saved successfully!")
        except Exception as e:
            print(f"Error saving teachers: {e}")
    
    def print_all_students(self):
        """Print all students with their details and average marks"""
        print("\n=== ALL STUDENTS ===")
        for student in self.students:
            print(f"{student}")
    
    def print_all_teachers(self):
        """Print all teachers with their details"""
        print("\n=== ALL TEACHERS ===")
        for teacher in self.teachers:
            print(teacher.get_details())
    
    def find_student_topper(self):
        """Find and return the student with the highest average marks"""
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.get_average())
    
    def add_new_student(self):
        """Add a new student to the system"""
        print("\n=== ADD NEW STUDENT ===")
        
        try:
            # Get student details
            student_id = max([s.id for s in self.students], default=0) + 1
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            grade = input("Enter student grade: ")
            
            # Get marks for each subject
            marks = {}
            print("Enter marks for each subject (leave blank to finish):")
            while True:
                subject = input("Subject: ").strip()
                if not subject:
                    break
                mark = float(input(f"Mark for {subject}: "))
                marks[subject] = mark
            
            # Create and add student
            new_student = Student(student_id, name, age, grade, marks)
            self.students.append(new_student)
            
            # Save to file
            self.save_students()
            print(f"Student {name} added successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"Error adding student: {e}")
    
    def add_new_teacher(self):
        """Add a new teacher to the system"""
        print("\n=== ADD NEW TEACHER ===")
        
        try:
            # Get teacher details
            teacher_id = max([t.id for t in self.teachers], default=0) + 1
            name = input("Enter teacher name: ")
            subject = input("Enter subject: ")
            salary = float(input("Enter salary: "))
            
            # Create and add teacher
            new_teacher = Teacher(teacher_id, name, subject, salary)
            self.teachers.append(new_teacher)
            
            # Save to file
            self.save_teachers()
            print(f"Teacher {name} added successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"Error adding teacher: {e}")
    
    def get_average_teacher_salary(self):
        """Calculate and return the average salary of all teachers"""
        if not self.teachers:
            return 0
        return sum(t.salary for t in self.teachers) / len(self.teachers)
    
    def find_highest_paid_teacher(self):
        """Find and return the teacher with the highest salary"""
        if not self.teachers:
            return None
        return max(self.teachers, key=lambda t: t.salary)
    
    def generate_student_teacher_report(self):
        """Generate report showing each student's name and their class teacher"""
        print("\n=== STUDENT-TEACHER REPORT ===")
        
        if not self.students or not self.teachers:
            print("No data available for report.")
            return
        
        for student in self.students:
            highest_subject = student.get_highest_subject()
            if highest_subject:
                # Find teacher for this subject
                subject_teachers = [t for t in self.teachers if t.subject.lower() == highest_subject.lower()]
                if subject_teachers:
                    teacher_name = subject_teachers[0].name
                else:
                    teacher_name = "No teacher found"
            else:
                teacher_name = "No subjects found"
            
            print(f"{student.name} (Highest Subject: {highest_subject}) - Class Teacher: {teacher_name}")
    
    def generate_summary_report(self):
        """Generate summary report with various statistics"""
        print("\n=== SUMMARY REPORT ===")
        
        # Total number of students per grade
        grade_counts = {}
        for student in self.students:
            if student.grade in grade_counts:
                grade_counts[student.grade] += 1
            else:
                grade_counts[student.grade] = 1
        
        print("\nStudents per Grade:")
        for grade, count in grade_counts.items():
            print(f"Grade {grade}: {count} students")
        
        # Average marks in each subject across all students
        subject_marks = {}
        subject_counts = {}
        for student in self.students:
            for subject, mark in student.marks.items():
                if subject in subject_marks:
                    subject_marks[subject] += mark
                    subject_counts[subject] += 1
                else:
                    subject_marks[subject] = mark
                    subject_counts[subject] = 1
        
        print("\nAverage Marks per Subject:")
        for subject, total_marks in subject_marks.items():
            avg_marks = total_marks / subject_counts[subject]
            print(f"{subject}: {avg_marks:.2f}")
        
        # Total salary spent on teachers
        total_salary = sum(t.salary for t in self.teachers)
        print(f"\nTotal Salary Spent on Teachers: ₹{total_salary:.2f}")
    
    def run_menu(self):
        """Run the main menu interface"""
        # Load data
        self.load_students()
        self.load_teachers()
        
        while True:
            print("\n=== SCHOOL MANAGEMENT SYSTEM ===")
            print("1. View All Students")
            print("2. View All Teachers")
            print("3. Add New Student")
            print("4. Add New Teacher")
            print("5. Generate Student-Teacher Report")
            print("6. Generate Summary Report")
            print("7. Show Statistics")
            print("8. Exit")
            
            choice = input("Enter your choice (1-8): ")
            
            if choice == '1':
                self.print_all_students()
            
            elif choice == '2':
                self.print_all_teachers()
            
            elif choice == '3':
                self.add_new_student()
            
            elif choice == '4':
                self.add_new_teacher()
            
            elif choice == '5':
                self.generate_student_teacher_report()
            
            elif choice == '6':
                self.generate_summary_report()
            
            elif choice == '7':
                print("\n=== STATISTICS ===")
                
                # Student topper
                topper = self.find_student_topper()
                if topper:
                    print(f"Top Student: {topper.name} (Average: {topper.get_average():.2f})")
                
                # Highest paid teacher
                highest_paid = self.find_highest_paid_teacher()
                if highest_paid:
                    print(f"Highest Paid Teacher: {highest_paid.name} (Salary: ₹{highest_paid.salary:.2f})")
                
                # Average teacher salary
                avg_salary = self.get_average_teacher_salary()
                print(f"Average Teacher Salary: ₹{avg_salary:.2f}")
                
                # Student count
                print(f"Total Students: {len(self.students)}")
                print(f"Total Teachers: {len(self.teachers)}")
            
            elif choice == '8':
                print("Thank you for using the School Management System!")
                break
            
            else:
                print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    system = SchoolManagementSystem()
    system.run_menu()