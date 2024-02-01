from typing import Annotated
from uuid import UUID

import grpc
from fastapi import Path, UploadFile, Depends, Query

from app.api.v1.endpoints import oauth2_scheme
from app.client.auth import auth_pb2_grpc, auth_pb2
from app.client.user import user_pb2_grpc, user_pb2
from app.dto.request.user import UpdateUserRequestDto, ChangePasswordRequestDto, \
    AddRoleRequestDto
from app.dto.response.user import DeleteUserResponseDto, UpdateUserResponseDto, ChangePasswordResponseDto, \
    AddRoleResponseDto, UserBoxerProfileResponseDto, BoxerProfileResponseDto
from app.errors.auth_errors import TokenIncorrectError, TokenMissingRequiredClaimError, TokenDecodeError, \
    TokenExpiredSignatureError
from app.errors.user_errors import UserNotFoundError, UserPasswordNotMatchError, UserValidateError, UserRoleExistError


class BoxerProfileResponseDtoobj:
    pass


async def grpc_get_boxers_filtered_pagination(
        first_name: str | None = None,
        last_name: str | None = None,
        club: str | None = None,
        country: str | None = None,
        region: str | None = None,
        athletic_distinction: str | None = None,
        sex: str | None = None,
        min_weight: float | None = None,
        max_weight: float | None = None,
        min_height: float | None = None,
        max_height: float | None = None,
        min_age: int | None = None,
        max_age: int | None = None,
        min_birthday: str | None = None,
        max_birthday: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, le=100)
):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = stub.Boxers(user_pb2.BoxersRequest(
            first_name=first_name,
            last_name=last_name,
            club=club,
            country=country,
            region=region,
            athletic_distinction=athletic_distinction,
            sex=sex,
            min_weight=min_weight,
            max_weight=max_weight,
            min_height=min_height,
            max_height=max_height,
            min_age=min_age,
            max_age=max_age,
            min_birthday=min_birthday,
            max_birthday=max_birthday,
            page=page,
            page_size=page_size
        ))
        boxers = []
        async for obj in response:
            boxers.append(BoxerProfileResponseDto(
                first_name=obj.first_name,
                last_name=obj.last_name,
                club=obj.club,
                country=obj.country,
                region=obj.region,
                weight=obj.weight,
                birthday=obj.birthday,
                athletic_distinction=obj.athletic_distinction,
                avatar=obj.avatar
            ))
    return boxers


async def grpc_delete_user(
        access_token=Depends(oauth2_scheme),
) -> DeleteUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        try:
            response = await stub.Access(auth_pb2.AccessRequest(
                access_token=access_token
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenIncorrect":
                raise TokenIncorrectError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenExpiredSignature":
                raise TokenExpiredSignatureError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenDecode":
                raise TokenDecodeError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenMissingRequiredClaim":
                raise TokenMissingRequiredClaimError()

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
        try:
            response = await stub.Access(auth_pb2.AccessRequest(
                access_token=access_token
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenIncorrect":
                raise TokenIncorrectError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenExpiredSignature":
                raise TokenExpiredSignatureError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenDecode":
                raise TokenDecodeError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenMissingRequiredClaim":
                raise TokenMissingRequiredClaimError()

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
        access_token=Depends(oauth2_scheme),
) -> UpdateUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        try:
            response = await stub.Access(auth_pb2.AccessRequest(
                access_token=access_token
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenIncorrect":
                raise TokenIncorrectError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenExpiredSignature":
                raise TokenExpiredSignatureError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenDecode":
                raise TokenDecodeError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenMissingRequiredClaim":
                raise TokenMissingRequiredClaimError()

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
        try:
            response = await stub.Access(auth_pb2.AccessRequest(
                access_token=access_token
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenIncorrect":
                raise TokenIncorrectError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenExpiredSignature":
                raise TokenExpiredSignatureError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenDecode":
                raise TokenDecodeError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenMissingRequiredClaim":
                raise TokenMissingRequiredClaimError()

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        try:
            response = await stub.ChangePassword(user_pb2.ChangePasswordRequest(
                **change_password_data.to_dict(), user_id=response.sub
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise UserNotFoundError(incoming_id=response.sub)
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT and e.details() == "PasswordNotMatch":
                raise UserPasswordNotMatchError()
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT and e.details() == "WrongPassword":
                raise UserValidateError()

    return ChangePasswordResponseDto(
        token_type=response.token_type,
        access_token=response.access_token,
        refresh_token=response.refresh_token
    )


async def grpc_add_role(
        add_role_data: AddRoleRequestDto,
        access_token=Depends(oauth2_scheme),
) -> AddRoleResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        try:
            response = await stub.Access(auth_pb2.AccessRequest(
                access_token=access_token
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenIncorrect":
                raise TokenIncorrectError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenExpiredSignature":
                raise TokenExpiredSignatureError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenDecode":
                raise TokenDecodeError()
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED and e.details() == "TokenMissingRequiredClaim":
                raise TokenMissingRequiredClaimError()

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        try:
            response = await stub.AddRole(user_pb2.AddRoleRequest(
                account_type=add_role_data.account_type.value,
                user_id=response.sub
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise UserRoleExistError(role=add_role_data.account_type.value)
    return AddRoleResponseDto(message=response.message)


async def grpc_get_boxer_by_id(
        user_id: Annotated[UUID, Path(description="The UUID id of the user")],
):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        try:
            response = await stub.UserBoxerProfile(user_pb2.UserBoxerProfileRequest(
                user_id=str(user_id)
            ))

        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise UserNotFoundError(incoming_id=user_id)

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
