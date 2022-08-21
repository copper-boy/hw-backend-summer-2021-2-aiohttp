import typing

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: 'Application'):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
        if updates:
            from_id = updates[0].object.message.from_id
            text = updates[0].object.message.text
            await self.app.store.vk_api.send_message(Message(from_id, text))
        return updates

