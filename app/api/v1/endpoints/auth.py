from fastapi import APIRouter, Depends

from app.deps import auth_deps
from app.utils.response_schema import create_response

router = APIRouter()

@router.post("/signup")
async def _signup(res = Depends(auth_deps.grpc_signup)):
    return create_response(data=res)

@router.post("/signin")
async def _signin(res = Depends(auth_deps.grpc_signin)):
    return create_response(data=res)
@router.get("/verify/email")
async def _verify_email():
    ...

@router.get("/verify/email/new")
async def _verify_email_new():
    ...

@router.post("/refresh")
async def _refresh(res = Depends(auth_deps.grpc_refresh)):
    return create_response(data=res)
