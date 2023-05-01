from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import Delete, Insert, Update

from src.core.config import CONFIG

# Create a context variable for the session context
session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    """
    Get the current session context value.
    :return: The current session context value.
    """
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    """
    Set the session context value.
    :param session_id: The session ID to set as the context value.
    :return: A token representing the previous session context value.
    """
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    """
    Reset the session context value to a previous value.
    :param context: The token representing the previous session context value.
    """
    session_context.reset(context)


# Create the reader and writer engines for the database
engines = {
    "writer": create_async_engine(CONFIG.MYSQL_URL, pool_recycle=3600),
    "reader": create_async_engine(CONFIG.MYSQL_URL, pool_recycle=3600),
}

# Disable echoing of SQL statements for both engines
engines["reader"].echo = False
engines["writer"].echo = False


# Custom session class to handle read-write routing
class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        # Use the writer engine for flushing and write operations
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        # Use the reader engine for other operations
        return engines["reader"].sync_engine


# Create an async session factory
async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

# Create an async scoped session
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


async def get_session():
    """
    Get the database session.
    This can be used for dependency injection.
    :return: The database session.
    """
    try:
        yield session
    finally:
        await session.close()


Base = declarative_base()
