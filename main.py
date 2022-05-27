from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import Excel2Sav, BaeminCheck


templates = Jinja2Templates(directory='app/frontend/templates')

app = FastAPI()

app.include_router(Excel2Sav.router)
app.include_router(BaeminCheck.router)

app.mount('/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/convert-sav/static', StaticFiles(directory='app/frontend/static'), name='static')
app.mount('/baemin-check/static', StaticFiles(directory='app/frontend/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('myindex.html', {'request': request})


@app.get('/index', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('myindex.html', {'request': request})


import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)