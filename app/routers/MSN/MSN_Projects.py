from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
# from ..classes.Baemin_Checking import BaeminCheck
import traceback

from .MSN_Database import MsnPrj

msn_prj = MsnPrj()


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/msn-prj', tags=['msn-prj'])



@router.get('', response_class=HTMLResponse)
async def retrieve(request: Request):
    lst_prj, overView = await msn_prj.retrieve()
    return templates.TemplateResponse('msn_prj.html', {'request': request, 'overView': overView, 'lst_prj': lst_prj})


@router.get('/{_id}')  # response_class=HTMLResponse
async def retrieve_id(_id):  # , request: Request
    a = await msn_prj.retrieve_id(_id)
    return a