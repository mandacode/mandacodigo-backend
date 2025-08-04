import datetime
from collections import defaultdict, deque

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class RateLimiter:

    def __init__(self, limit: int = 3, time_window: int = 10) -> None:
        self._mapper = defaultdict(deque)
        self._limit = limit
        self._time_window = time_window

    def check_request(self, ip_address: str) -> bool:
        now = datetime.datetime.now()
        self._mapper[ip_address].append(now)

        while (
            self._mapper[ip_address]
            and now - self._mapper[ip_address][0] > datetime.timedelta(seconds=self._time_window)
        ):
            self._mapper[ip_address].popleft()

        if len(self._mapper[ip_address]) > self._limit:
            return False

        return True


app = FastAPI()
rate_limiter = RateLimiter()


@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next: callable):
    is_valid = rate_limiter.check_request(ip_address=request.client.host)

    if not is_valid:
        return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

    response = await call_next(request)
    return response


@app.post("/auth/login")
async def login_controller(dto: LoginSchema):
    return {"message": "success"}
