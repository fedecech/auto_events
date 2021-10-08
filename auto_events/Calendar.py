from datetime import datetime
from typing import Callable, List, Optional
from apscheduler.schedulers.background import BackgroundScheduler

from .deafults import default_callback
from .Source import Source
from .Event import Event


class Calendar:
    """
    Create a new Calendar that will execute Event's Tasks

    Paramaters
    ----------
    from_source: bool, default True
        indicates if calendar should use source to fetch events
    events: Optional[List['Event']], default `[]`
        list of events (used if from_source=False)
    source: Optional['Source'], default None
        source used to fetche events from API
    filter: Optional[Callable[['Event'], bool]], default, `deafult_callback` 
        callback function used to filter events fetched using source from API
    map: Optional[Callable[['Event'], 'Event']], deafult `deafult_callback`
        callback function used to modify events fetched using source from API

    Raises
    ------
    Exception
        If from_source=True and source=None
    """

    update_events = False

    def __init__(self, from_source: bool = True, events: Optional[List['Event']] = [], source: Optional['Source'] = None, filter: Optional[Callable[['Event'], bool]] = default_callback, map: Optional[Callable[['Event'], 'Event']] = default_callback) -> None:
        self.filter = filter
        self.map = map
        self.from_source = from_source
        self.source = source
        self.scheduler = BackgroundScheduler()
        self.previous = []

        if from_source:
            if source == None:
                raise Exception('Need to provide Source')
            else:
                self.events = source.load_events(
                    filter=filter, map=map)
        else:
            if events != []:
                self.events = events

    def update(self) -> None:
        """Updates calendar by calling `source.load_events(filter=self.filter, map=self.map)` (`if source != None and from_source=True`) and
        updates scheduler with new fetched events (if any)

        Returns
        -------
        None
        """

        if self.source == None or not self.from_source:
            self.update_scheduler()
            return

        if Calendar.update_events:
            # self.previous = self.events
            self.events = self.source.load_events(
                filter=self.filter, map=self.map)

        else:
            Calendar.update_events = True
        self.update_scheduler()

    def update_scheduler(self) -> None:
        """Add new events to scheduler queue

        Returns
        -------
        None
        """

        if len(self.events) < 1 or self.events == self.previous:
            return

        tmp = self.events
        print("[Calendar] Calculating tasks...")
        for event in self.events:
            if len([e == event for e in self.previous]) == 0:
                for task in event.tasks:
                    self.scheduler.add_job(trigger='date', run_date=datetime.strftime(
                        task.run_date, '%Y-%m-%d %H:%M:%S'), func=task.trigger)
                print('[Calendar] ' + str(event) + " ADDED TO QUEUE")
        self.previous = tmp

    def listen(self):
        """Listen for tasks to be runned

        Returns
        -------
        None
        """
        self.scheduler.start()
