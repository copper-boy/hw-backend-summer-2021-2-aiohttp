from asyncio import CancelledError, Task
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.poll_task = Task(self.poll)

    async def stop(self):
        self.poll_task.cancel()

    async def poll(self):
        return self.poll_task

