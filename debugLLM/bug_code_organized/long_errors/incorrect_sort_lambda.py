def sort_students(students):
	students.sort(key=lambda student: student['name'] > 'Smith')

students = [
	{'name': 'John', 'age': 20},
	{'name': 'Alice', 'age': 22},
	{'name': 'Bob', 'age': 21}
]
sort_students(students)
print(students)