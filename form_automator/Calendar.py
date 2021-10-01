from Source import Source
from typing import Any, Callable, List, Optional
from Event import Event
import sched
import time


class Calendar:
    update_events = False
    # filter function is called in [Source] when events are parse from API data to Event obj
    # it takes an Event and should return a new Event modified
    # events need to be already sorted if passed in constructor

    def __init__(self, events: Optional[List['Event']] = None, source: Optional['Source'] = None, filter: Optional[Callable[['Event'], bool]] = None, map: Optional[Callable[['Event'], 'Event']] = None) -> None:
        # self.update_events = False
        self.filter = filter
        self.map = map
        # load from ICal/Microsoft Cal/Google Cal
        if (source != None):
            self.source = source

            # first Calendar instance needs to login next ones no... but update_events need to be False at the start so that update doesnt get triggered immidiatly
            self.events = source.load_events(
                filter=filter, map=map, should_login=(not Calendar.update_events))
        # Passing events -> custom way of creating them
        elif events != None:
            self.events = events
        else:
            self.events = []

    # dont't update when object just init
    # so we can just call update instead of update and listen_for_events_triggering
    def update(self):
        if self.source == None:
            return

        if Calendar.update_events:
            self.events = self.source.load_events(filter=self.filter, map=self.map,
                                                  should_login=(not Calendar.update_events))
        else:
            Calendar.update_events = True
        self.listen_for_events_triggering()

    # when trigger event date is date.now() runs that event's tasks (event.trigger_tasks)
    def listen_for_events_triggering(self):
        if len(self.events) < 1:
            return

        print("[Calendar] Calculating tasks...")
        scheduler = sched.scheduler(time.time, time.sleep)
        for event in self.events:
            date = event.trigger_date
            ts = date.timestamp()

            scheduler.enterabs(ts, 0,
                               event.trigger_tasks)
            print('[Calendar] ' + str(event) + " ADDED TO QUEUE")

        print("Total queue length: " + str(len(scheduler.queue)))

        scheduler.run(blocking=False)
