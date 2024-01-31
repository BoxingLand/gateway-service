from base64 import b64encode
from io import BytesIO
from typing import Annotated
from uuid import UUID

import grpc
from fastapi import Path, UploadFile, Depends, Query
from starlette.responses import StreamingResponse, Response

from app.api.v1.endpoints import oauth2_scheme
from app.client.auth import auth_pb2_grpc, auth_pb2
from app.client.user import user_pb2_grpc, user_pb2
from app.dto.request.user import UpdateUserRequestDto, ChangePasswordRequestDto, \
    AddRoleRequestDto, UploadFileRequestDto
from app.dto.response.user import DeleteUserResponseDto, UpdateUserResponseDto, ChangePasswordResponseDto, \
    AddRoleResponseDto, UserBoxerProfileResponseDto


async def grpc_delete_user(
        access_token = Depends(oauth2_scheme),
) -> DeleteUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.DeleteUser(user_pb2.DeleteUserRequest(
            user_id=response.sub
        ))
    return DeleteUserResponseDto(message=response.message)


async def grpc_upload_foto(
        file: UploadFile,
        is_avatar: Annotated[bool, Query(description="Is user avatar")],
        access_token=Depends(oauth2_scheme),
):
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=access_token
        ))
    file_content = await file.read()
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.UploadFile(user_pb2.UploadFileRequest(
            file_content=file_content,
            is_avatar=is_avatar,
            content_type=file.content_type,
            user_id=str(response.sub)
        ))
    return response.message


async def grpc_update_user(
        update_user_data: UpdateUserRequestDto,
        access_token = Depends(oauth2_scheme),
) -> UpdateUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.UpdateUserProfile(user_pb2.UpdateUserProfileRequest(
            **update_user_data.to_dict(), user_id=response.sub
        ))
    return UpdateUserResponseDto(message=response.message)


async def grpc_change_password(
        change_password_data: ChangePasswordRequestDto,
        access_token=Depends(oauth2_scheme),

) -> ChangePasswordResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=access_token
        ))

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.ChangePassword(user_pb2.ChangePasswordRequest(
            **change_password_data.to_dict(), user_id=response.sub
        ))
    return ChangePasswordResponseDto(
        token_type=response.token_type,
        access_token=response.access_token,
        refresh_token=response.refresh_token
    )


async def grpc_add_role(
        add_role_data: AddRoleRequestDto,
        access_token = Depends(oauth2_scheme),
) -> AddRoleResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.AddRole(user_pb2.AddRoleRequest(
            account_type=add_role_data.account_type.value,
            user_id=response.sub
        ))
    return AddRoleResponseDto(message=response.message)


async def grpc_get_boxer_by_id(
        user_id: Annotated[UUID, Path(description="The UUID id of the user")],
):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.UserBoxerProfile(user_pb2.UserBoxerProfileRequest(
            user_id=str(user_id)
        ))

    return UserBoxerProfileResponseDto(
        first_name=response.first_name,
        last_name=response.last_name,
        sex=response.sex,
        birthday=response.birthday,
        country=response.country,
        region=response.region,
        weight=response.weight,
        height=response.height,
        athletic_distinction=response.athletic_distinction,
        avatar=response.avatar
    )
