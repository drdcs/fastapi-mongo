from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_student,
    delete_student,
    retrive_student,
    retrieve_students,
    update_student
)

from app.server.models.student import(
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel
)

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")

@router.get("/{id}", response_description="Student data retrieved")
async def get_student_by_id(id):
    student = await retrive_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
