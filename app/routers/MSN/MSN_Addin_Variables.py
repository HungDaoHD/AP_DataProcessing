import pandas as pd
import numpy as np
import traceback


class AddinVariables:
    def __init__(self, prj_addVars, df: pd.DataFrame, dictVarName: dict, dictValLbl: dict):

        self.prj_addVars = prj_addVars
        self.df = df
        self.dictVarName = dictVarName
        self.dictValLbl = dictValLbl


    def addin(self):

        try:
            print('----------------------------Addin variables----------------------------')

            availabelCols = self.df.columns

            for key, val in self.prj_addVars.items():
                varName = val['name']
                varLbl = val['lbl']

                if varName in availabelCols:
                    print(f"{varName} is already in data. You are updating that.")
                else:
                    print(f'Addin variables {varName}')

                self.dictVarName[varName] = varLbl
                self.df[varName] = [np.nan] * self.df.shape[0]

                for k, v in val['cats'].items():

                    catVal = int(v['val'])
                    catLbl = str(v['lbl'])

                    if varName in self.dictValLbl.keys():
                        self.dictValLbl[varName].update({catVal: catLbl})
                    else:
                        self.dictValLbl[varName] = {catVal: catLbl}

                    self.execCondition(varName=varName, catVal=catVal,
                                       strCondition=v['condition'],
                                       availabelCols=list(availabelCols))

            print('----------------------------Addin variables completed----------------------------')

            return True, None

        except Exception:
            return False, traceback.format_exc()



    def execCondition(self, varName: str, catVal: int, strCondition: str, availabelCols: list):

        if strCondition.upper() != 'SYSMISS':
            df = self.df
            strCondition = str(strCondition).replace('=', '==').replace('<>', '!=')
            lstCondition = strCondition.split(' ')

            dictQreCond = dict()
            dictQreCond['a0'] = varName

            idx = 1
            for item in lstCondition:
                if item in availabelCols and item != varName:
                    dictQreCond[f'a{idx}'] = item
                    idx += 1

            strZip = f"zip(df[{'], df['.join(list(dictQreCond.values()))}])"
            strZip = strZip.replace("[", "['").replace("]", "']")

            strFor = f"for {', '.join(list(dictQreCond.keys()))} in "

            strConditionReplace = strCondition
            for key, val in dictQreCond.items():
                if key == 'a0':
                    continue

                strConditionReplace = strConditionReplace.replace(val, key)

            strIf = f"{catVal} if {strConditionReplace} else a0"

            strExec = f"df['{varName}'] = [{strIf} {strFor} {strZip}]"
            strExec = strExec.replace('AND', 'and').replace('OR', 'or')

            exec(strExec)










