from enum import Enum
from functools import wraps
from .session import session

class Propagation(Enum):
    """
    Enumeration for transaction propagation types.

    - REQUIRED: The transaction will participate in an existing transaction, or a new transaction will be started.
    - REQUIRED_NEW: The transaction will always start a new transaction, suspending the current transaction if one exists.
    """
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"

class Transactional:
    """
    Decorator for providing transactional behavior to a function.

    This decorator is used to wrap a function and provide transactional behavior
    to the function's execution. It supports different transaction propagation types.

    Usage:
    @Transactional(propagation=Propagation.REQUIRED)
    async def my_function(...):
        # Function code goes here

    Parameters:
    - propagation: The transaction propagation type to use. Defaults to Propagation.REQUIRED.

    Returns:
    - The decorated function.

    Notes:
    - The decorator creates a transaction around the function execution.
    - The session is used for managing the transaction.
    - The transaction is committed if the function executes successfully.
    - The transaction is rolled back if an exception occurs during function execution.
    - Supports two propagation types: REQUIRED and REQUIRED_NEW.
    - REQUIRED: The transaction participates in an existing transaction or starts a new one.
    - REQUIRED_NEW: The transaction always starts a new one, suspending the current transaction.
    """

    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                match self.propagation:
                    case Propagation.REQUIRED:
                        result = await self._run_required(
                            function=function,
                            args=args,
                            kwargs=kwargs,
                        )
                    case Propagation.REQUIRED_NEW:
                        result = await self._run_required_new(
                            function=function,
                            args=args,
                            kwargs=kwargs,
                        )
                    case _:
                        result = await self._run_required(
                            function=function,
                            args=args,
                            kwargs=kwargs,
                        )
            except Exception as exception:
                await session.rollback()
                raise exception

            return result

        return decorator

    async def _run_required(self, function, args, kwargs) -> None:
        """
        Run the function within an existing or new transaction (REQUIRED).
        """
        result = await function(*args, **kwargs)
        await session.commit()
        return result

    async def _run_required_new(self, function, args, kwargs) -> None:
        """
        Run the function within a new transaction (REQUIRED_NEW).
        """
        session.begin()
        result = await function(*args, **kwargs)
        await session.commit()
        return result
