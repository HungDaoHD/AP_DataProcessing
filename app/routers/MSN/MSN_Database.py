import motor.motor_asyncio
from bson.objectid import ObjectId


class MsnPrj:

    def __init__(self):
        MONGO_DETAILS = 'mongodb://localhost:27017'

        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

        db_msn = client.msn

        self.prj_collection = db_msn.get_collection('projects')


    @staticmethod
    def prj_info(prj, isShort) -> dict:
        if isShort:
            return {
                'id': str(prj['_id']),
                'prj_id': prj['prj_id'],
                'name': prj['name'],
                'categorical': prj['categorical'],
                'status': prj['status']
            }
        else:
            return {
                'id': str(prj['_id']),
                'prj_id': prj['prj_id'],
                'name': prj['name'],
                'categorical': prj['categorical'],
                'status': prj['status'],
                'detail': prj['detail']
            }


    async def retrieve(self):
        lst_prj = []
        async for prj in self.prj_collection.find():
            lst_prj.append(self.prj_info(prj, True))

        overView = {
            'total': len(lst_prj),
            'completed': 0,
            'on_going': 0,
            'pending_cancel': 0,
        }

        for item in lst_prj:
            if item['status'] in ['Completed']:
                overView['completed'] += 1
            elif item['status'] in ['On Going']:
                overView['on_going'] += 1
            elif item['status'] in ['Pending', 'Cancel']:
                overView['pending_cancel'] += 1

        return lst_prj, overView


    async def retrieve_id(self, _id: str) -> dict:
        prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

        prj = self.prj_info(prj, False)

        return prj





























#
#
# def course_helper(course) -> dict:
#     return {
#         "id": str(course["_id"]),
#         "name": course["name"],
#     }
#
#
# # Retrieve all students present in the database
# async def retrieve_students():
#     students = []
#     async for student in student_collection.find():
#
#         dictStudent = student_helper(student)
#
#         dictCourse = await courseOfStudy.find_one({'_id': student['course'].id})
#         dictStudent['course'] = course_helper(dictCourse)
#
#         students.append(dictStudent)
#     return students
#
#
# # Add a new student into to the database
# async def add_student(student_data: dict) -> dict:
#     student = await student_collection.insert_one(student_data)
#     new_student = await student_collection.find_one({"_id": student.inserted_id})
#     return student_helper(new_student)
#
#
# # Retrieve a student with a matching ID
# async def retrieve_student(id: str) -> dict:
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#
#     dictStudent = student_helper(student)
#     dictCourse = await courseOfStudy.find_one({'_id': student['course'].id})
#     dictStudent['course'] = course_helper(dictCourse)
#
#     if dictStudent:
#         return dictStudent
#
#
# # Update a student with a matching ID
# async def update_student(id: str, data: dict):
#     # Return false if an empty request body is sent.
#     if len(data) < 1:
#         return False
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         updated_student = await student_collection.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_student:
#             return True
#         return False
#
#
# # Delete a student from the database
# async def delete_student(id: str):
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         await student_collection.delete_one({"_id": ObjectId(id)})
#         return True


