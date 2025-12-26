from client_cleaner_api import ClientCleanerApi, ClientCleanerCommandResult 

# в данном случае, ClientCleanerApi не хранит состояние, 
# он получает на вход некий непрозрачный объект типа  ClientCleanerCommandResult,
# а если он не задан - инициирует результат команды как пустой
# ClientCleanerCommandResult. 
# ClientCleanerCommandResult содержит методы, которые позволяют получить характеристики 
# робота в данной точке выполнения.  
cleaner_api = ClientCleanerApi()

cleanerCommandResult = cleaner_api.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ))

cleaner_info = cleanerCommandResult.get_cleaner_info()

print (cleaner_info.get_x(), 
    cleaner_info.get_y(), 
    cleaner_info.get_angle(), 
    cleaner_info.get_state())

# сохранение/сериализация результата выполнение команды
# в том или ином хранилище, в зависимости от предпочитаемой логики
savedCleanerInfo = cleanerCommandResult.save()


# восстановление результата выполнения команды из хранилища
restoredCleanerCommandResult = ClientCleanerCommandResult(savedCleanerInfo)

# продолжене выполнения из заданной точки
cleanerCommandResultAfterRestore = cleaner_api.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ), restoredCleanerCommandResult)