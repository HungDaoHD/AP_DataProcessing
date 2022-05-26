from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import Excel2Sav


from starlette.responses import FileResponse
import traceback
# from app.classes.AP_DataConverter import APDataConverter
from app.classes.Baemin_Checking import BaeminCheck


templates = Jinja2Templates(directory='app/frontend/templates')

app = FastAPI()

app.include_router(Excel2Sav.router)
# app.include_router(BaeminCheck.router)

app.mount('/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/convert-sav/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/baemin-check/static', StaticFiles(directory='app/frontend/static'), name='static')



@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('myindex.html', {'request': request})






# @app.get('/convert-sav', response_class=HTMLResponse)
# async def load_xlsx(request: Request):
#     return templates.TemplateResponse('load_xlsx.html', {'request': request})
#
#
#
# @app.post('/convert-sav', response_class=HTMLResponse)
# async def convert_sav(file: UploadFile, request: Request):
#     try:
#         apCvt = APDataConverter()
#         apCvt.load(file)
#         apCvt.toSav()
#         apCvt.getMRSetSyntax()
#         apCvt.zipfiles()
#
#         return FileResponse(apCvt.zipName, filename=apCvt.zipName)
#
#         # return templates.TemplateResponse('successful.html', {
#         #     'request': request,
#         #     'strTask': 'Convert to SAV',
#         #     'strFileName': str(apCvt.strFileName).replace('.xlsx', '')
#         # })
#
#     except Exception:
#         print(traceback.format_exc())
#
#         return templates.TemplateResponse('error.html', {
#             'request': request,
#             'strTask': 'Convert to SAV',
#             'strErr': 'Error!!! Please check your upload file.'
#         })
#
#
#
#
#



@app.get('/baemin-check', response_class=HTMLResponse)
async def load_baemin_xlsx(request: Request):
    return templates.TemplateResponse('baemin_check.html', {'request': request})


@app.post('/baemin-check', response_class=HTMLResponse)
async def baemin_cheking(file: UploadFile, request: Request):

    try:
        bmc = BaeminCheck()
        bmc.load(file)
        bmc.check()

        return FileResponse(bmc.strFileName, filename=bmc.strFileName)

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Baemin checking',
            'strErr': traceback.format_exc()
        })


























import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)