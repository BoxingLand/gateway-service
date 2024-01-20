import grpc

from app.client.auth import auth_pb2_grpc, auth_pb2
from app.client.user import user_pb2_grpc, user_pb2
from app.dto.request.profile import DeleteUserRequestDto, UpdateUserRequestDto, ChangePasswordRequestDto, \
    AddRoleRequestDto
from app.dto.response.profile import DeleteUserResponseDto, UpdateUserResponseDto, ChangePasswordResponseDto, \
    AddRoleResponseDto


async def grpc_delete_user(
        delete_user_data: DeleteUserRequestDto
) -> DeleteUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=delete_user_data.access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.DeleteUser(user_pb2.DeleteUserRequest(
            user_id=response.sub
        ))
    return DeleteUserResponseDto(message=response.message)

async def grpc_update_user(
        update_user_data: UpdateUserRequestDto
) -> UpdateUserResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=update_user_data.access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.UpdateUserProfile(user_pb2.UpdateUserProfileRequest(
            **update_user_data.to_dict(), user_id=response.sub
        ))
    return UpdateUserResponseDto(message=response.message)

async def grpc_change_password(
     change_password_data: ChangePasswordRequestDto
) -> ChangePasswordResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=change_password_data.access_token
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
        add_role_data: AddRoleRequestDto
) -> AddRoleResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Access(auth_pb2.AccessRequest(
            access_token=add_role_data.access_token
        ))
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.AddRole(user_pb2.AddRoleRequest(
            account_type=add_role_data.account_type.value,
            user_id=response.sub
        ))
    return AddRoleResponseDto(message=response.message)