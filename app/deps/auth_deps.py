import grpc

from app.client.auth import auth_pb2_grpc, auth_pb2
from app.client.user import user_pb2_grpc, user_pb2
from app.dto.request.auth import SignupRequestDto, SigninRequestDto, RefreshRequestDto
from app.dto.response.auth import SigninResponseDto, SignupResponseDto, RefreshResponseDto
from app.errors.auth_errors import TokenIncorrectError, TokenExpiredSignatureError, TokenDecodeError, \
    TokenMissingRequiredClaimError
from app.errors.user_errors import UserPasswordNotMatchError, UserEmailExistError, UserPhoneNumberExistError, \
    UserCreateError, UserNotFoundError, UserValidateError


async def grpc_signup(
        signup_data: SignupRequestDto
) -> SignupResponseDto:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        try:
            response = await stub.Signup(user_pb2.SignupRequest(
                **signup_data.model_dump()
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise UserPasswordNotMatchError()
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS and e.details() == "Email":
                raise UserEmailExistError(email=signup_data.email)
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS and e.details() == "Phone":
                raise UserPhoneNumberExistError(phone_number=signup_data.phone_number)
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise UserCreateError()

        return SignupResponseDto(message=response.message)


async def grpc_signin(
        signin_data: SigninRequestDto
) -> SigninResponseDto:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserStub(channel)
        try:
            response = await stub.Signin(user_pb2.SigninRequest(
                email=signin_data.email,
                phone_number=signin_data.phone_number,
                password=signin_data.password
            ))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise UserValidateError()
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise UserNotFoundError()
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
        try:
            response = await stub.Refresh(auth_pb2.RefreshRequest(
                refresh_token=refresh_data.refresh_token
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

        return RefreshResponseDto(
            token_type=response.token_type,
            access_token=response.access_token,
            refresh_token=response.refresh_token
        )