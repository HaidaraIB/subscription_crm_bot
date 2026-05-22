from pathlib import Path

from models import *
from Config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from contextlib import contextmanager
from functools import wraps
import logging
import asyncio
import traceback
from common.error_handler import write_error

Base = declarative_base()
engine = create_engine(
    f"sqlite:///{Config.DB_PATH}",
    connect_args={"check_same_thread": False},
    pool_size=Config.DB_POOL_SIZE,
    max_overflow=Config.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)


def _run_alembic_upgrade() -> None:
    from alembic import command
    from alembic.config import Config as AlembicConfig

    ini_path = Path(__file__).resolve().parent.parent / "alembic.ini"
    alembic_cfg = AlembicConfig(str(ini_path))
    db_path = Path(Config.DB_PATH).as_posix()
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    # Do not let Alembic's fileConfig replace the app's logging setup.
    alembic_cfg.attributes["configure_logger"] = False
    logging.getLogger("alembic").setLevel(logging.WARNING)
    command.upgrade(alembic_cfg, "head")


def init_db():
    # Configure SQLite for better concurrency
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL"))
        conn.execute(text("PRAGMA synchronous=NORMAL"))
        conn.execute(text("PRAGMA foreign_keys=ON"))
        conn.execute(text("PRAGMA busy_timeout=5000"))
        conn.commit()

    Base.metadata.create_all(engine)
    _run_alembic_upgrade()
    from models.BotSettings import BotSettings

    with session_scope() as s:
        BotSettings.seed_defaults(s)


Session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of database operations.

    Yields:
        Session: A SQLAlchemy database session

    Raises:
        Exception: Any exception that occurs during the transaction will be
                  logged and re-raised after rolling back the transaction.
    """
    logger = logging.getLogger(__name__)

    session = Session()
    try:
        yield session
        session.commit()
        logger.debug("Transaction committed successfully")
    except Exception as e:
        session.rollback()
        logger.error(
            "Database transaction failed",
            exc_info=True,
            extra={"exception": str(e)},
        )
        write_error(traceback.format_exc())
    finally:
        session.close()
        logger.debug("Session closed")


def with_retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    if "database is locked" in str(e):
                        retries += 1
                        await asyncio.sleep(delay * retries)
                        continue
                    raise
            raise OperationalError("Max retries reached", None, None)

        return async_wrapper

    return decorator
