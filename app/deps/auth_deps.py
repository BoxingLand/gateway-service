import grpc

from app.client.auth import auth_pb2_grpc, auth_pb2
from app.client.user import user_pb2_grpc, user_pb2
from app.dto.request.auth import SignupRequestDto, SigninRequestDto, RefreshRequestDto
from app.dto.response.auth import SigninResponseDto, SignupResponseDto, RefreshResponseDto


async def grpc_signup(
        signup_data: SignupRequestDto
) -> SignupResponseDto:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.Signup(user_pb2.SignupRequest(
            **signup_data.model_dump()
        ))
        return SignupResponseDto(message=response.message)


async def grpc_signin(
        signin_data: SigninRequestDto
) -> SigninResponseDto:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        response = await stub.Signin(user_pb2.SigninRequest(
            email=signin_data.email,
            phone_number=signin_data.phone_number,
            password=signin_data.password
        ))
        return SigninResponseDto(
            token_type=response.token_type,
            access_token=response.access_token,
            refresh_token=response.refresh_token
        )


async def grpc_refresh(
        refresh_data: RefreshRequestDto
) -> RefreshResponseDto:
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        response = await stub.Refresh(auth_pb2.RefreshRequest(
            refresh_token=refresh_data.refresh_token
        ))
        return RefreshResponseDto(
            token_type=response.token_type,
            access_token=response.access_token,
            refresh_token=response.refresh_token
        )