from src.services.base import BaseService


class NotificationsServices(BaseService):
    async def get_notifications(self):
        return "notifications"
