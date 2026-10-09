import time
import traceback
from datetime import datetime
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Optional

RESET = "\033[0m"
CHECK_MARK = "\u2705"
CROSS_MARK = "\u274c"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Log the start, duration and result of a test function.

    Args:
        func: The test function to wrap.

    Returns:
        Callable: The wrapped function with logging.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Run the wrapped function and print timing information.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            Any: The result of the wrapped function, or None on error.
        """
        start_time: float = time.time()
        timestamp_start: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(
            f"{YELLOW}[{timestamp_start}]{RESET}"
            + f" {BLUE}Commencing Test ({func.__module__})\n"
            + f"Running test function{RESET}"
            + f" {func.__name__}"
        )

        result: Any = None
        tb: Optional[TracebackType] = None
        error: str = ""

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            tb = e.__traceback__
            error = str(e)

        duration: float = time.time() - start_time
        timestamp_end: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if tb is None:
            status: str = f"{GREEN}{CHECK_MARK} Success{RESET}"
            stack_info: str = ""
        else:
            status = f"{RED}{CROSS_MARK} Failure: {error}{RESET}"
            stack_info = f"Stack trace info:\n{tb}\n"

        print(
            f"{YELLOW}[{timestamp_end}]{RESET}"
            + f"{BLUE} Ran function in {duration:.4f} seconds{RESET} - "
            + f"{status}\n"
            + stack_info
            + "-" * 68
            + "\n"
        )

        return result

    return wrapper
