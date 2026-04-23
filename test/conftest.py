import pytest

from src.config import setting
from src.database import engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.schemas.roles import RoleAddDTO
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session")
def check_test():
    assert setting.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def create_role(setup_database):
    role = RoleAddDTO(
        name='admin',
        description='admin'
    )
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.roles.add(role)
        await db.commit()