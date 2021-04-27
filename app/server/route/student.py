from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
# from app.server.kafka_io.aio_producer import AIOProducer
# from app.server.kafka_io import kafka_conn
from app.server.kafka_io.kafka_conn import aioproducer
import json

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
    await aioproducer.send("pymongo", json.dumps(new_student).encode('ascii'))
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}", response_description="Retrive a single Student")
async def get_student_by_id(id):
    student = await retrive_student(id)
    if student:
        return ResponseModel(student, message= f"Successfully retrive the student of {id}")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    await aioproducer.send("pymongo", json.dumps(deleted_student).encode('ascii'))
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )

@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel= Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    await aioproducer.send("pymongo", json.dumps(updated_student).encode('ascii'))
    if updated_student:
        return ResponseModel("Student with ID: {} removed".format(id),"Student name updated successfully")
    return ErrorResponseModel(
        "An error occured ",
        404,
        "There was an error updating the student data."
    )