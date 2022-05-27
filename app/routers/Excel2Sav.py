from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from ..classes.AP_DataConverter import APDataConverter
import traceback


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/convert-sav', tags=['convert-sav'])


@router.get('', response_class=HTMLResponse)
async def load_xlsx(request: Request):
    return templates.TemplateResponse('load_xlsx.html', {'request': request})


@router.post('', response_class=FileResponse)
async def convert_sav(file: UploadFile, request: Request):
    try:
        apCvt = APDataConverter()
        apCvt.load(file)
        apCvt.toSav()
        apCvt.getMRSetSyntax()
        apCvt.zipfiles()

        return FileResponse(apCvt.zipName, filename=apCvt.zipName)

        # return templates.TemplateResponse('successful.html', {
        #     'request': request,
        #     'strTask': 'Convert to SAV',
        #     'strFileName': str(apCvt.strFileName).replace('.xlsx', '')
        # })

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('load_xlsx.html', {
            'request': request,
            'strTask': 'Convert to SAV',
            'strErr': 'Error!!! Please check your upload file.'
        })



# @app.get('/successful', response_class=HTMLResponse)
# async def successful(request: Request, strTask: Optional[str] = '', strFileName: Optional[str] = ''):
#     return templates.TemplateResponse('successful.html', {'request': request, 'strTask': strTask, 'strFileName': strFileName})
#
#
# @app.get('/download', response_class=FileResponse)
# async def download():
#     try:
#
#         return FileResponse(apCvt.zipName, filename=apCvt.zipName)
#
#     except Exception:
#         return {'errors': traceback.format_exc()}



# @app.get('/error', response_class=HTMLResponse)
# async def error(request: Request, strTask: Optional[str] = '', strErr: Optional[str] = ''):
#     return templates.TemplateResponse('error.html', {'request': request, 'strTask': strTask, 'strErr': strErr})

