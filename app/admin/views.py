import base64
from hashlib import sha256

from aiohttp.web_exceptions import HTTPForbidden
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
        existed_admin = await self.request.app.store.admins.get_by_email(data['email'])
        if not existed_admin:
            raise HTTPForbidden
        if sha256(data['password'].encode('utf-8')).hexdigest() != existed_admin.password:
            raise HTTPForbidden

        raw_admin = AdminResponseSchema().dump(existed_admin)

        session = await new_session(request=self.request)
        session['admin'] = raw_admin

        return json_response(data=raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminResponseSchema)
    async def get(self):
        return json_response(data=AdminResponseSchema().dump(self.request.admin))
