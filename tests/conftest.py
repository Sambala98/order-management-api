import os
import pytest
from alembic import command
from alembic.config import Config

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    # This should point to the Alembic config inside container (/app)
    alembic_cfg = Config("alembic.ini")

    # Run migrations
    command.upgrade(alembic_cfg, "head")

    yield