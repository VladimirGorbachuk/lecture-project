from fastapi import APIRouter, FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from domain.auth import UserAuthenticationInfo, UserInfoInToken
from serializers.auth import UserAuthenticationInfoSerializer
from exceptions.auth import BaseAuthTokenException
from use_cases.auth import AuthenticatorProtocol


router = APIRouter()


@router.post('/login')
def login(user: UserAuthenticationInfoSerializer, authenticator: AuthenticatorProtocol = Depends()):
    user_entity = user.to_entity()
    if user_entity.login != "test" or user_entity.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")
    user_info = UserInfoInToken(login = "test", email="test@test.test")
    response = JSONResponse({"msg":"Successfully logged in"})
    response_with_cookies = authenticator.set_auth_tokens(response, auth_info=user_info)
    return response_with_cookies


@router.post('/refresh')
def refresh(request: Request, authenticator: AuthenticatorProtocol = Depends()):
    response = JSONResponse({"msg":"The token has been refreshed"})
    response_with_refreshed_access_cookie = authenticator.refresh_access_token(request, response)
    return response_with_refreshed_access_cookie


@router.delete('/logout')
def logout(request: Request, authenticator: AuthenticatorProtocol = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    response = JSONResponse({"msg":"Successfully logged out"})
    response_with_removed_cookies = authenticator.revoke_token(response)
    return response_with_removed_cookies


@router.get('/protected')
def protected(request: Request, authenticator: AuthenticatorProtocol = Depends()):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """
    user_info = authenticator.get_auth_info_from_token(request)
    return {"login": user_info.login, "email": user_info.email}
