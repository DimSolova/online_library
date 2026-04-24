import json

import pytest

from src.config import setting
from src.database import engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.roles import RoleAddDTO
from src.schemas.users import UserAddDTO
from src.utils.db_manager import DBManager

from httpx import ASGITransport, AsyncClient

"""Фикстура на создание сессии, Она видна во всем pytest"""
@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

"""Фикстура на Асинхронного клиента , который обращается по API. Виден во всем pytest"""
@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def check_test():
    assert setting.MODE == "TEST"

#TODO Users создаются не с хэшированыыми паролями // Нужно Зарегистрировать их через API или захэшировать пароль
"""Фикстура для поднятия БД Так же добавляются данные через roles users JSON
Здесь оправданно повторно создавать _db в остальных случаех ее прокидываем"""
@pytest.fixture(scope="session", autouse=True)
async def setup_database(ac, check_test):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("test/mock_users_data.json", encoding="utf-8") as f:
        users_data = json.load(f)
    users_schemas = [UserAddDTO(**user) for user in users_data]

    with open("test/mock_role_data.json", encoding="utf-8") as f:
        roles_data = json.load(f)
        roles_schemas = [RoleAddDTO(**role) for role in roles_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        for role in roles_schemas:
            await _db.roles.add(role)


        for data in users_schemas:
            await _db.users.add(data)
        await _db.commit()


"""Фикстура Асинхронного клиента на регистрацию"""
@pytest.fixture(scope="session", autouse=True)
async def test_root(ac):

    response = await ac.post("/auth/register",
                             json={"username": "user",
                                   "email": "user@exm.com",
                                   "password": "string"}
                             )
    assert response.status_code == 201

