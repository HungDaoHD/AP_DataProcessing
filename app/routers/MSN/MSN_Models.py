new_user_template = {
    "_id": {},
    "email": "",
    "password": "",
    "name": "",
    "role": "user",
    "create_at": "",
    "login_at": "",
    "legal": False
}

new_prj_template = {
    "_id": {},
    "internal_id": "",
    "name": "",
    "categorical": "",
    "status": "",
    "create_date": "",
    "detail": {
        "join_col": "",
        "sections": {
            "1": {
                "name": "",
                "filter": "",
                "product_qres": {
                    "1": {
                        "name": "",
                        "lbl": "",
                        "qres": [
                            ""
                        ],
                        "cats": {
                            "1": {
                                "val": "1",
                                "lbl": ""
                            },
                            "2": {
                                "val": "2",
                                "lbl": ""
                            }
                        }
                    },
                    "2": {
                        "name": "",
                        "lbl": "",
                        "qres": [
                            ""
                        ],
                        "cats": {
                            "1": {
                                "val": "1",
                                "lbl": ""
                            },
                            "2": {
                                "val": "2",
                                "lbl": ""
                            }
                        }
                    }
                },
                "fc_qres": [
                    ""
                ]
            },
            "2": {
                "name": "",
                "filter": "",
                "product_qres": {
                    "1": {
                        "name": "",
                        "lbl": "",
                        "qres": [
                            ""
                        ],
                        "cats": {
                            "1": {
                                "val": "1",
                                "lbl": ""
                            },
                            "2": {
                                "val": "2",
                                "lbl": ""
                            }
                        }
                    },
                    "2": {
                        "name": "",
                        "lbl": "",
                        "qres": [
                            ""
                        ],
                        "cats": {
                            "1": {
                                "val": "1",
                                "lbl": ""
                            },
                            "2": {
                                "val": "2",
                                "lbl": ""
                            }
                        }
                    }
                },
                "fc_qres": [
                    ""
                ]
            }
        },
        "oe_combine_cols": {},
        "scr_cols": {},
        "product_cols": {},
        "fc_cols": {},
        "addin_vars": {
            "1": {
                "name": "FC",
                "lbl": "FC",
                "cats": {
                    "1": {
                        "val": "1",
                        "lbl": "Th??ch 654/328",
                        "condition": "Main_Recall_P100_thich_hon = 1"
                    },
                    "2": {
                        "val": "2",
                        "lbl": "Th??ch 403/394",
                        "condition": "Main_Recall_P100_thich_hon = 2"
                    }
                }
            },
            "2": {
                "name": "Rotation",
                "lbl": "Rotation",
                "cats": {
                    "1": {
                        "val": "1",
                        "lbl": "Th??? 654/328 tr?????c",
                        "condition": "Main_P0b_ROTATION = 1 OR Main_P0b_ROTATION = 3"
                    },
                    "2": {
                        "val": "2",
                        "lbl": "Th??? 403/394 tr?????c",
                        "condition": "Main_P0b_ROTATION = 2 OR Main_P0b_ROTATION = 4"
                    }
                }
            }
        },
        "topline_design": {
            "is_display_pct_sign": False,
            "is_jar_scale_3": True,
            "header": {
                "1": {
                  "name": "Total",
                  "lbl": "Total",
                  "hidden_cats": ""
                }
            },
            "side": {
                "1": {
                  "group_lbl": "I. ????NH GI?? S???N PH???M TR?????C KHI ??N",
                  "name": "Main_P2_OL_Mui_nuoc_dung",
                  "lbl": "P2. M???c ????? th??ch M??I N?????C D??NG",
                  "type": "OL",
                  "t2b": True,
                  "b2b": True,
                  "mean": True,
                  "ma_cats": "",
                  "hidden_cats": "",
                  "is_count": False,
                  "is_corr": True,
                  "is_ua": False
                },
            }
        }
    },
    "screener": {},
    "main": {},
    "topline_exporter": {}
}