from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import Excel2Sav, BaeminCheck
from app.routers.MSN import MSN_Projects

templates = Jinja2Templates(directory='app/frontend/templates')

app = FastAPI()

app.include_router(Excel2Sav.router)
app.include_router(BaeminCheck.router)
app.include_router(MSN_Projects.router)

app.mount('/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/convert-sav/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/baemin-check/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/msn-prj/static', StaticFiles(directory='app/frontend/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/index', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, _):
    return templates.TemplateResponse('404.html', {'request': request})


@app.get('/chart', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('chart.html', {'request': request})


import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)