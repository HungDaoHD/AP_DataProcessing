from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from . import token as tkn


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# oauth2_scheme = HTTPBearer(scheme_name='Authorization')
oauth2_scheme = APIKeyCookie(name='ap-login')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    return tkn.verify_token(token, credentials_exception)



