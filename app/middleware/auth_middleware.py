from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

API_KEY = "mysecretapikey123"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        api_key = request.headers.get('X-API-KEY')
        if api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        response = await call_next(request)
        return response