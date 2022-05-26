from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from ..classes.Baemin_Checking import BaeminCheck
import traceback


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/baemin-check', tags=['baemin-check'])


@router.get('/', response_class=HTMLResponse)
async def load_baemin_xlsx(request: Request):
    return templates.TemplateResponse('baemin_check.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
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