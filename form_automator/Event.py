from datetime import datetime
from re import sub
from typing import List, Optional
from Task import Task
from O365.calendar import Event as MicrosoftEvent


class Event:

    def __init__(self, start_date: 'datetime', end_date: 'datetime', trigger_date: 'datetime', title: str, tasks: List['Task']) -> None:
        self.start = start_date
        self.end_date = end_date
        self.trigger_date = trigger_date
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
        trigger = end
        tasks = []
        return Event(start_date=start, end_date=end, trigger_date=trigger, title=subject, tasks=tasks)

    def __lt__(self, other: 'Event'):
        return self.trigger_date < other.trigger_date

    def __str__(self) -> str:
        return "(Event){ " + "Title: " + self.title.upper() + ", Trigger date: " + datetime.strftime(self.trigger_date, '%d/%m/%Y %H:%M') + " }"
