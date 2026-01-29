from abc import ABC, abstractmethod
from robot_events import *
from typing import List, Tuple

class EventProcessor:
    def __init__(self, event_store):
        self.event_store = event_store
        self.unprocessed_events:List[Tuple[Event, str]] = []

    def new_event(self, event:Event, robot_id:str):
        self.unprocessed_events.append((event, robot_id))

    def do_unprocessed_events(self) -> List[Tuple[Event, str]]:
        new_events:List[Tuple[Event, str]]  = []
        for event, robot_id in self.unprocessed_events:
            new_events.append((self._process_event(event), robot_id))
        self.unprocessed_events = []
        return new_events

    def _process_event(self, event:Event) -> List[Event]:
        return []


class RobotMoveRequestedProcessor(EventProcessor):
    def _process_event(self, event:RobotMoveRequested) -> List[Event]:
        return [RobotMovedEvent(event.distance)]

class RobotTurnRequestedProcessor(EventProcessor):
    def _process_event(self, event:RobotTurnRequestedEvent) -> List[Event]:
        return [RobotTurnedEvent(event.angle)]

class RobotStateChangeRequestProcessor(EventProcessor):
    def _process_event(self, event:RobotStateChangedEvent) -> List[Event]:
        return [RobotStateChangedEvent(event.new_state)]

class RobotStartRequestedProcessor(EventProcessor):
    def _process_event(self, event:RobotStartRequestedEvent) -> List[Event]:
        return [RobotStartedEvent()]

class RobotStopRequestedProcessor(EventProcessor):
    def _process_event(self, event:RobotStopRequestedEvent) -> List[Event]:
        return [RobotStoppedEvent()]
