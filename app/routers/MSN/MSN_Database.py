import motor.motor_asyncio
from bson.objectid import ObjectId
import re
import json
from ...classes.AP_DataConverter import APDataConverter
import pandas as pd
import traceback


class MsnPrj:

    def __init__(self):
        # MONGO_DETAILS = 'mongodb://localhost:27017'
        MONGO_DETAILS = 'mongodb+srv://hungdao:Hung123456@cluster0.m1qzy.mongodb.net/test'

        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

        db_msn = client.msn

        self.prj_collection = db_msn.get_collection('projects')


    @staticmethod
    def prj_info(prj, isShort) -> dict:
        if isShort:
            return {
                'id': str(prj['_id']),
                'internal_id': prj['internal_id'],
                'name': prj['name'],
                'categorical': prj['categorical'],
                'status': prj['status']
            }
        else:
            return {
                'id': str(prj['_id']),
                'internal_id': prj['internal_id'],
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

        if prj:
            prj = self.prj_info(prj, False)

        return prj



    async def update_prj(self, _id: str, strBody: str):

        data = self.body_to_json(strBody)

        if len(data) < 1:
            return False

        prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

        if prj:

            prj_updated = await self.prj_collection.update_one(
                {'_id': ObjectId(_id)}, {'$set': data}
            )

            if prj_updated:
                return True

            return False


    @staticmethod
    def body_to_json(strBody: str):
        re_json = re.compile(r'\{"output".+}')
        str_json = re_json.search(strBody).group()
        dictBody = dict(json.loads(str_json))
        dictBody.pop('output')

        updateData = dict()
        for key, val in dictBody.items():
            if val is not None:

                if str(val).lower() in ['true', 'false']:
                    upVal = True if str(val).lower() == 'true' else False
                else:
                    upVal = val

                if '.' in key:
                    parentKey = str(key).rsplit('.', 1)[0]
                    childKey = str(key).rsplit('.', 1)[1]

                    if parentKey in ['detail.oe_combine_cols', 'detail.scr_cols', 'detail.product_cols', 'detail.fc_cols']:

                        if updateData:
                            updateData[parentKey][childKey] = upVal
                        else:
                            updateData = {
                                parentKey:
                                    {
                                        childKey: upVal
                                    }
                            }

                    elif 'detail.addin_vars' in parentKey:

                        lstKey = str(key).rsplit('.')

                        parentKey2 = '.'.join(lstKey[:2])
                        varIdx = lstKey[2]
                        varAtt = lstKey[3]

                        catIdx, catAtt = None, None
                        if len(lstKey) > 4:
                            catIdx = lstKey[4]
                            catAtt = lstKey[5]

                        if parentKey2 not in updateData.keys():
                            updateData[parentKey2] = dict()

                        if varIdx not in updateData[parentKey2].keys():
                            updateData[parentKey2][varIdx] = dict()

                        if varAtt not in updateData[parentKey2][varIdx].keys():
                            updateData[parentKey2][varIdx][varAtt] = dict()

                        if varAtt in ['name', 'lbl']:
                            updateData[parentKey2][varIdx][varAtt] = upVal
                        else:
                            if catIdx not in updateData[parentKey2][varIdx][varAtt].keys():
                                updateData[parentKey2][varIdx][varAtt][catIdx] = dict()

                            updateData[parentKey2][varIdx][varAtt][catIdx][catAtt] = upVal

                    elif 'topline_design.header' in parentKey:
                        lstKey = str(key).rsplit('.')
                        parentKey2 = '.'.join(lstKey[:3])
                        varIdx = lstKey[3]

                        if parentKey2 not in updateData.keys():
                            updateData[parentKey2] = dict()

                        if varIdx not in updateData[parentKey2].keys():
                            updateData[parentKey2][varIdx] = dict()

                        if isinstance(upVal, list):
                            updateData[parentKey2][varIdx] = {
                              'name': upVal[0],
                              'lbl': upVal[1],
                              'hidden_cats': upVal[2],
                            }

                        else:
                            varAtt = lstKey[4]
                            updateData[parentKey2][varIdx][varAtt] = upVal

                    elif 'topline_design.side' in parentKey:

                        lstKey = str(key).rsplit('.')
                        parentKey2 = '.'.join(lstKey[:3])
                        varIdx = lstKey[3]

                        if parentKey2 not in updateData.keys():
                            updateData[parentKey2] = dict()

                        if varIdx not in updateData[parentKey2].keys():
                            updateData[parentKey2][varIdx] = {
                                'name': '',
                                'group_lbl': '',
                                'lbl': '',
                                'type': '',
                                't2b': False,
                                'b2b': False,
                                'mean': False,
                                'ma_cats': '',
                                'hidden_cats': '',
                                'is_count': False,
                                'is_corr': False,
                                'is_ua': False
                            }

                        if isinstance(upVal, list):

                            lstAttKey = updateData[parentKey2][varIdx].keys()
                            for idx_AttKey, val_AttKey in enumerate(lstAttKey):

                                if str(upVal[idx_AttKey]).lower() in ['true', 'false']:
                                    newUpVal = True if str(upVal[idx_AttKey]).lower() == 'true' else False
                                else:
                                    newUpVal = upVal[idx_AttKey]

                                updateData[parentKey2][varIdx][val_AttKey] = newUpVal

                        else:
                            varAtt = lstKey[4]
                            updateData[parentKey2][varIdx][varAtt] = upVal

                    else:
                        updateData[key] = upVal
                else:
                    updateData[key] = upVal

        return updateData


    async def upload_prj_data(self, _id: str, file_scr, file_main):

        try:

            apCvt = APDataConverter()

            apCvt.load(file_scr)

            scr_data = apCvt.dictData
            scr_varLbl = apCvt.dictVarLbl
            scr_valLbl = {k: {str(k2): v2 for k2, v2 in v.items()} for k, v in apCvt.dictValLbl.items()}

            apCvt.load(file_main)

            main_data = apCvt.dictData
            main_varLbl = apCvt.dictVarLbl
            main_valLbl = {k: {str(k2): v2 for k2, v2 in v.items()} for k, v in apCvt.dictValLbl.items()}

            if not scr_data or not main_data:
                return False

            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            if prj:

                data = {
                    'screener': {
                        'data': scr_data,
                        'varLbl': scr_varLbl,
                        'valLbl': scr_valLbl
                    },
                    'main': {
                        'data': main_data,
                        'varLbl': main_varLbl,
                        'valLbl': main_valLbl
                    }
                }

                upload_prj_data = await self.prj_collection.update_one(
                    {'_id': ObjectId(_id)}, {'$set': data}
                )

                if upload_prj_data:
                    return True

                return False

        except Exception:
            print(traceback.format_exc())
            return False




























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


