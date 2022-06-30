from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..Auth import token
from ..MSN.MSN_Database import MsnPrj



msn_prj = MsnPrj()

templates = Jinja2Templates(directory='./app/frontend/templates')
router = APIRouter(prefix='/charts', tags=['charts'])


@router.get('', response_class=HTMLResponse)
async def load_charts(request: Request):
    user_name = token.get_token_username(request)

    result = await msn_prj.get_overView()

    if result['isSuccess']:
        return templates.TemplateResponse('charts.html', {'request': request, 'overView': result['overView'], 'user_name': user_name})
    else:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'strTask': 'Charting error',
            'strErr': result['strErr']
        })








