import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.config import setting
from src.database import async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models import *
from src.schemas.roles import RoleAddDTO
from src.schemas.users import UserAddDTO
from src.services.users import UserService
from src.utils.db_manager import DBManager


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool
"""Фикстура на создание сессии, Она видна во всем pytest"""


@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


"""Фикстура на Асинхронного клиента , который обращается по API. Виден во всем pytest"""


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def check_test():
    assert setting.MODE == "TEST"


"""Фикстура для поднятия БД Так же добавляются данные через roles users JSON
Здесь оправданно повторно создавать _db в остальных случаех ее прокидываем"""


@pytest.fixture(scope="session", autouse=True)
async def setup_database(ac, check_test):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("test/mock_role_data.json", encoding="utf-8") as f:
        roles_data = json.load(f)
        roles_schemas = [RoleAddDTO(**role) for role in roles_data]

    with open("test/mock_users_data.json", encoding="utf-8") as f:
        users_data = json.load(f)
    users_schemas = []
    for user in users_data:
        hashed_password = UserService().get_password_hash(user["password"])
        users_schemas.append(
            UserAddDTO(
                username=user["username"],
                email=user["email"],
                hashed_password=hashed_password,
                role_id=user["role_id"],
            )
        )

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        for role in roles_schemas:
            await _db.roles.add(role)

        for data in users_schemas:
            await _db.users.add(data)
        await _db.commit()
