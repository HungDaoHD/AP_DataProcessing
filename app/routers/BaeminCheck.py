from fastapi import APIRouter, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from ..classes.Baemin_Checking import BaeminCheck
from .Auth import token
import traceback


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/baemin-check', tags=['baemin-check'])


@router.get('', response_class=HTMLResponse)
async def load_baemin_xlsx(request: Request):
    user_name = token.get_token_username(request, credentials_exception)

    return templates.TemplateResponse('baemin_check.html', {'request': request, 'user_name': user_name})


@router.post('', response_class=HTMLResponse)
async def baemin_checking(file: UploadFile, request: Request):

    try:
        bmc = BaeminCheck()
        bmc.load(file)
        bmc.check()

        return FileResponse(bmc.strFileName, filename=bmc.strFileName)

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('baemin_check.html', {
            'request': request,
            'strTask': 'Baemin checking',
            'strErr': traceback.format_exc()
        })