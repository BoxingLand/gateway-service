from fastapi import APIRouter, Depends

from app.deps import user_deps
from app.utils.response_schema import create_response


router = APIRouter()


@router.get("/{user_id}/profile")
async def get_profile(res = Depends(user_deps.grpc_get_boxer_by_id)):
    return create_response(data=res)


@router.get("/{user_id}/me")
async def get_my_profile():
    ...


@router.get("/boxers")
async def get_boxers():
    ...


@router.get("/judges")
async def get_judges():
    ...


@router.get("/coaches")
async def get_coaches():
    ...


@router.get("/organizers")
async def get_organizers():
    ...


@router.post("/photo/upload")
async def upload_photo(res = Depends(user_deps.grpc_upload_foto)):
    return create_response(data=res)


@router.post("/change_password")
async def _change_password(res = Depends(user_deps.grpc_change_password)):
    return create_response(data=res)


@router.put("/update")
async def _update_data(res = Depends(user_deps.grpc_update_user)):
    return create_response(data=res)


@router.post("/add_role")
async def _add_role(res = Depends(user_deps.grpc_add_role)):
    return create_response(data=res)


@router.delete("/delete")
async def _delete_data(res = Depends(user_deps.grpc_delete_user)):
    return create_response(data=res)
