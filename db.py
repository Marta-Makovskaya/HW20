from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from sqlalchemy import func
from flask import Flask, request, jsonify


DATABASE_URL = "postgresql://postgres:Paroll1$@localhost:5432/p_g"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Instructor(Base):
    __tablename__ = 'Instructors'

    instructor_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    data_to_start = Column(DateTime, default=datetime.utcnow)
    deleted_date = Column(DateTime, nullable=True)

    courses = relationship('Course', back_populates='instructor')


class Course(Base):
    __tablename__ = 'Courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)
    instructor_id = Column(Integer, ForeignKey('Instructors.instructor_id'))
    data_to_start = Column(DateTime, default=datetime.utcnow)
    deleted_date = Column(DateTime, nullable=True)

    instructor = relationship('Instructor', back_populates='courses')
    students_courses = relationship('StudentsCourse', back_populates='course')
    grades = relationship('Grade', back_populates='course')


class Student(Base):
    __tablename__ = 'Students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(50), nullable=False)
    data_to_start = Column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_date = Column(DateTime, nullable=True)

    grades = relationship('Grade', back_populates='student')
    students_courses = relationship('StudentsCourse', back_populates='student')


class Grade(Base):
    __tablename__ = 'Grades'

    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'))
    course_id = Column(Integer, ForeignKey('Courses.course_id'))
    data_grade = Column(DateTime, default=datetime.utcnow, nullable=False)
    grade = Column(DECIMAL(3, 2), nullable=False)

    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')


class StudentsCourse(Base):
    __tablename__ = 'Students_courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('Students.student_id'))
    course_id = Column(Integer, ForeignKey('Courses.course_id'))

    student = relationship('Student', back_populates='students_courses')
    course = relationship('Course', back_populates='students_courses')



engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


def get_all_students():
    return session.query(Student).filter(Student.deleted_date.is_(None)).all()


def get_all_instructors():
    return session.query(Instructor).filter(Instructor.deleted_date.is_(None)).all()


def get_all_courses():
    return session.query(Course).filter(Course.deleted_date.is_(None)).all()


def get_students_in_course(course_id):
    return (session.query(Student.student_id, Student.full_name)
            .join(StudentsCourse)
            .filter(StudentsCourse.course_id == course_id, Student.deleted_date.is_(None)).all())


def get_students_by_instructor(instructor_id):
    return (session.query(Student.student_id, Student.full_name)
            .join(StudentsCourse)
            .join(Course)
            .filter(Course.instructor_id == instructor_id, Student.deleted_date.is_(None)).all())


def get_all_programs():
    return session.query(Program).filter(Program.deleted_date.is_(None)).all()


def get_student_average_grade(student_id):
    avg_grade = session.query(func.avg(Grade.grade)). \
        join(Student). \
        filter(Student.student_id == student_id, Student.deleted_date.is_(None)).scalar()

    return avg_grade if avg_grade is not None else 0.0


def get_student_details(student_id):
    return (session.query(Student, Course, Grade)
            .outerjoin(Grade, Student.student_id == Grade.student_id)
            .outerjoin(Course, Grade.course_id == Course.course_id)
            .filter(Student.student_id == student_id, Student.deleted_date.is_(None)).all())



def get_instructor_info(instructor_id):
    subquery = (session.query(StudentsCourse.course_id, func.count(Student.student_id).label('student_count'))
                 .join(Student, StudentsCourse.student_id == Student.student_id)
                 .group_by(StudentsCourse.course_id).subquery())

    return (session.query(Instructor, Course, subquery.c.student_count)
            .join(Course, Instructor.instructor_id == Course.instructor_id)
            .outerjoin(subquery, Course.course_id == subquery.c.course_id)
            .filter(Instructor.instructor_id == instructor_id, Instructor.deleted_date.is_(None))
            .all())


def add_course(course_name):
    existing_course = session.query(Course).filter(Course.course_name == course_name).first()

    if existing_course is None:
        new_course = Course(course_name=course_name)
        session.add(new_course)
        session.commit()
        print(f"Курс '{course_name}' успешно добавлен.")
    else:
        print(f"Курс с именем '{course_name}' уже существует.")


def add_grade(student_id, course_id, grade):
    new_grade = Grade(student_id=student_id, course_id=course_id, grade=grade)
    session.add(new_grade)
    session.commit()


def add_instructor(full_name, email):
    new_instructor = Instructor(full_name=full_name, email=email)
    session.add(new_instructor)
    session.commit()


def add_student(full_name, email):
    new_student = Student(full_name=full_name, email=email)
    session.add(new_student)
    session.commit()


def edit_course(course_id, new_name):
    course = session.query(Course).filter(Course.course_id == course_id).first()
    if course:
        course.course_name = new_name
        session.commit()


def soft_delete_instructor(instructor_id):
    instructor = session.query(Instructor).filter(Instructor.instructor_id == instructor_id).first()
    if instructor:
        instructor.deleted_date = datetime.utcnow()
        session.commit()


def soft_delete_student(student_id):
    student = session.query(Student).filter(Student.student_id == student_id).first()
    if student:
        student.deleted_date = datetime.utcnow()
        session.commit()


def search_instructor_by_name(name_part):
    return (session.query(Instructor)
            .filter(Instructor.full_name.ilike(f'%{name_part}%'), Instructor.deleted_date.is_(None)).all())


def search_student_by_name(name_part):
    return (session.query(Student)
            .filter(Student.full_name.ilike(f'%{name_part}%'), Student.deleted_date.is_(None)).all())

if __name__ == "__main__":
    init_db()