import pytest

from src.config import setting
from src.database import engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.roles import RoleAddDTO
from src.utils.db_manager import DBManager

from httpx import ASGITransport, AsyncClient

@pytest.fixture(scope="session")
def check_test():
    assert setting.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def create_default_roles(setup_database):
    roles_data = [
        {"name": "admin", "description": "Администратор"},
        {"name": "author", "description": "Автор книг"},
        {"name": "user", "description": "Обычный пользователь"},
    ]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for data in roles_data:
            role_dto = RoleAddDTO(**data)
            await db.roles.add(role_dto)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/auth/register",
                                 json={"username": "user",
                                       "email": "user@exm.com",
                                       "password": "string"}
                                 )
        assert response.status_code == 201

# @pytest.fixture(scope="session")
# async def ac():
#     async with AsyncClient(
#             transport=ASGITransport(app=app), base_url="http://test") as ac:
#         yield ac
#
# async def register_admin(ac):
#     await ac.post("/auth/register", json={"email": "admin@exm.com", })