from fastapi import APIRouter, Request, status, Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from ..MSN.MSN_Database import MsnPrj


msn_prj = MsnPrj()

templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/users', tags=['users'])


# @router.post('/add', response_class=HTMLResponse)
# async def add_user(request: Request, strBody: str = Body(...)):
#
#     a = strBody
#
#     return templates.TemplateResponse('logup.html', {'request': request})
#
#     # result = await msn_prj.update_prj(_id, strBody)
#     #
#     # if result['isSuccess']:
#     #     redirect_url = request.url_for('retrieve_id', **{'_id': _id})
#     #     return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
#     # else:
#     #     return templates.TemplateResponse('error.html', {
#     #         'request': request,
#     #         'strTask': 'Update project data error',
#     #         'strErr': result['strErr']
#     #     })
