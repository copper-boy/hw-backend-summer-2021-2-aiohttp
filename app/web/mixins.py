from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, Optional

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from aiohttp.web_response import Response
from aiohttp_session import get_session

from app.web.utils import error_json_response

if TYPE_CHECKING:
    from app.web.app import Request


class AuthRequiredMixin:
    async def auth_required(self, request: 'Request'):
        session = await get_session(request=request)
        email = session.get('email')

        if email is None:
            return error_json_response(http_status=401, message='no session yet', status='unauthorized')

        admin = await request.app.store.admins.get_by_email(email)
        if not admin:
            return error_json_response(http_status=403, message='not a valid email', status='forbidden')
        return email
