from fastapi import APIRouter, Request, UploadFile, Form, Body, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import traceback
from .MSN_Database import MsnPrj


msn_prj = MsnPrj()


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/msn-prj', tags=['msn-prj'])



@router.get('', response_class=HTMLResponse)
async def retrieve(request: Request):
    try:
        lst_prj, overView = await msn_prj.retrieve()
        return templates.TemplateResponse('msn_prj.html', {'request': request, 'overView': overView, 'lst_prj': lst_prj})

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('msn_prj.html', {
            'request': request,
            'strTask': 'MSN Projects',
            'strErr': traceback.format_exc()
        })



@router.get('/{_id}', response_class=HTMLResponse)
async def retrieve_id(_id, request: Request):
    try:
        prj = await msn_prj.retrieve_id(_id)

        if prj:
            return templates.TemplateResponse('msn_prj_id.html', {'request': request, 'prj': prj})
        else:
            return templates.TemplateResponse('404.html', {'request': request})

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('msn_prj_id.html', {
            'request': request,
            'strTask': 'MSN Projects\'s id',
            'strErr': traceback.format_exc()
        })


@router.post('/update/{_id}', response_class=RedirectResponse)
async def update_prj_data(request: Request, _id: str, strBody: str = Body(...)):
    try:
        updated_prj = await msn_prj.update_prj(_id, strBody)

        if updated_prj:
            redirect_url = request.url_for('retrieve_id', **{'_id': _id})
            return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        else:
            redirect_url = request.url_for('retrieve')
            return RedirectResponse(redirect_url, status_code=status.HTTP_404_NOT_FOUND)

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('msn_prj_id.html', {
            'request': request,
            'strTask': 'MSN Projects\'s id',
            'strErr': traceback.format_exc()
        })


@router.post('/data_upload/{_id}', response_class=RedirectResponse)
async def upload_prj_data(request: Request, _id: str, file_scr: UploadFile, file_main: UploadFile):
    try:

        upload_data = await msn_prj.upload_prj_data(_id, file_scr, file_main)

        if upload_data:
            redirect_url = request.url_for('retrieve_id', **{'_id': _id})
            return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        else:
            redirect_url = request.url_for('retrieve')
            return RedirectResponse(redirect_url, status_code=status.HTTP_404_NOT_FOUND)

    except Exception:
        print(traceback.format_exc())

        return templates.TemplateResponse('msn_prj_id.html', {
            'request': request,
            'strTask': 'MSN Projects\'s id',
            'strErr': traceback.format_exc()
        })


















