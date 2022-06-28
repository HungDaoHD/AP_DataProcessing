from fastapi import Depends
from fastapi.security import APIKeyCookie
from . import token as tkn


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# oauth2_scheme = HTTPBearer(scheme_name='Authorization')
oauth2_scheme = APIKeyCookie(name='ap-login')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return tkn.verify_token(token)



