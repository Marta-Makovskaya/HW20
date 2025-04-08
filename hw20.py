from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route('/',methods=['GET'])
def ping():
    return jsonify({"message":"Server is up and running!"})
@app.route('/students', methods=['GET'])
def get_students():
    students = db.get_all_students()
    return jsonify([{'id': student.student_id, 'full_name': student.full_name, 'email': student.email,
                     'data_to_start': student.data_to_start} for student in students])

@app.route('/instructors', methods=['GET'])
def get_instructors():
    instructors = db.get_all_instructors()
    return jsonify([{'id': instructor.instructor_id, 'full_name': instructor.full_name, 'email': instructor.email} for instructor in instructors])

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = db.get_all_courses()
    return jsonify([{'id': course.course_id, 'course_name': course.course_name} for course in courses])

@app.route('/students/course/<int:course_id>', methods=['GET'])
def get_students_in_course(course_id):
    students = db.get_students_in_course(course_id)
    return jsonify([{'id': student.student_id, 'full_name': student.full_name} for student in students])

@app.route('/students/instructor/<int:instructor_id>', methods=['GET'])
def get_students_by_instructor(instructor_id):
    students = db.get_students_by_instructor(instructor_id)
    return jsonify([{'id': student.student_id, 'full_name': student.full_name} for student in students])

@app.route('/students/average_grade/<int:student_id>', methods=['GET'])
def get_student_average_grade(student_id):
    average_grade = db.get_student_average_grade(student_id)
    return jsonify({'average_grade': average_grade})

@app.route('/students/details/<int:student_id>', methods=['GET'])
def get_student_details(student_id):
    details = db.get_student_details(student_id)
    return jsonify([
        {'id': student.student_id, 'full_name': student.full_name,
         'course': course.course_name if course else 'Нет курса',
         'grade': grade.grade if grade else 'Нет оценки'}
        for student, course, grade in details
    ])

@app.route('/instructors/info/<int:instructor_id>', methods=['GET'])
def get_instructor_info(instructor_id):
    instructor_info = db.get_instructor_info(instructor_id)
    return jsonify([
        {'id': instructor.instructor_id, 'full_name': instructor.full_name,
         'course': course.course_name if course else 'Нет курса',
         'student_count': student_count}
        for instructor, course, student_count in instructor_info
    ])

@app.route('/courses', methods=['POST'])
def create_course():
    course_name = request.json.get('course_name')
    db.add_course(course_name)
    return jsonify({'message': 'Курс успешно добавлен.'}), 201


@app.route('/grades', methods=['POST'])
def add_grade():
    student_id = request.json.get('student_id')
    course_id = request.json.get('course_id')
    grade = request.json.get('grade')

    print(f"Received - student_id: {student_id}, course_id: {course_id}, grade: {grade}")  

    if student_id is None or course_id is None or grade is None:
        return jsonify({"error": "Все поля должны быть заполнены."}), 400

    db.add_grade(student_id, course_id, grade)
    return jsonify({'message': 'Оценка успешно добавлена.'}), 201


@app.route('/instructors', methods=['POST'])
def create_instructor():
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    db.add_instructor(full_name, email)
    return jsonify({'message': 'Преподаватель успешно добавлен.'}), 201

@app.route('/students', methods=['POST'])
def create_student():
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    db.add_student(full_name, email)
    return jsonify({'message': 'Студент успешно добавлен.'}), 201

@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    new_name = request.json.get('new_name')
    db.edit_course(course_id, new_name)
    return jsonify({'message': 'Курс успешно отредактирован.'})

@app.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    db.soft_delete_instructor(instructor_id)
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    db.soft_delete_student(student_id)
    return jsonify({'message': 'Преподаватель успешно удален.'})

    return jsonify({'message': 'Студент успешно удален.'})

@app.route('/instructors/search', methods=['GET'])
def search_instructor():
    name_part = request.args.get('name_part')
    instructors = db.search_instructor_by_name(name_part)
    return jsonify([{'id': instructor.instructor_id, 'full_name': instructor.full_name,
                     'email': instructor.email} for instructor in instructors])

@app.route('/students/search', methods=['GET'])
def search_student():
    name_part = request.args.get('name_part')
    students = db.search_student_by_name(name_part)
    return jsonify([{'id': student.student_id, 'full_name': student.full_name,
                     'email': student.email} for student in students])

if __name__ == "__main__":
    app.run(debug=True)



