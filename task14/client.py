from robot_code import EventStore, RobotState, StateProjector, CommandHandler
from robot_commands import MoveCommand, TurnCommand, StartCommand, StopCommand, SetStateCommand
from robot import CleaningMode
from robot_events import *
from robot_event_processors import *

def main():

    event_store = EventStore()

    event_store.subscribe(RobotMoveRequested.type, RobotMoveRequestedProcessor(event_store))
    event_store.subscribe(RobotTurnRequestedEvent.type, RobotTurnRequestedProcessor(event_store))
    event_store.subscribe(RobotStateChangeRequestedEvent.type, RobotStateChangeRequestProcessor(event_store))
    event_store.subscribe(RobotStartRequestedEvent.type, RobotStartRequestedProcessor(event_store))
    event_store.subscribe(RobotStopRequestedEvent.type, RobotStopRequestedProcessor(event_store))


    initial_state = RobotState(0.0, 0.0, 0, CleaningMode.WATER.value)
    state_projector = StateProjector(initial_state)
    command_handler = CommandHandler(event_store)
    
    robot_id = "robot_001"
    

    commands = [
        MoveCommand(100),
        TurnCommand(-90),
        SetStateCommand(CleaningMode.SOAP),
        StartCommand(),
        MoveCommand(50),
        StopCommand()
    ]
    
    for cmd in commands:
        command_handler.handle_command(robot_id, cmd)
    
    
    events = event_store.get_events(robot_id)
    for event in events:
        print(event)

    state = state_projector.project_state(event_store.get_events(robot_id))
    print(state)

main()