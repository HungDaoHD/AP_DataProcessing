from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# class PrjSchema(BaseModel):
#     prj_id: str = Field(...)
#     name: str = Field(...)
#     categorical: str = Field(...)
#     status: str = Field(...)
#     detail: dict = {
#         'join_col': str(),
#         'sections': {
#             '1': {
#                 'name': str(),
#                 'filter': str(),
#                 'product_qres': {
#                     '1': {
#                         'name': str(),
#                         'lbl': str(),
#                         'qres': [str()],
#                         'cats': {
#                           '1': int(),
#                           '2': int()
#                         }
#                     },
#                     '2': {
#                         'name': str(),
#                         'lbl': str(),
#                         'qres': [str()],
#                         'cats': {
#                           '1': int(),
#                           '2': int()
#                         }
#                     }
#                 },
#                 'fc_qres': [str()]
#             },
#             '2': {
#                 'name': str(),
#                 'filter': str(),
#                 'product_qres': {
#                     '1': {
#                         'name': str(),
#                         'lbl': str(),
#                         'qres': [str()],
#                         'cats': {
#                             '1': int(),
#                             '2': int()
#                         }
#                     },
#                     '2': {
#                         'name': str(),
#                         'lbl': str(),
#                         'qres': [str()],
#                         'cats': {
#                             '1': int(),
#                             '2': int()
#                         }
#                     }
#                 },
#                 'fc_qres': [str()]
#             },
#         },
#
#         'oe_combine_cols': dict(),
#         'scr_cols': dict(),
#         'product_cols': dict(),
#         'fc_cols': dict(),
#         'addin_vars': dict(),
#         'topline_design': dict()
#     }
#
#     class Config:
#         schema_extra = {
#             'example': {
#                 'prj_id': str(),
#                 'name': str(),
#                 'categorical': str(),
#                 'status': str(),
#                 'detail': {
#                     'join_col': str(),
#                     'sections': {
#                         '1': {
#                             'name': str(),
#                             'filter': str(),
#                             'product_qres': {
#                                 '1': {
#                                     'name': str(),
#                                     'lbl': str(),
#                                     'qres': [str()],
#                                     'cats': {
#                                         '1': int(),
#                                         '2': int()
#                                     }
#                                 },
#                                 '2': {
#                                     'name': str(),
#                                     'lbl': str(),
#                                     'qres': [str()],
#                                     'cats': {
#                                         '1': int(),
#                                         '2': int()
#                                     }
#                                 }
#                             },
#                             'fc_qres': [str()]
#                         },
#                         '2': {
#                             'name': str(),
#                             'filter': str(),
#                             'product_qres': {
#                                 '1': {
#                                     'name': str(),
#                                     'lbl': str(),
#                                     'qres': [str()],
#                                     'cats': {
#                                         '1': int(),
#                                         '2': int()
#                                     }
#                                 },
#                                 '2': {
#                                     'name': str(),
#                                     'lbl': str(),
#                                     'qres': [str()],
#                                     'cats': {
#                                         '1': int(),
#                                         '2': int()
#                                     }
#                                 }
#                             },
#                             'fc_qres': [str()]
#                         },
#                     },
#
#                     'oe_combine_cols': dict(),
#                     'scr_cols': dict(),
#                     'product_cols': dict(),
#                     'fc_cols': dict(),
#                     'addin_vars': dict(),
#                     'topline_design': dict()
#                 }
#             }
#         }


class UpdatePrjModel(BaseModel):

    # prj_id: Optional[str]
    # name: Optional[str]
    # categorical: Optional[str]
    # status: Optional[str]
    join_col: Optional[str]

    class Config:
        orm_mode = True

        schema_extra = {
            'example': {
                # 'prj_id': str(),
                # 'name': str(),
                # 'categorical': str(),
                # 'status': str()
                'join_col': str()
            }
        }


