import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: 'Application'):
        self.app.database.admins = []
        await self.create_admin(self.app.config.admin.email, self.app.config.admin.password)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        try:
            return next(admin for admin in self.app.database.admins if admin.email == email)
        except StopIteration:
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(email=email, password=sha256(password.encode('utf-8')).hexdigest(),
                      id=self.app.database.next_admin_id)
        self.app.database.admins.append(admin)
        return admin
