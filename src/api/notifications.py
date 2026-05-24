from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.services.favorites import FavoritesServices
from src.services.notifications import NotificationsServices

router = APIRouter(prefix="/auth/notifications", tags=["Уведомления"])


@router.get("")
async def get_notifications(
        user: UserIdDep,
        db: DBDep
):
    print(user.id)
    notifications = await NotificationsServices(db).get_notifications(user.id)
    return {"status": "success", "data": notifications}
