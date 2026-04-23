import pytest

from src.config import setting
from src.database import engine_null_pool
from src.models import *


@pytest.fixture(scope="session")
def check_test():
    assert setting.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)