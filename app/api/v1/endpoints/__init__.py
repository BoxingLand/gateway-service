from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/signin")