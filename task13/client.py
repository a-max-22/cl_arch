from  robot_commands import *

def main():
    # Создаем исполнителя
    handler = CommandHandler()
    
    # Добавляем команды
    handler.exec_command(MoveCommand(100))
    handler.exec_command(TurnCommand(-90))
    handler.exec_command(SetStateCommand(CleaningMode.SOAP))
    handler.exec_command(StartCommand())
    handler.exec_command(MoveCommand(50))
    handler.exec_command(StopCommand())
    
    # Выполняем все команды
    final_state, logs = handler.get_state()
    
    # Выводим результаты
    print("Final state:", final_state)
    print("Command log:", logs)

main()