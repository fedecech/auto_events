from datetime import datetime
from typing import List, Optional
from O365.calendar import Event as MicrosoftEvent
import random
import string

from .Task import Task


class Event:

    def __init__(self, start_date: 'datetime', end_date: 'datetime',  title: str, tasks: List['Task']) -> None:
        self.id = self.__generate_id()
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.tasks = tasks

    def trigger_tasks(self, id: Optional[str] = None, trigger_all: bool = True):
        if trigger_all:
            for task in self.tasks:
                task.trigger()
        elif id != None:
            index = self.tasks.index(id)
            if(index != None or index != -1):
                self.tasks[index].trigger()

    def add_task(self, task: 'Task'):
        self.tasks.append(task)

    def from_microsoft_event(micro_event: 'MicrosoftEvent') -> 'Event':
        subject = micro_event.subject
        start = micro_event.start
        end = micro_event.end
        tasks = []
        return Event(start_date=start, end_date=end, title=subject, tasks=tasks)

    def __generate_id(self, length: int = 16) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def __eq__(self, other: 'Event') -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return "(Event){ " + "Title: " + self.title.upper() + ", Trigger date: " + "#Tasks: " + str(len(self.tasks)) + " }"
