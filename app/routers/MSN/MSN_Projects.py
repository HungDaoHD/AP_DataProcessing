from fastapi import APIRouter, Request, UploadFile, Body, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from .MSN_Database import MsnPrj
from ..Auth import oauth2, token
from ...classes.CleanUpResponseFiles import CleanupFiles




msn_prj = MsnPrj()


templates = Jinja2Templates(directory='./app/frontend/templates')
# router = APIRouter(prefix='/msn-prj', tags=['msn-prj'], dependencies=[Depends(oauth2.get_current_user)])
router = APIRouter(prefix='/msn-prj', tags=['msn-prj'])


@router.get('', response_class=HTMLResponse)
async def retrieve(request: Request, page: int = 1):

    user_name = token.get_token_username(request)

    result = await msn_prj.retrieve(page)

    if result['isSuccess']:
        return templates.TemplateResponse('msn_prj.html', {'request': request, 'overView': result['overView'], 'lst_prj': result['lst_prj'], 'page_sel': int(page), 'page_count': result['page_count'], 'user_name': user_name})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Retrieve project error',
            'strErr': result['strErr']
        })


@router.get('/search', response_class=HTMLResponse)
async def search(request: Request, search_prj_name: str = ''):

    user_name = token.get_token_username(request)

    if search_prj_name == '':
        result = await msn_prj.retrieve(1)
    else:
        result = await msn_prj.search(search_prj_name)

    if result['isSuccess']:
        return templates.TemplateResponse('msn_prj.html', {'request': request, 'overView': result['overView'], 'lst_prj': result['lst_prj'], 'search_prj_name': search_prj_name, 'page_sel': 1, 'page_count': result['page_count'], 'user_name': user_name})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Search project by name error',
            'strErr': result['strErr']
        })


@router.get('/add', response_class=HTMLResponse, dependencies=[Depends(oauth2.get_current_user)])
async def prj_add(request: Request, internal_id, prj_name, categorical, prj_status):

    result = await msn_prj.add(internal_id, prj_name, categorical, prj_status)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve')
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Add project error',
            'strErr': result['strErr']
        })


@router.get('/copy/{_id}', response_class=HTMLResponse, dependencies=[Depends(oauth2.get_current_user)])
async def prj_copy(request: Request, _id):

    result = await msn_prj.copy_prj(_id)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve')
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Copy project error',
            'strErr': result['strErr']
        })


@router.get('/delete/{_id}', response_class=HTMLResponse, dependencies=[Depends(oauth2.get_current_user)])
async def prj_delete_id(_id, request: Request):
    email = token.verify_token(request.cookies['ap-login'])['email']

    result = await msn_prj.delete(_id, email)

    if result['isSuccess']:
        redirect_url = request.url_for('retrieve')
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Delete project error',
            'strErr': result['strErr']
        })


@router.get('/{_id}', response_class=HTMLResponse)
async def retrieve_id(_id, request: Request):
    user_name = token.get_token_username(request)

    result = await msn_prj.retrieve_id(_id)

    if result['isSuccess']:
        return templates.TemplateResponse('msn_prj_id.html', {'request': request, 'prj': result['prj'], 'user_name': user_name})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Retrieve project id error',
            'strErr': result['strErr']
        })


@router.post('/update/{_id}', response_class=RedirectResponse, dependencies=[Depends(oauth2.get_current_user)])
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


@router.post('/data_upload/{_id}', response_class=RedirectResponse, dependencies=[Depends(oauth2.get_current_user)])
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


@router.post('/data_clear/{_id}', response_class=RedirectResponse, dependencies=[Depends(oauth2.get_current_user)])
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

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

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


@router.get('/handcount_export/{_id}', response_class=FileResponse)
async def prj_handcount_export(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'HAND')

    if result['isSuccess']:

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export handcount error',
            'strErr': result['strErr']
        })


@router.get('/topline_export/{_id}', response_class=FileResponse)
async def prj_topline_export_full(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'FULL')

    if result['isSuccess']:

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export_product_1/{_id}', response_class=FileResponse)
async def prj_topline_export_pro_1(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'PRODUCTS_1')

    if result['isSuccess']:

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export_product_2/{_id}', response_class=FileResponse)
async def prj_topline_export_pro_2(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'PRODUCTS_2')

    if result['isSuccess']:

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })


@router.get('/topline_export_ua_corr/{_id}', response_class=FileResponse)
async def prj_topline_export_ua_corr(request: Request, _id: str, export_section):

    result = await msn_prj.topline_export(_id, export_section, 'UA_CORR')

    if result['isSuccess']:

        cleanup = CleanupFiles(lstFileName=[result['zipName']])
        return FileResponse(result['zipName'], filename=result['zipName'], background=BackgroundTask(cleanup.cleanup))

    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Export topline error',
            'strErr': result['strErr']
        })




