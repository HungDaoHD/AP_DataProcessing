import pandas as pd
import openpyxl
import numpy as np
import pyreadstat
import re


class ConvertQandMeExcelFile:

    def __init__(self, strFileName):
        self.strFileName = strFileName

        self.dfData = pd.DataFrame()
        self.dict_column_labels, self.variable_value_labels = dict(), dict()

    def convert(self):
        wb = openpyxl.load_workbook(f'{self.strFileName}')

        wsData = wb['Data']
        wsQres = wb['Question']

        mergedCells = list()
        for group in wsData.merged_cells.ranges:
            mergedCells.append(group)

        for group in mergedCells:
            wsData.unmerge_cells(str(group))

        wsData.delete_rows(1, 4)
        wsData.delete_rows(2, 1)

        for icol in range(1, wsData.max_column + 1):
            if wsData.cell(row=1, column=icol).value is None:
                wsData.cell(row=1,
                            column=icol).value = f'{wsData.cell(row=1, column=icol - 1).value}_{wsData.cell(row=2, column=icol).value}'

        wsData.delete_rows(2, 1)

        data = wsData.values
        columns = next(data)[0:]
        dfData = pd.DataFrame(data, columns=columns)

        lstDrop = [
            'Approve',
            'Reject',
            'Re - do request',  'Re-do request',
            'Reason to reject',
            'Memo'
            'No.',
            'Date',
            'ID',
            'Country',
            'Channel',
            'Chain / Type',
            'Distributor',
            'Method',
            'Panel ID',
            'Panel FB',
            'Panel Email',
            'Panel Phone',
            'Panel Age',
            'Panel Gender',
            'Panel Area',
            'Panel Income',
            'Login ID',
            'User name',
            'Store ID',
            'Store Code',
            'Store name',
            'Store level',
            'District',
            'Ward',
            'Store address',
            'Area group',
            'Store ranking',
            'Region 2',
            'Nhóm cửa hàng',
            'Nhà phân phối',
            'Manager',
            'Telephone number',
            'Contact person',
            'Email',
            'Others 1',
            'Others 2',
            'Others 3',
            'Others 4',
            'Check in',
            'Store Latitude',
            'Store Longitude',
            'User Latitude',
            'User Longitude',
            'Check out',
            'Distance',
            'Task duration',

            'InterviewerID',
            'InterviewerName',
            'RespondentName',
            'RespondentEmail',
            'RespondentPhone',
            'RespondentCellPhone',
            'RespondentAddress',

        ]

        for col in dfData.columns:
            if col in lstDrop or '_Images' in col:
                dfData.drop(col, inplace=True, axis=1)

        data = wsQres.values
        columns = next(data)[0:]
        dfQres = pd.DataFrame(data, columns=columns)

        dictQres = dict()
        for idx in dfQres.index:

            strMatrix = (
                '' if dfQres.loc[idx, 'Question(Matrix)'] is None else f"{dfQres.loc[idx, 'Question(Matrix)']}_")
            strNormal = (dfQres.loc[
                             idx, 'Question(Normal)'] if strMatrix == '' else f"{strMatrix}{dfQres.loc[idx, 'Question(Normal)']}")
            strQreName = str(dfQres.loc[idx, 'Name of items'])
            strQreName = strQreName.replace('Rank_', 'Rank') if 'Rank_' in strQreName else strQreName

            dictQres[strQreName] = {
                'type': dfQres.loc[idx, 'Question type'],
                'label': f'{strNormal}',
                'isMAMatrix': True if strMatrix != '' and dfQres.loc[idx, 'Question type'] == 'MA' else False,
                'cats': {
                }
            }

            for col in dfQres.columns:
                if col not in ['Name of items', 'Question type', 'Question(Matrix)', 'Question(Normal)'] \
                        and dfQres.loc[idx, col] is not None:
                    dictQres[strQreName]['cats'].update({int(col): self.cleanhtml(str(dfQres.loc[idx, col]))})

        lstMatrixHeader = list()
        for k in dictQres.keys():
            if dictQres[k]['isMAMatrix'] and len(dictQres[k]['cats'].keys()):
                lstMatrixHeader.append(k)

        for i in lstMatrixHeader:
            for code in dictQres[i]['cats'].keys():
                lstLblMatrixMA = dictQres[f'{i}_{code}']['label'].split('_')
                dictQres[f'{i}_{code}']['cats'].update({1: self.cleanhtml(lstLblMatrixMA[1])})
                dictQres[f'{i}_{code}']['label'] = f"{dictQres[i]['label']}_{lstLblMatrixMA[1]}"

        dict_column_labels = dict()
        variable_value_labels = dict()
        for col in dfData.columns:
            if col in dictQres.keys():
                dict_column_labels[col] = self.cleanhtml(dictQres[col]['label'])

                variable_value_labels[col] = dictQres[col]['cats']

            else:
                dict_column_labels[col] = col

        dfData.replace({None: np.nan}, inplace=True)

        wb.close()

        self.dfData, self.dict_column_labels, self.variable_value_labels = dfData, dict_column_labels, variable_value_labels

        return dfData, dict_column_labels, variable_value_labels


    def toSav(self):
        pyreadstat.write_sav(self.dfData,
                             f'{self.strFileName}.sav',
                             column_labels=list(self.dict_column_labels.values()),
                             variable_value_labels=self.variable_value_labels)


    @staticmethod
    def cleanhtml(raw_html):
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(CLEANR, '', raw_html)
        return cleantext