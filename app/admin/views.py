import base64
from hashlib import sha256

from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.web.app import View
from app.admin.schemes import AdminResponseSchema, AdminRequestSchema
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class AdminLoginView(View):
    @request_schema(AdminRequestSchema)
    @response_schema(AdminResponseSchema)
    async def post(self):
        data = self.request['data']
        admin = await self.request.app.store.admins.get_by_email(data['email'])
        if not admin:
            return error_json_response(http_status=403, message='invalid email or password', status='forbidden')
        if sha256(data['password'].encode('utf-8')).hexdigest() != admin.password:
            return error_json_response(http_status=403, message='invalid email or password', status='forbidden')

        session = await new_session(request=self.request)
        session['email'] = admin.email

        return json_response(data=AdminResponseSchema().dump(admin))


class AdminCurrentView(View, AuthRequiredMixin):
    @response_schema(AdminResponseSchema)
    async def get(self):
        result = await self.auth_required(self.request)
        if not isinstance(result, str):
            return result

        admin = await self.request.app.store.admins.get_by_email(result)

        return json_response(data=AdminResponseSchema().dump(admin))
