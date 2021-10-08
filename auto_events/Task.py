from datetime import datetime
from typing import Any, Callable, Optional
import string
import random

from .deafults import default_callback


class Task:
    """Create task used in `Event`

    Paramaters
    ----------
    id: `Optional[str]`, default `None`
        id of tasks (if not provided 16 chars random string)
    run_date: `'datetime'` 
        datetime when task will be run
    to_run: `Callable[[], bool]`, default `default_callback`
        callback function that will run when run_date is now
    on_success: Optional[Callable[[Any], None]], default `default_callback`
        callback function runned if `to_run` return `True`
    on_failure: Optional[Callable[[Any], None]], default `default_callback`
        callback function runned if `to_run` returns `False`
    """

    def __init__(self, run_date: 'datetime', id: Optional[str] = None, to_run: Callable[[], bool] = default_callback, on_success: Optional[Callable[[Any], None]] = default_callback, on_failure: Optional[Callable[[Any], None]] = default_callback) -> None:
        if id != None:
            self.id = id
        else:
            self.id = self.__generate_id()

        self.to_run = to_run
        self.on_success = on_success
        self.on_failure = on_failure
        self.run_date = run_date

    def trigger(self) -> bool:
        """Runs `to_run` and `on_success`/`on_failure` based on retuned value of `to_run`

        Returns
        -------
        bool
            if task was runned succesfully
        """
        is_success = False
        try:
            is_success = self.to_run()
        except Exception:
            print("[Task id: {}}] TASK FAILED: exception cougth".format(self.id))
        print("[Task] Task: " + self.id +
              " RUNNED" if is_success else " FAILED")

        if is_success and self.on_success != None:
            self.on_success()
        elif not is_success and self.on_failure != None:
            self.on_failure()

        return is_success

    def __generate_id(self, length: int = 16) -> str:
        """Generates randome string of length

        Paramaters
        ----------
        length: `int`, default `16`
            length of retuned string

        Returns
        -------
        `str`
            random generated id
        """
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def __eq__(self, other: 'Task') -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return "(Task) { " + "id: " + str(self.id) + " }"
