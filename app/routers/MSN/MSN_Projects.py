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

    result = await msn_prj.retrieve()

    if result['isSuccess']:
        return templates.TemplateResponse('msn_prj.html', {'request': request, 'overView': result['overView'], 'lst_prj': result['lst_prj']})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Retrieve project error',
            'strErr': result['strErr']
        })


@router.get('/{_id}', response_class=HTMLResponse)
async def retrieve_id(_id, request: Request):
    result = await msn_prj.retrieve_id(_id)

    if result['isSuccess']:
        return templates.TemplateResponse('msn_prj_id.html', {'request': request, 'prj': result['prj']})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Retrieve project id error',
            'strErr': result['strErr']
        })


@router.post('/update/{_id}', response_class=RedirectResponse)
async def update_prj_data(request: Request, _id: str, strBody: str = Body(...)):
    result = await msn_prj.update_prj(_id, strBody)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve_id', **{'_id': _id})
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Update project data error',
            'strErr': result['strErr']
        })


@router.post('/data_upload/{_id}', response_class=RedirectResponse)
async def upload_prj_data(request: Request, _id: str, file_scr: UploadFile, file_main: UploadFile):

    result = await msn_prj.upload_prj_data(_id, file_scr, file_main)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve_id', **{'_id': _id})
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Upload project data error',
            'strErr': result['strErr']
        })


@router.post('/data_clear/{_id}', response_class=RedirectResponse)
async def clear_prj_data(request: Request, _id: str):

    result = await msn_prj.clear_prj_data(_id)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve_id', **{'_id': _id})
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Clear project data error',
            'strErr': result['strErr']
        })


@router.get('/data_export/{_id}', response_class=FileResponse)
async def prj_data_export(request: Request, _id: str, export_section):

    result = await msn_prj.data_export(_id, export_section)

    if result['isSuccess']:

        return FileResponse(result['zipName'], filename=result['zipName'])

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export data error',
            'strErr': result['strErr']
        })


@router.get('/topline_process/{_id}', response_class=RedirectResponse)
async def prj_topline_process(request: Request, _id: str, export_section):

    result = await msn_prj.topline_process(_id, export_section)

    if result['isSuccess']:

        redirect_url = request.url_for('retrieve_id', **{'_id': _id})
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Process topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export/{_id}', response_class=FileResponse)
async def prj_topline_export(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'FULL')

    if result['isSuccess']:

        return FileResponse(result['zipName'], filename=result['zipName'])

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export_product/{_id}', response_class=FileResponse)
async def prj_topline_export(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'PRODUCTS')

    if result['isSuccess']:

        return FileResponse(result['zipName'], filename=result['zipName'])

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export_ua_corr/{_id}', response_class=FileResponse)
async def prj_topline_export(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'UA_CORR')

    if result['isSuccess']:

        return FileResponse(result['zipName'], filename=result['zipName'])

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })




