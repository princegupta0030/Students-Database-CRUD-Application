from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Optional
import sqlite3
from .database import init_db, get_db_connection
from .models import StudentCreate, StudentResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Database CRUD Application!"}

@app.get("/students", response_model=list[StudentResponse])
def get_students(name: Optional[str] = None, email: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM students"
    conditions = []
    params = []

    if name:
        conditions.append("name LIKE ?")
        params.append(f"%{name}%")
    if email:
        conditions.append("email LIKE ?")
        params.append(f"%{email}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    students = cursor.fetchall()
    conn.close()

    return [dict(student) for student in students]

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(student)

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if student exists
    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        cursor.execute(
            """
            UPDATE students
            SET name = ?, date_of_birth = ?, email = ?, phone = ?, course = ?, address = ?, enrollment_date = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.date_of_birth,
                student.email,
                student.phone,
                student.course,
                student.address,
                student.enrollment_date,
                student_id
            )
        )
        conn.commit()

        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        updated_student = cursor.fetchone()

    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: students.email" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail="Database integrity error")
    finally:
        conn.close()

    return dict(updated_student)

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return {"message": "Student deleted successfully"}

@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, date_of_birth, email, phone, course, address, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student.name,
                student.date_of_birth,
                student.email,
                student.phone,
                student.course,
                student.address,
                student.enrollment_date
            )
        )
        conn.commit()
        student_id = cursor.lastrowid

        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        new_student = cursor.fetchone()

    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: students.email" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail="Database integrity error")
    finally:
        conn.close()

    return dict(new_student)
