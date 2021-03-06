from fastapi import APIRouter, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from fastapi.templating import Jinja2Templates
from ..classes.AP_DataConverter import APDataConverter
from ..classes.CleanUpResponseFiles import CleanupFiles
from .Auth import token
import traceback


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/convert-sav', tags=['convert-sav'])


@router.get('', response_class=HTMLResponse)
async def load_xlsx(request: Request):
    user_name = token.get_token_username(request)

    return templates.TemplateResponse('load_xlsx.html', {'request': request, 'user_name': user_name})


@router.post('', response_class=FileResponse)
async def convert_sav(file: UploadFile, request: Request):
    try:
        apCvt = APDataConverter()
        apCvt.load(file)
        apCvt.toSav()
        apCvt.getMRSetSyntax()
        apCvt.zipfiles()

        cleanup = CleanupFiles(lstFileName=[apCvt.zipName])

        return FileResponse(apCvt.zipName, filename=apCvt.zipName, background=BackgroundTask(cleanup.cleanup))

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
            'strErr': traceback.format_exc()
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

