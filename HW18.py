import db

def print_menu():
    print("Выберите нужную команду:")
    print("0. Выход")
    print("1. Показать список студентов")
    print("2. Показать список преподавателей")
    print("3. Показать список курсов")
    print("4. Показать список студентов курса")
    print("5. Показать список студентов у преподавателя")
    print("6. Показать средний бал студента")
    print("7. Вывести детальную информацию по студенту (ФИО, Курс, Оценка)")
    print("8. Информация о преподавателе: ФИО, курс, студенты курса")
    print("9. Добавить курс")
    print("10. Добавить оценку")
    print("11. Добавить преподавателя")
    print("12. Добавить студента")
    print("13. Редактировать курс")
    print("14. Удалить преподавателя")
    print("15. Удалить студента")
    print("16. Поиск преподавателя по части имени")
    print("17. Поиск студента по части имени")


def show_students():
    students = db.get_all_students()
    for student in students:
        print(f"ID: {student.student_id} - Полное имя: {student.full_name}, "
              f"email: {student.email}, дата поступления: {student.data_to_start}")


def show_instructors():
    instructors = db.get_all_instructors()
    for instructor in instructors:
        print(f"ID: {instructor.instructor_id} - Полное имя: {instructor.full_name}, email: {instructor.email}")


def show_courses():
    courses = db.get_all_courses()
    for course in courses:
        print(f"ID: {course.course_id} - Название курса: {course.course_name}")


def show_students_in_course():
    course_id = int(input("Введите ID курса: "))
    students = db.get_students_in_course(course_id)
    for student in students:
        print(f"ID: {student.student_id} - Имя: {student.full_name}")


def show_students_by_instructor():
    instructor_id = int(input("Введите ID преподавателя: "))
    students = db.get_students_by_instructor(instructor_id)
    for student in students:
        print(f"ID: {student.student_id} - Имя: {student.full_name}")


def show_student_average_grade():
    student_id = int(input("Введите ID студента: "))
    average_grade = db.get_student_average_grade(student_id)
    print(f"Средний балл студента с ID {student_id}: {average_grade}")


def show_student_details():
    student_id = int(input("Введите ID студента: "))
    details = db.get_student_details(student_id)
    for student, course, grade in details:
        print(
            f"ID: {student.student_id}, ФИО: {student.full_name}, Курс: {course.course_name if course else 'Нет курса'},"
            f" Оценка: {grade.grade if grade else 'Нет оценки'}")


def show_instructor_info():
    instructor_id = int(input("Введите ID преподавателя: "))
    instructor_info = db.get_instructor_info(instructor_id)
    for instructor, course, student_count in instructor_info:
        print(
            f"ID: {instructor.instructor_id}, ФИО: {instructor.full_name}, "
            f"Курс: {course.course_name if course else 'Нет курса'}, Количество студентов: {student_count}")


def add_course():
    course_name = input("Введите название нового курса: ")
    db.add_course(course_name)



def add_grade():
    student_id = int(input("Введите ID студента: "))
    course_id = int(input("Введите ID курса: "))
    grade = float(input("Введите оценку: "))
    db.add_grade(student_id, course_id, grade)
    print("Оценка успешно добавлена.")


def add_instructor():
    full_name = input("Введите полное имя преподавателя: ")
    email = input("Введите email преподавателя: ")
    db.add_instructor(full_name, email)
    print("Преподаватель успешно добавлен.")


def add_student():
    full_name = input("Введите полное имя студента: ")
    email = input("Введите email студента: ")
    db.add_student(full_name, email)
    print("Студент успешно добавлен.")


def edit_course():
    course_id = int(input("Введите ID курса для редактирования: "))
    new_name = input("Введите новое название курса: ")
    db.edit_course(course_id, new_name)
    print("Курс успешно отредактирован.")


def delete_instructor():
    instructor_id = int(input("Введите ID преподавателя для удаления: "))
    db.soft_delete_instructor(instructor_id)
    print("Преподаватель успешно удален.")


def delete_student():
    student_id = int(input("Введите ID студента для удаления: "))
    db.soft_delete_student(student_id)
    print("Студент успешно удален.")


def search_instructor_by_name():
    name_part = input("Введите часть имени преподавателя для поиска: ")
    instructors = db.search_instructor_by_name(name_part)
    if instructors:
        for instructor in instructors:
            print(f"ID: {instructor.instructor_id}, ФИО: {instructor.full_name}, email: {instructor.email}")
    else:
        print("Такой преподаватель не найден.")


def search_student_by_name():
    name_part = input("Введите часть имени студента для поиска: ")
    students = db.search_student_by_name(name_part)
    if students:
        for student in students:
            print(f"ID: {student.student_id}, ФИО: {student.full_name}, email: {student.email}")
    else:
        print("Такой студент не найден.")


def app():
    db.init_db()
    print("База данных успешно инициализирована.")

    while True:
        print_menu()
        cmd = int(input("Введите номер команды: "))

        if cmd == 0:
            print("До свидания!")
            break
        elif cmd == 1:
            show_students()
        elif cmd == 2:
            show_instructors()
        elif cmd == 3:
            show_courses()
        elif cmd == 4:
            show_students_in_course()
        elif cmd == 5:
            show_students_by_instructor()
        elif cmd == 6:
            show_student_average_grade()
        elif cmd == 7:
            show_student_details()
        elif cmd == 8:
            show_instructor_info()
        elif cmd == 9:
            add_course()
        elif cmd == 10:
            add_grade()
        elif cmd == 11:
            add_instructor()
        elif cmd == 12:
            add_student()
        elif cmd == 13:
            edit_course()
        elif cmd == 14:
            delete_instructor()
        elif cmd == 15:
            delete_student()
        elif cmd == 16:
            search_instructor_by_name()
        elif cmd == 17:
            search_student_by_name()
        else:
            print("Неправильная команда, попробуйте снова.")


if __name__ == "__main__":
    app()