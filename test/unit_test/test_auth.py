from src.database import async_session_maker_null_pool
from src.schemas.users import UserAddDTO, UserAddRequestDTO
from src.services.users import UserService
from src.utils.db_manager import DBManager


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = UserService().create_access_token(data)
    assert jwt_token
    assert isinstance(jwt_token, str)




# async def test_register_user():
#     data = UserAddDTO(
#         username='user',
#         email="user@exm.com",
#         hashed_password="qwe",
#         role_id=3
#     )
#     async with DBManager(session_factory=async_session_maker_null_pool) as db:
#         user = await db.users.add(data)