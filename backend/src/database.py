from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .settings import database_settings


async_engine = create_async_engine(
    url=database_settings.DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
)