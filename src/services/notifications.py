from src.services.base import BaseService


class NotificationsServices(BaseService):
    async def get_notifications(self, user_id):
        notification = await self.db.notifications.get_filtered(user_id=user_id)
        return notification
