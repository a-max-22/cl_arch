from typing import List, Dict


from robot_events import *
from robot_commands import Command
from robot_event_processors import EventProcessor


class EventStore:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}
        self._event_processors: Dict[str, List[EventProcessor]] = {}
    
    def _notify_processors(self, robot_id:str,  new_events:List[Event]):
        for event in new_events:
            evt_type = event.get_event_type()
            if evt_type not in self._event_processors:
                continue
            for processor in self._event_processors[evt_type]:
                processor.new_event(event, robot_id)

    def _process_all_events(self):
        new_events_count = 0
        for evt_type in self._event_processors:
            for processor in self._event_processors[evt_type]:
                new_events = processor.do_unprocessed_events()
                for events, robot_id in new_events:
                    self.append_events(robot_id, events)
                new_events_count += len(new_events)
        
        return new_events_count
    
    def append_events(self, robot_id: str, events: List[Event]):
        if robot_id not in self._events:
            self._events[robot_id] = []        
        self._events[robot_id].extend(events)
        self._notify_processors(robot_id, events)
        self._process_all_events()


    def subscribe(self, event_type:str, event_processor:EventProcessor):
        if event_type not in self._event_processors:
            self._event_processors[event_type] = []
        self._event_processors[event_type].append(event_processor)




    def get_events(self, robot_id: str) -> List[Event]:
        return self._events.get(robot_id, [])


class CommandHandler:
    def __init__(self, event_store:EventStore):
        self.event_store = event_store
        
    def handle_command(self, robot_id:str, command:Command):
        events = command.handle()
        self.event_store.append_events(robot_id, events)


class StateProjector:
    def __init__(self, initial_state: RobotState):
        self._initial_state = initial_state
    
    def project_state(self, events: List[Event]) -> RobotState:
        current_state = self._initial_state
        for event in events:
            current_state = event.apply(current_state)
        return current_state