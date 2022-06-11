import pandas as pd
import numpy as np
import pyreadstat
import openpyxl
import warnings
import zipfile


warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class ExportMSNData:

    def __init__(self, prj: dict, isExportSPCode: bool, export_section: str):

        self.prj = prj
        self.obj_section = prj['detail']['sections'][export_section]

        self.isExportForceChoiceYN = True
        self.isExportSPCode = isExportSPCode

        self.strProjectName = f"{prj['internal_id']}_{prj['name']}_{self.obj_section['name']}"
        self.strRidColName = prj['detail']['join_col']
        self.strFilter = self.obj_section['filter']
        self.lstSPCodes = [self.obj_section['product_qres']['1']['cats']['1']['lbl'], self.obj_section['product_qres']['1']['cats']['2']['lbl']]

        # {'Main_P0c_2_Ma_san_pham_HN': {1: '426', 2: '705'}, 'Main_O0c_2_Ma_san_pham_HN': {1: '426', 2: '705'}}
        self.dictReProductCode = dict()

        # {'Main_P0c_Ma_san_pham': {'label': 'P0c. MÃ SẢN PHẨM ĐƯỢC ĐÁNH GIÁ TƯƠNG ỨNG',
        #                           'qres': ['Main_P0c_2_Ma_san_pham_HN', 'Main_P0c_2_Ma_san_pham_HN'],
        #                           'cats': {1: '426', 2: '705'}},
        #  'Main_O0c_Ma_san_pham': {'label': 'P0c. MÃ SẢN PHẨM ĐƯỢC ĐÁNH GIÁ TƯƠNG ỨNG',
        #                           'qres': ['Main_O0c_2_Ma_san_pham_HN', 'Main_O0c_2_Ma_san_pham_HN'],
        #                           'cats': {1: '426', 2: '705'}}}
        self.dictNewProductCodeQres = dict()

        dictCats = dict()

        for key, val in self.obj_section['product_qres'].items():

            dictCats = {
                int(val['cats']['1']['val']): str(val['cats']['1']['lbl']),
                int(val['cats']['2']['val']): str(val['cats']['2']['lbl']),
            }

            self.dictReProductCode[val['qres'][0]] = dictCats

            self.dictNewProductCodeQres[val['name']] = {
                'label': val['lbl'],
                'qres': [val['qres'][0], val['qres'][0]],
                'cats': dictCats
            }

        self.lstNewProductCodeQres = list(self.dictNewProductCodeQres.keys())

        dictSPCodes = dict()
        if self.isExportSPCode:
            for item in self.lstSPCodes:
                dictSPCodes[int(item)] = str(item)
        else:
            dictSPCodes = dictCats

        self.dictReForceChoice = {
            self.obj_section['fc_qres'][0]: {
                'oldVal': {
                    1: self.lstNewProductCodeQres[0],
                    2: self.lstNewProductCodeQres[1]},
                'newVal': dictSPCodes
            }
        }

        self.dfCombinedOE = pd.DataFrame.from_dict(self.prj['detail']['oe_combine_cols'],
                                                   orient='index',
                                                   columns=['Combined name', 'Qre name 1', 'Qre name 2'])

        self.lstScrFormat = list()
        for key, val in self.prj['detail']['scr_cols'].items():
            self.lstScrFormat.append([val[1], val[0]])

        self.lstSP1Format = [[self.lstNewProductCodeQres[0], self.lstNewProductCodeQres[0]]]
        self.lstSP2Format = [[self.lstNewProductCodeQres[1], self.lstNewProductCodeQres[0]]]
        for key, val in self.prj['detail']['product_cols'].items():
            self.lstSP1Format.append([val[1], val[0]])
            self.lstSP2Format.append([val[2], val[0]])



        self.lstPreFormat = list()
        for key, val in self.prj['detail']['fc_cols'].items():
            self.lstPreFormat.append([val[1], val[0]])

        self.dfMerge = pd.DataFrame()
        self.dictMerge_column_labels, self.dictMerge_variable_value_labels = dict(), dict()

        self.create_dfMerge()

        self.dfSP1, self.dfSP2 = pd.DataFrame(), pd.DataFrame()
        self.create_dfSP1_dfSP2()

        self.dfStacked, self.dfUnstacked = pd.DataFrame(), pd.DataFrame()
        # self.dictUnstack_column_labels, self.dictUnstack_variable_value_labels = dict(), dict()

        self.savStackName = f"{self.strProjectName}_Stack.sav"
        self.savStackFile = None

        self.zipName = f"{self.strProjectName}.zip"
        self.zipFile = None

        pass




    def create_dfMerge(self):
        # Load excel file to dataframe----------------------------------------------------------------------------------

        dfScr = pd.DataFrame.from_dict(self.prj['screener']['data'])
        dictScr_column_labels = self.prj['screener']['varLbl']
        dictScr_variable_value_labels = {key: {int(k): v for k, v in val.items()} for key, val in self.prj['screener']['valLbl'].items()}

        dfMain = pd.DataFrame.from_dict(self.prj['main']['data'])
        dictMain_column_labels = self.prj['main']['varLbl']
        dictMain_variable_value_labels = {key: {int(k): v for k, v in val.items()} for key, val in self.prj['main']['valLbl'].items()}

        dfScr[self.strRidColName] = dfScr[self.strRidColName].apply(pd.to_numeric)
        dfMain[self.strRidColName] = dfMain[self.strRidColName].apply(pd.to_numeric)

        if not self.check_RID(dfScr[self.strRidColName].copy(), dfMain[self.strRidColName].copy()):
            exit()

        print('Load Q&Me excel files to dataframe')

        # Create dfMerge -----------------------------------------------------------------------------------------------
        self.dfMerge = pd.merge(dfScr, dfMain, on=self.strRidColName, how='left')

        self.dfMerge = self.get_filter_data(self.dfMerge.copy(), self.strFilter)

        for idx in self.dfCombinedOE.index:
            strCombineName = self.dfCombinedOE.at[idx, 'Combined name']
            strSP1Name = self.dfCombinedOE.at[idx, 'Qre name 1']
            strSP2Name = self.dfCombinedOE.at[idx, 'Qre name 2']

            self.dfMerge[strSP1Name].replace({np.nan: 'NULL'}, inplace=True)
            self.dfMerge[strSP2Name].replace({np.nan: 'NULL'}, inplace=True)

            self.dfMerge[strCombineName] = [(a if a != 'NULL' else (b if b != 'NULL' else np.nan)) for a, b in
                                            zip(self.dfMerge[strSP1Name], self.dfMerge[strSP2Name])]

            self.dfMerge[strSP1Name].replace({'NULL': np.nan}, inplace=True)
            self.dfMerge[strSP2Name].replace({'NULL': np.nan}, inplace=True)

            dictMain_variable_value_labels[strCombineName] = {}
            dictMain_column_labels[strCombineName] = dictMain_column_labels[strSP1Name]

        # self.dfMerge.drop(self.dfDroppedOE['Delete columns name'].values.tolist(), inplace=True, axis=1)

        self.dictMerge_column_labels = dictScr_column_labels | dictMain_column_labels

        self.dictMerge_variable_value_labels = dictScr_variable_value_labels | dictMain_variable_value_labels

        for key, val in self.dictReProductCode.items():
            self.dictMerge_variable_value_labels[key] = val

        for key, val in self.dictReForceChoice.items():
            self.dictMerge_variable_value_labels[key] = val['newVal']

        if self.isExportSPCode:
            for key in self.dictReProductCode.keys():
                self.dfMerge[key].replace(self.dictReProductCode[key], inplace=True)

        for key, val in self.dictNewProductCodeQres.items():
            self.dfMerge[key] = [a if float(a) > 0 else b for a, b in
                                 zip(self.dfMerge[val['qres'][0]], self.dfMerge[val['qres'][1]])]

            self.dictMerge_column_labels[key] = val['label']

            self.dictMerge_variable_value_labels[key] = val['cats']

        for key, val in self.dictReForceChoice.items():
            for idx in self.dfMerge.index:
                for key2, val2 in val['oldVal'].items():
                    if self.dfMerge.at[idx, key] == key2:
                        self.dfMerge.at[idx, key] = self.dfMerge.at[idx, val2]
                        break

        # self.dfMerge.to_csv('dfMerge.csv', encoding='utf-8-sig')

        print('Created dfMerge')


    @staticmethod
    def check_RID(dfRidScr, dfRidMain):

        isValid = True

        dfRidScr = pd.DataFrame(dfRidScr)
        dfRidMain = pd.DataFrame(dfRidMain)

        dfRidScrDup = pd.DataFrame(dfRidScr[dfRidScr.astype(int).duplicated()])
        if not dfRidScrDup.empty:
            isValid = False
            print('Duplicated id in screener:', dfRidScrDup.values)

        dfRidMainDup = pd.DataFrame(dfRidMain[dfRidMain.astype(int).duplicated()])
        if not dfRidMainDup.empty:
            isValid = False
            print('Duplicated id in Main:', dfRidMainDup.values)

        setRidScr = set(dfRidScr.iloc[:, 0])
        setRidMain = set(dfRidMain.iloc[:, 0])

        diffRidScr = setRidScr.difference(setRidMain)
        if len(diffRidScr):
            isValid = False
            print('ID in screener but not in main:', diffRidScr)

        diffRidMain = setRidMain.difference(setRidScr)
        if len(diffRidMain):
            isValid = False
            print('ID in main but not in screener:', diffRidMain)

        if not isValid:
            print('The process is terminated.')

        return isValid


    @staticmethod
    def get_filter_data(dfMerge: pd.DataFrame, strFilter: str):
        try:

            strFilter = strFilter.strip()
            strFilter = "{}{}{}".format('{', strFilter.replace(' ', '} {'), '}')
            strFilter = strFilter.replace('} {=} {', "'] == ")
            strFilter = strFilter.replace('} {<>} {', "'] != ")
            strFilter = strFilter.replace('} {>} {', "'] > ")
            strFilter = strFilter.replace('} {>=} {', "'] >= ")
            strFilter = strFilter.replace('} {<} {', "'] < ")
            strFilter = strFilter.replace('} {<=} {', "'] <= ")
            strFilter = strFilter.replace('{OR}', '|')
            strFilter = strFilter.replace('{AND}', '&')
            strFilter = strFilter.replace('{', "(dfMerge['")
            strFilter = strFilter.replace('}', ")")

            dfMerge = eval(f"dfMerge.loc[({strFilter})]")

            return dfMerge

        except Exception:
            print('Filter error!!!', '\n', 'The process is terminated.')
            exit()


    def create_dfSP1_dfSP2(self):
        lstSP1_toLoc = [row[0] for row in self.lstScrFormat + self.lstSP1Format + self.lstPreFormat]
        lstSP2_toLoc = [row[0] for row in self.lstScrFormat + self.lstSP2Format + self.lstPreFormat]

        self.dfSP1 = self.dfMerge.loc[:, lstSP1_toLoc].copy()
        self.dfSP2 = self.dfMerge.loc[:, lstSP2_toLoc].copy()

        self.dfSP1.set_axis([row[1] for row in self.lstScrFormat + self.lstSP1Format + self.lstPreFormat], axis=1, inplace=True)
        self.dfSP2.set_axis([row[1] for row in self.lstScrFormat + self.lstSP2Format + self.lstPreFormat], axis=1, inplace=True)

        print('Created dfSP1 & dfSP2')


    def export_stackSav(self):

        self.dfStacked = pd.concat([self.dfSP1, self.dfSP2], ignore_index=True)

        lstStack_column_labels = [self.dictMerge_column_labels[row[0]] for row in self.lstScrFormat + self.lstSP1Format + self.lstPreFormat]

        dictStack_variable_value_labels = dict()

        for row in self.lstScrFormat + self.lstSP1Format + self.lstPreFormat:
            dictStack_variable_value_labels[row[1]] = self.dictMerge_variable_value_labels[row[0]]


        strForceChoiceYN = ''
        if self.isExportForceChoiceYN:
            strForceChoice = list(self.dictReForceChoice.keys())[0]
            strForceChoiceYN = f'{strForceChoice}_YN'
            strProductCodeQre = self.dictReForceChoice[strForceChoice]['oldVal'][1]

            self.dfStacked[strForceChoiceYN] = [1 if a == b else 0 for a, b in zip(self.dfStacked[strForceChoice], self.dfStacked[strProductCodeQre])]

            lstStack_column_labels.append(self.dictMerge_column_labels[strForceChoice])
            dictStack_variable_value_labels[strForceChoiceYN] = {0: 'No', 1: 'Yes'}

        self.dfStacked.sort_values(by=self.lstScrFormat[0][1], inplace=True)

        self.dfStacked.replace({-99999: np.nan}, inplace=True)

        # dfStacked.to_csv(f'{strFormatedPath}/dfStacked.csv', encoding='utf-8-sig')

        print('Created dfStacked')

        # if self.isExportForceChoiceYN:
        #
        #     pyreadstat.write_sav(self.dfStacked,
        #                          f'{self.strFormatedPath}/{self.strProjectName}_Stack_{self.strDateVer}_ForceChoiceYN.sav',
        #                          column_labels=lstStack_column_labels,
        #                          variable_value_labels=dictStack_variable_value_labels)
        #
        #     self.dfStacked.drop(columns=[strForceChoiceYN], inplace=True)
        #     lstStack_column_labels = lstStack_column_labels[:-1]
        #     dictStack_variable_value_labels.pop(strForceChoiceYN)


        self.savStackFile = pyreadstat.write_sav(self.dfStacked, self.savStackName,
                                                 column_labels=lstStack_column_labels,
                                                 variable_value_labels=dictStack_variable_value_labels)

        print('Exported Stacked Sav file')



    # def export_unstackSav(self):
    #     self.dfUnstacked = pd.DataFrame()
    #
    #     lstUnstack_column_labels = list()
    #     dictUnstack_variable_value_labels = dict()
    #
    #     for row in self.lstScrFormat:
    #         self.dfUnstacked[row[1]] = self.dfMerge[row[0]].copy()
    #
    #         lstUnstack_column_labels.append(self.dictMerge_column_labels[row[0]])
    #         dictUnstack_variable_value_labels[row[1]] = self.dictMerge_variable_value_labels[row[0]]
    #
    #         self.dictUnstack_column_labels[row[1]] = self.dictMerge_column_labels[row[0]]
    #         self.dictUnstack_variable_value_labels[row[1]] = self.dictMerge_variable_value_labels[row[0]]
    #
    #
    #     for row in self.lstSP1Format:
    #         if row[0] != list(self.dictReProductCode.keys())[0]:  # row[0] != self.lstNewProductCodeQres[0]:
    #             for spCode in self.lstSPCodes:
    #                 self.dfUnstacked[f'{row[1]}_{spCode}'] = [np.nan] * self.dfUnstacked.shape[0]
    #
    #                 lstUnstack_column_labels.append(f'{self.dictMerge_column_labels[row[0]]}_{spCode}')
    #                 dictUnstack_variable_value_labels[f'{row[1]}_{spCode}'] = self.dictMerge_variable_value_labels[row[0]]
    #
    #                 self.dictUnstack_column_labels[f'{row[1]}_{spCode}'] = f'{self.dictMerge_column_labels[row[0]]}_{spCode}'
    #                 self.dictUnstack_variable_value_labels[f'{row[1]}_{spCode}'] = self.dictMerge_variable_value_labels[row[0]]
    #
    #
    #     for row in self.lstPreFormat:
    #         self.dfUnstacked[row[1]] = self.dfMerge[row[0]].copy()
    #
    #         lstUnstack_column_labels.append(self.dictMerge_column_labels[row[0]])
    #         dictUnstack_variable_value_labels[row[1]] = self.dictMerge_variable_value_labels[row[0]]
    #
    #         self.dictUnstack_column_labels[row[1]] = self.dictMerge_column_labels[row[0]]
    #         self.dictUnstack_variable_value_labels[row[1]] = self.dictMerge_variable_value_labels[row[0]]
    #
    #
    #
    #     for idx in self.dfUnstacked.index:
    #
    #         for row in self.lstSP1Format:
    #             if row[0] != list(self.dictReProductCode.keys())[0]:  # row[0] != self.lstNewProductCodeQres[0]:
    #                 # masp = int(self.dfMerge.at[idx, self.lstNewProductCodeQres[0]])
    #
    #                 masp = self.dictMerge_variable_value_labels[self.lstNewProductCodeQres[0]][int(self.dfMerge.at[idx, self.lstNewProductCodeQres[0]])]
    #
    #                 val = self.dfMerge.at[idx, row[0]]
    #
    #                 self.dfUnstacked.at[idx, f'{row[1]}_{masp}'] = val
    #
    #
    #         for row in self.lstSP2Format:
    #             if row[0] != list(self.dictReProductCode.keys())[1]:  # row[0] != self.lstNewProductCodeQres[1]:
    #                 # masp = int(self.dfMerge.at[idx, self.lstNewProductCodeQres[1]])
    #
    #                 masp = self.dictMerge_variable_value_labels[self.lstNewProductCodeQres[1]][int(self.dfMerge.at[idx, self.lstNewProductCodeQres[1]])]
    #
    #                 val = self.dfMerge.at[idx, row[0]]
    #
    #                 self.dfUnstacked.at[idx, f'{row[1]}_{masp}'] = val
    #
    #
    #     self.dfUnstacked.sort_values(by=self.lstScrFormat[0][1], inplace=True)
    #
    #     self.dfUnstacked.replace({-99999: np.nan}, inplace=True)
    #
    #     # dfUnstacked.to_csv(f'{strFormatedPath}/dfUnstacked.csv', encoding='utf-8-sig')
    #
    #     print('Created dfUnstacked')
    #
    #     pyreadstat.write_sav(self.dfUnstacked, f'{self.strFormatedPath}/{self.strProjectName}_Unstack_{self.strDateVer}.sav',
    #                          column_labels=lstUnstack_column_labels,
    #                          variable_value_labels=dictUnstack_variable_value_labels)
    #
    #     if self.isExportForceChoiceYN:
    #         strForceChoice = list(self.dictReForceChoice.keys())[0]
    #         dictProductCode = self.dictReForceChoice[strForceChoice]['newVal']
    #
    #         strForceChoiceSP1 = f'{strForceChoice}_{int(list(dictProductCode.values())[0])}'
    #         strForceChoiceSP2 = f'{strForceChoice}_{int(list(dictProductCode.values())[1])}'
    #
    #         self.dfUnstacked[strForceChoiceSP1] = [1 if int(a) == list(dictProductCode.keys())[0] else 0 for a in self.dfUnstacked[strForceChoice]]
    #         self.dfUnstacked[strForceChoiceSP2] = [1 if int(a) == list(dictProductCode.keys())[1] else 0 for a in self.dfUnstacked[strForceChoice]]
    #
    #         self.dictUnstack_column_labels[strForceChoiceSP1] = strForceChoiceSP1
    #         self.dictUnstack_column_labels[strForceChoiceSP2] = strForceChoiceSP2
    #
    #         self.dictUnstack_variable_value_labels[strForceChoiceSP1] = {0: 'No', 1: 'Yes'}
    #         self.dictUnstack_variable_value_labels[strForceChoiceSP2] = {0: 'No', 1: 'Yes'}
    #
    #         self.strSavToToplinePath = f'{self.strFormatedPath}/{self.strProjectName}_Unstack_{self.strDateVer}_ForceChoiceYN.sav'
    #
    #         pyreadstat.write_sav(self.dfUnstacked,
    #                              self.strSavToToplinePath,
    #                              column_labels=list(self.dictUnstack_column_labels.values()),
    #                              variable_value_labels=self.dictUnstack_variable_value_labels)
    #
    #
    #     print('Exported Unstacked Sav file')
    #
    #
    # def export_excelFile(self):
    #     dictRecodeScrForXlsx = dict()
    #
    #     for row in self.lstScrFormat:
    #         dictRecodeScrForXlsx[row[1]] = self.dictMerge_variable_value_labels[row[0]]
    #
    #     dfUnstacked = self.dfUnstacked.replace(dictRecodeScrForXlsx)
    #     dfStacked = self.dfStacked.replace(dictRecodeScrForXlsx)
    #
    #     with pd.ExcelWriter(f'{self.strFormatedPath}/{self.strProjectName}_ExcelData_{self.strDateVer}.xlsx') as writer:
    #         dfUnstacked.to_excel(writer, sheet_name='Product - Unstacked', index=False, encoding='utf-8-sig')
    #         dfStacked.to_excel(writer, sheet_name='Product - Stacked', index=False, encoding='utf-8-sig')
    #
    #     print('Exported Excel data files')
    #
    #
    # def export_codingFile(self):
    #     dictCoding = dict()
    #
    #     for idx in self.dfExportCoding.index:
    #
    #         strCodeFrame = self.dfExportCoding.at[idx, 'Codeframe']
    #         strQreCoding = self.dfExportCoding.at[idx, 'Questions']
    #
    #         lstAddinCol = list()
    #         for i in range(1, 6):
    #             if not pd.isnull(self.dfExportCoding.at[idx, f'AddinColumn{i}']):
    #                 lstAddinCol.append(self.dfExportCoding.at[idx, f'AddinColumn{i}'])
    #
    #         if strCodeFrame in dictCoding.keys():
    #             if strQreCoding not in dictCoding[strCodeFrame]:
    #                 dictCoding[strCodeFrame].append(strQreCoding)
    #         else:
    #             dictCoding[strCodeFrame] = lstAddinCol + [strQreCoding]
    #
    #
    #     dfScrCols = pd.read_excel(self.strFormatFile, sheet_name='ScreenerColumns')
    #     strIDCol = dfScrCols.at[0, 'Rename columns name']
    #
    #     writer = pd.ExcelWriter(f'{self.strFormatedPath}/{self.strProjectName}_Coding_{self.strDateVer}.xlsx', engine='xlsxwriter')
    #
    #     pd.DataFrame().to_excel(writer, sheet_name='Code list', index=False, encoding='utf-8-sig')
    #
    #     for key, val in dictCoding.items():
    #
    #         lstCols = [strIDCol] + val
    #         df = pd.DataFrame(self.dfStacked.loc[:, lstCols].copy())
    #
    #         arrNan = [np.nan] * df.shape[0]
    #         for i in range(1, 21):
    #             if 1 <= i <= 10:
    #                 df[f'{key}_Y_Dau_Col{i}'] = arrNan
    #             else:
    #                 df[f'{key}_Y_TiepTheo_Col{i-10}'] = arrNan
    #
    #
    #         if key == 'P100a':
    #             df.drop_duplicates(inplace=True)
    #
    #         df.to_excel(writer, sheet_name=key, index=False, encoding='utf-8-sig')
    #
    #
    #     writer.save()
    #
    #
    #


    def run(self):

        print('---------------------------Start data formatting---------------------------')

        self.export_stackSav()

        # self.export_unstackSav()
        #
        # self.export_excelFile()

        print('---------------------------Data exporting completed---------------------------')


    def zipfiles(self):

        with zipfile.ZipFile(self.zipName, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(self.savStackName)

        self.zipFile = zf












