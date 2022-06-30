from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..MSN.MSN_Database import MsnPrj
from ..Auth.hashing import Hash

msn_prj = MsnPrj()

templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/users', tags=['users'])


@router.post('/add', response_class=HTMLResponse)
async def add_user(request: Request, username: str = Form(default=''), useremail: str = Form(default=''), password: str = Form(default='')):

    result = await msn_prj.add_user(username, useremail, Hash.bcrypt(password))

    if result['isSuccess']:
        return templates.TemplateResponse('login.html', {'request': request, 'strSuccess': 'Successfully registration, please wait for admin activate your account.'})
    else:
        return templates.TemplateResponse('logup.html', {
            'request': request,
            'strTask': 'Add user error',
            'strErr': result['strErr']
        })
