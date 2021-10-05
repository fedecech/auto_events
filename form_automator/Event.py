from datetime import datetime
from typing import List, Optional
from O365.calendar import Event as MicrosoftEvent
import random
import string

from .Task import Task


class Event:
    """Create a new Event to add to calendar

    Paramaters
    ----------
    title: str
        title of the event
    start_date: `'datetime'`
        when the event starts
    end_date: `'datetime'`
        when the event ends
    tasks: `List['Task']`
        list of tasks to execute for this event
    id: `Optional[str]`, default `None`
        id of the event (if not provided a random 16 chars string)
    """

    def __init__(self, start_date: 'datetime', end_date: 'datetime',  title: str, tasks: List['Task'] = [], id: Optional[str] = None) -> None:
        if id != None:
            self.id = id
        else:
            self.id = self.__generate_id()

        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.tasks = tasks

    def add_tasks(self, tasks: List['Task']) -> None:
        """Add a list of tasks to event

        Paramaters
        ----------

        tasks: `List['Task']`
            tasks to add to end of event.tasks list

        Returns
        -------
        `None`
        """
        self.tasks.extend(tasks)

    def add_task(self, task: 'Task') -> None:
        """Add taks to event

        Paramaters
        ----------
        task: `'Task'`
            task to ass to end of event.tasks list

        Returns
        -------
        `None`
        """
        self.tasks.append(task)

    def from_microsoft_event(micro_event: 'MicrosoftEvent') -> 'Event':
        """Creates `Event` object from `MicrosoftEvent` (returned from API when using `MicrosoftSource`)

        Paramaters
        ----------
        micro_event: `'MicrosoftEvent'`
            obj returned from API (when using `MicrosoftSource`)

        Returns
        -------
        `'Event'`
        """
        subject = micro_event.subject
        start = micro_event.start
        end = micro_event.end
        tasks = []
        return Event(start_date=start, end_date=end, title=subject, tasks=tasks)

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

    def __eq__(self, other: 'Event') -> bool:
        """Verify if object are equal

        Paramaters
        ----------
        other: `'Event'`
            event to compare `self` with

        Returns
        -------
        bool
        """
        return self.id == other.id

    def __str__(self) -> str:
        return "(Event){ " + "Title: " + self.title.upper() + ", Trigger date: " + "#Tasks: " + str(len(self.tasks)) + " }"
