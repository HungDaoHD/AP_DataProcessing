import motor.motor_asyncio
import pandas as pd
from bson.objectid import ObjectId
from datetime import datetime
import re
import json
import traceback
from .MSN_Data_Converter import QMeFileConvert
from .MSN_Export_Data import ExportMSNData
from .MSN_Topline_Exporter import ToplineExporter
from .MSN_Models import new_prj_template



class MsnPrj:

    def __init__(self):
        # MONGO_DETAILS = 'mongodb://localhost:27017'
        MONGO_DETAILS = 'mongodb+srv://hungdao:Hung123456@cluster0.m1qzy.mongodb.net/test'
        
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

        db_msn = client.msn

        self.prj_collection = db_msn.get_collection('projects')
        self.user_collection = db_msn.get_collection('users')


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
            sec_topline_exporter = dict()
            if not prj['topline_exporter']:
                sec_topline_exporter = {}
            else:
                for key, val in prj['topline_exporter'].items():
                    if val:
                        strSecName = prj['detail']['sections'][str(key)]['name']
                        sec_topline_exporter.update({str(key): strSecName})

            lenOfScr = len(prj['screener']['data']) if prj['screener'] else 0
            lenOfMain = len(prj['main']['data']) if prj['main'] else 0

            return {
                'id': str(prj['_id']),
                'internal_id': prj['internal_id'],
                'name': prj['name'],
                'categorical': prj['categorical'],
                'status': prj['status'],
                'detail': prj['detail'],
                'lenOfScr': lenOfScr,
                'lenOfMain': lenOfMain,
                'sec_topline_exporter': sec_topline_exporter
            }

    @staticmethod
    def get_overView(lst_prj: list):
        overView = {
            'total': len(lst_prj),
            'completed': 0,
            'on_going': 0,
            'pending_cancel': 0,
        }

        # for item in lst_prj:
        #     if item['status'] in ['Completed']:
        #         overView['completed'] += 1
        #     elif item['status'] in ['On Going']:
        #         overView['on_going'] += 1
        #     elif item['status'] in ['Pending', 'Cancel']:
        #         overView['pending_cancel'] += 1

        return overView


    @staticmethod
    def count_page(lst_prj, step):
        tuple_divMod = divmod(len(lst_prj), step)

        if tuple_divMod[1] != 0:
            page_count = tuple_divMod[0] + 1
        else:
            page_count = tuple_divMod[0]

        return page_count


    async def retrieve(self, page):
        try:

            lst_prj = list()
            async for prj in self.prj_collection.find().sort('create_date', -1):
                lst_prj.append(self.prj_info(prj, True))

            overView = self.get_overView(lst_prj)

            step = 5
            page_count = self.count_page(lst_prj, step)

            lst_prj = lst_prj[((page - 1) * step):(page * step)]

            return {
                'isSuccess': True,
                'strErr': None,
                'lst_prj': lst_prj,
                'overView': overView,
                'page_count': page_count
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc(),
                'lst_prj': None,
                'overView': None,
                'page_count': None
            }


    async def search(self, prj_name: str = ''):
        try:

            lst_prj = list()
            async for prj in self.prj_collection.find({'name': {'$regex': f'.*{prj_name}.*', '$options': 'i'}}).sort('create_date', -1):
                lst_prj.append(self.prj_info(prj, True))

            overView = self.get_overView(lst_prj)

            step = 10
            page_count = self.count_page(lst_prj, step)

            return {
                'isSuccess': True,
                'strErr': None,
                'lst_prj': lst_prj,
                'overView': overView,
                'page_count': page_count
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc(),
                'lst_prj': None,
                'overView': None,
                'page_count': None
            }


    async def add(self, internal_id, prj_name, categorical, prj_status):
        try:

            new_prj = new_prj_template
            new_prj['_id'] = ObjectId()
            new_prj['internal_id'] = internal_id
            new_prj['name'] = prj_name
            new_prj['categorical'] = categorical
            new_prj['status'] = prj_status
            new_prj['create_date'] = datetime.now()

            prj = await self.prj_collection.insert_one(new_prj)

            if not prj:
                return {
                    'isSuccess': False,
                    'strErr': 'Add projects error'
                }

            return {
                'isSuccess': True,
                'strErr': None
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }


    async def delete(self, _id):
        try:

            prj = await self.prj_collection.delete_one({'_id': ObjectId(_id)})

            if not prj:
                return {
                    'isSuccess': False,
                    'strErr': 'Delete projects error'
                }

            return {
                'isSuccess': True,
                'strErr': None
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }


    async def retrieve_id(self, _id: str) -> dict:
        try:

            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            if prj:
                prj = self.prj_info(prj, False)

            return {
                'isSuccess': True,
                'strErr': None,
                'prj': prj
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc(),
                'prj': None
            }


    async def update_prj(self, _id: str, strBody: str):

        try:

            data = self.body_to_json(strBody)

            if len(data) < 1:
                return {
                    'isSuccess': False,
                    'strErr': 'Data is null'
                }

            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            if prj:

                prj_updated = await self.prj_collection.update_one(
                    {'_id': ObjectId(_id)}, {'$set': data}
                )

                if prj_updated:
                    return {
                        'isSuccess': True,
                        'strErr': None
                    }

            return {
                'isSuccess': False,
                'strErr': 'Cannot update'
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }



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
                                'group_lbl': '',
                                'name': '',
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

            cvter = QMeFileConvert()
            scr_data, scr_varLbl, scr_valLbl = cvter.convert(file_scr)
            main_data, main_varLbl, main_valLbl = cvter.convert(file_main)

            if not scr_data or not main_data:
                return {
                    'isSuccess': False,
                    'strErr': 'Data is null'
                }

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
                    return {
                        'isSuccess': True,
                        'strErr': 'Upload successfully'
                    }

            return {
                'isSuccess': False,
                'strErr': 'Upload unsuccessfully'
            }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }



    async def clear_prj_data(self, _id: str):

        try:
            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            if prj:

                data = {
                    'screener': {
                        'data': {},
                        'varLbl': {},
                        'valLbl': {}
                    },
                    'main': {
                        'data': {},
                        'varLbl': {},
                        'valLbl': {}
                    }
                }

                clear_prj_data = await self.prj_collection.update_one(
                    {'_id': ObjectId(_id)}, {'$set': data}
                )

                if clear_prj_data:
                    return {
                        'isSuccess': True,
                        'strErr': 'Upload successfully'
                    }

            return {
                    'isSuccess': False,
                    'strErr': 'Upload unsuccessfully'
                }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }


    async def data_export(self, _id: str, export_section):

        try:
            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            exp_data = ExportMSNData(prj=prj, isExportSPCode=False, export_section=export_section, isExportForceChoiceYN=False)

            isSuccess = exp_data.export_data()

            if not isSuccess[0]:
                return {
                    'isSuccess': False,
                    'strErr': isSuccess[1],
                    'zipName': None
                }

            return {
                    'isSuccess': True,
                    'strErr': None,
                    'zipName': exp_data.zipName
                }

        except Exception:
            return {
                'isSuccess': False,
                'strErr': traceback.format_exc(),
                'zipName': None
            }


    async def topline_process(self, _id: str, export_section):

        try:
            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            exp_data = ExportMSNData(prj=prj, isExportSPCode=False, export_section=export_section, isExportForceChoiceYN=True)

            isSuccess = exp_data.export_dfOnly()
            if not isSuccess[0]:
                return {
                    'isSuccess': False,
                    'strErr': isSuccess[1]
                }

            if prj:
                prj = self.prj_info(prj, False)

            dfUnstacked = exp_data.dfUnstacked
            dfStacked = exp_data.dfStacked
            dictUnstack_column_labels = exp_data.dictUnstack_column_labels
            dictUnstack_variable_value_labels = exp_data.dictUnstack_variable_value_labels
            lstSPCodes = [int(i) for i in exp_data.lstSPCodes]

            exp_data = None

            exp_topline = ToplineExporter(prj=prj, df=dfUnstacked,
                                          dfCorr=dfStacked,
                                          dictVarName=dictUnstack_column_labels,
                                          dictValLbl=dictUnstack_variable_value_labels,
                                          lstSPCodes=lstSPCodes,
                                          export_section=export_section)

            isSuccess = exp_topline.getInfo_RunSig()
            if not isSuccess[0]:
                return {
                    'isSuccess': False,
                    'strErr': isSuccess[1]
                }

            json_Ttest = json.dumps(exp_topline.dictTtest)
            json_UA = json.dumps(exp_topline.dictUA)

            topline_exporter_data = {
                export_section: {
                        'Ttest': json_Ttest,
                        'UA': json_UA,
                        'dfStacked': json.dumps(dfStacked.to_dict('records')),
                        'dictSide': json.dumps(exp_topline.dictSide)
                    }
                }

            exp_topline = None

            upload_prj_Ttest_UA = await self.prj_collection.update_one(
                {'_id': ObjectId(_id)}, {'$set': {
                        'topline_exporter': topline_exporter_data
                    }
                }
            )

            if not upload_prj_Ttest_UA:
                return {
                    'isSuccess': False,
                    'strErr': 'Upload Test & UA failed'
                }

            return {
                    'isSuccess': True,
                    'strErr': None
                }

        except Exception:

            return {
                'isSuccess': False,
                'strErr': traceback.format_exc()
            }


    async def topline_export(self, _id: str, export_section, strHow):

        try:
            prj = await self.prj_collection.find_one({'_id': ObjectId(_id)})

            dfCorr = pd.DataFrame(json.loads(prj['topline_exporter'][export_section]['dfStacked']))
            dictSide = json.loads(prj['topline_exporter'][export_section]['dictSide'])
            dictTtest = json.loads(prj['topline_exporter'][export_section]['Ttest'])
            dictUA = json.loads(prj['topline_exporter'][export_section]['UA'])

            if prj:
                prj = self.prj_info(prj, False)

            exp_topline = ToplineExporter(prj=prj,
                                          df=pd.DataFrame(),
                                          dfCorr=dfCorr,
                                          dictVarName=dict(),
                                          dictValLbl=dict(),
                                          lstSPCodes=list(),
                                          export_section=export_section)

            exp_topline.dictSide = dictSide
            exp_topline.dictTtest = dictTtest
            exp_topline.dictUA = dictUA

            if strHow in ['PRODUCTS_1']:

                isSuccess = exp_topline.toExcel_Product_1()

            elif strHow in ['PRODUCTS_2']:

                isSuccess = exp_topline.toExcel_Product_2()

            elif strHow in ['UA_CORR']:

                isSuccess = exp_topline.toExcel_UA_Corr()

            elif strHow in ['HAND']:
                isSuccess = exp_topline.toExcel_Handcount()

            else:
                isSuccess = exp_topline.toExcel()


            if not isSuccess[0]:
                return {
                    'isSuccess': False,
                    'strErr': isSuccess[1],
                    'zipName': None
                }

            if strHow in ['FULL', 'UA_CORR', 'HAND']:
                clear_prj_Ttest_UA = await self.prj_collection.update_one(
                    {'_id': ObjectId(_id)}, {'$set': {
                            'topline_exporter': {}
                        }
                    }
                )

                if not clear_prj_Ttest_UA:
                    return {
                        'isSuccess': False,
                        'strErr': 'Clear Ttest & UA failed',
                        'zipName': None
                    }

            return {
                'isSuccess': True,
                'strErr': None,
                'zipName': exp_topline.toplineName
            }

        except Exception:

            return {
                'isSuccess': False,
                'strErr': traceback.format_exc(),
                'zipName': None
            }
























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


