from uuid import uuid4
from .session import reset_session_context, session, set_session_context

def standalone_session(func):
    """
    Decorator for providing a standalone session to a function.

    This decorator is used to wrap a function and provide it with a separate session
    for each invocation. It ensures that the function operates within its own session
    context, handles exceptions, and performs proper session cleanup.

    Usage:
    @standalone_session
    async def my_function(...):
        # Function code goes here

    Parameters:
    - func: The function to be decorated.

    Returns:
    - The decorated function.

    Notes:
    - Each invocation of the decorated function will have its own unique session ID.
    - The session ID is stored in the session context using ContextVar.
    - Exceptions that occur during function execution will cause a session rollback.
    - The session is removed from the current context after function execution.
    - The session context is reset to the previous value after function execution.
    """

    async def _standalone_session(*args, **kwargs):
        # Generate a new session ID
        session_id = str(uuid4())

        # Set the session context to the new session ID
        context = set_session_context(session_id=session_id)

        try:
            # Call the decorated function
            await func(*args, **kwargs)
        except Exception as exception:
            # Rollback the session in case of an exception
            await session.rollback()
            raise exception
        finally:
            # Remove the session from the current context
            await session.remove()

            # Reset the session context to the previous value
            reset_session_context(context=context)

    return _standalone_session
