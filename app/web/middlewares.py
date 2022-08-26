import base64
import json
import typing

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException, HTTPForbidden, HTTPUnauthorized
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from app.admin.models import Admin
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: 'bad_request',
    401: 'unauthorized',
    403: 'forbidden',
    404: 'not_found',
    405: 'not_implemented',
    409: 'conflict',
    500: 'internal_server_error',
}


@middleware
async def auth_middleware(request: 'Request', handler) -> None:
    session = await get_session(request)
    if session.new:
        request.admin = None
    else:
        request.admin = Admin(
            id=session['admin']['id'],
            email=session['admin']['email']
        )
    return await handler(request)


@middleware
async def error_handling_middleware(request: 'Request', handler) -> None:
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status='bad_request',
            message=e.reason,
            data=json.loads(e.text))
    except HTTPException as e:
        return error_json_response(http_status=e.status,
                                   status=HTTP_ERROR_CODES[e.status],
                                   message=e.reason)
    except Exception as e:
        return error_json_response(http_status=500,
                                   status=HTTP_ERROR_CODES[500],
                                   message=str(e))


def setup_middlewares(app: 'Application') -> None:
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
