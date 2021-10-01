from typing import Any, Callable, Optional
import string
import random


class Task:
    def __init__(self, id: Optional[str] = None, to_run: Callable[[], bool] = None, on_success: Optional[Callable[[Any], None]] = None, on_failure: Optional[Callable[[Any], None]] = None) -> None:
        if id != None:
            self.id = id
        else:
            self.id = self.__generate_id()

        self.to_run = to_run
        self.on_success = on_success
        self.on_failure = on_failure

    def trigger(self) -> bool:
        is_success = self.to_run()
        print("[Task] Task: " + self.id +
              " RUNNED" if is_success else " FAILED")

        if is_success and self.on_success != None:
            self.on_success()
        elif not is_success and self.on_failure != None:
            self.on_failure()

        return is_success

    def __generate_id(self, length: int = 16) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def __eq__(self, other: 'Task') -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return "(Task) { " + "id: " + str(self.id) + " }"
