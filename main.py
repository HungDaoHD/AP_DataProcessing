from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import Excel2Sav, BaeminCheck
from app.routers.MSN import MSN_Projects
from app.routers.Auth import authentication, token
from app.routers.User import Users
import uvicorn


templates = Jinja2Templates(directory='app/frontend/templates')


app = FastAPI()

app.include_router(Excel2Sav.router)
app.include_router(BaeminCheck.router)
app.include_router(MSN_Projects.router)
app.include_router(authentication.router)
app.include_router(Users.router)

app.mount('/static', StaticFiles(directory='app/frontend/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    user_name = token.get_token_username(request)
    return templates.TemplateResponse('home.html', {'request': request, 'user_name': user_name})


@app.get('/index', response_class=HTMLResponse)
async def index(request: Request):
    user_name = token.get_token_username(request)
    return templates.TemplateResponse('home.html', {'request': request, 'user_name': user_name})


@app.get('/chart', response_class=HTMLResponse)
async def index(request: Request):
    user_name = token.get_token_username(request)
    return templates.TemplateResponse('chart.html', {'request': request, 'user_name': user_name})


@app.get('/workload', response_class=HTMLResponse)
async def index(request: Request):
    user_name = token.get_token_username(request)
    return templates.TemplateResponse('workload.html', {'request': request, 'user_name': user_name})


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, _):
    user_name = token.get_token_username(request)
    return templates.TemplateResponse('404.html', {'request': request, 'user_name': user_name})


@app.exception_handler(status.HTTP_403_FORBIDDEN)
async def custom_403_handler(_, __):
    print('HTTP_403_FORBIDDEN')
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def custom_401_handler(_, __):
    print('HTTP_401_UNAUTHORIZED')
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)