from __future__ import annotations

from asyncio import TimeoutError


class Reschedule(Exception):
    """Reschedule this task

    Raising this exception will stop the current execution of the task and ask
    the scheduler to reschedule this task, possibly on a different machine.

    This does not guarantee that the task will move onto a different machine.
    The scheduler will proceed through its normal heuristics to determine the
    optimal machine to accept this task.  The machine will likely change if the
    load across the cluster has significantly changed since first scheduling
    the task.
    """


class WorkerStartTimeoutError(TimeoutError):
    """Raised when the expected number of workers to not start within the timeout period."""

    #: Number of workers that are available.
    available_workers: int

    #: Number of workers that were expected to be available.
    expected_workers: int

    #: Timeout period in seconds.
    timeout: float

    def __init__(
        self, available_workers: int, expected_workers: int, timeout: float
    ) -> None:
        # Directly call super().__init__ with preformatted string to optimize __str__ and argument passing
        # This avoids constructing tuple and string formatting each time __str__ is called.
        self.available_workers = available_workers
        self.expected_workers = expected_workers
        self.timeout = timeout
        self._str_msg = f"Only {available_workers}/{expected_workers} workers arrived after {timeout}"
        super().__init__(self._str_msg)

    def __str__(self) -> str:
        return self._str_msg
