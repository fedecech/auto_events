from datetime import datetime
from typing import Any, Callable, List, Optional
import sched
import time
from apscheduler.schedulers.background import BackgroundScheduler

from .Source import Source
from .Event import Event


class Calendar:
    update_events = False
    # filter function is called in [Source] when events are parse from API data to Event obj
    # it takes an Event and should return a new Event modified
    # events need to be already sorted if passed in constructor

    def __init__(self, from_source: bool = True, events: Optional[List['Event']] = None, source: Optional['Source'] = None, filter: Optional[Callable[['Event'], bool]] = None, map: Optional[Callable[['Event'], 'Event']] = None) -> None:
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
                    filter=filter, map=map, should_login=(not Calendar.update_events))
        elif events != None:
            self.events = events
        else:
            self.events = []

    # dont't update when object just init
    # so we can just call update instead of update and listen_for_events_triggering
    def update(self) -> None:
        if self.source == None or not self.from_source:
            self.listen_for_events_triggering()
            return

        if Calendar.update_events:
            self.previous = self.events
            self.events = self.source.load_events(filter=self.filter, map=self.map,
                                                  should_login=(not Calendar.update_events))
        else:
            Calendar.update_events = True
        self.listen_for_events_triggering()

    # when trigger event date is date.now() runs that event's tasks (event.trigger_tasks)
    def listen_for_events_triggering(self) -> None:
        if len(self.events) < 1 or self.events == self.previous:
            return

        print("[Calendar] Calculating tasks...")
        for event in self.events:
            if len([e == event for e in self.previous]) == 0:
                for task in event.tasks:
                    self.scheduler.add_job(trigger='date', run_date=datetime.strftime(
                        task.run_date, '%Y-%m-%d %H:%M:%S'), func=task.trigger)
                print('[Calendar] ' + str(event) + " ADDED TO QUEUE")

        # print("Total queue length: " + str(len(self.scheduler.queue)))
