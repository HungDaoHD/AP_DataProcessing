import traceback
from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from . import token
from .hashing import Hash
from ..MSN.MSN_Database import MsnPrj


manager = LoginManager(token.SECRET_KEY, use_cookie=True, token_url='/login', default_expiry=timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES))
manager.cookie_name = "ap-login"


msn_prj = MsnPrj()


templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(
    tags=['authentication']
)


@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login', response_class=HTMLResponse)
async def login(request: Request, OAuth: OAuth2PasswordRequestForm = Depends()):

    try:
        user = None
        async for usr in msn_prj.user_collection.find({'email': OAuth.username}).limit(1):
            user = usr
            break

        if not user:
            return templates.TemplateResponse('login.html', {'request': request, 'strErr': 'Invalid email'})

        if not Hash.verify(user['password'], OAuth.password):
            return templates.TemplateResponse('login.html', {'request': request, 'strErr': 'Incorrect password'})

        await msn_prj.user_collection.update_one(
            {'email': user['email']}, {'$set': {
                    'login_at': datetime.now()
                }
            }
        )

        access_token = manager.create_access_token(data=dict(sub=user['email'], name=user['name']), expires=timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES))

        resp = RedirectResponse(url='/index', status_code=status.HTTP_302_FOUND)
        manager.set_cookie(response=resp, token=access_token)

        return resp

    except Exception:
        print(traceback.format_exc())
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Login error',
            'strErr': traceback.format_exc()
        })


@router.get('/logout', response_class=HTMLResponse)
async def logout(request: Request):
    resp = RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response=resp, token='')
    return resp





