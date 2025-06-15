from FileWork import read_counter


api_id = -
api_hash = -


# Чат
AVAILABLE_CHATS = {
    1: ("Основной чат", -1002514980200),
    2: ("Тестовый чат", -1002676476786)
}


#Булевые переменные
AVTO = False
active_task = None

#Простые переменные
fileN = 'LOG.txt'


#Получение переменных
rand = read_counter()

#Analyzers
min_pattern_len = 3
max_pattern_len = 7
min_count = 3
min_probabi1lity = 0.6

ColorLenLog = 3000
RangeLenLog = 3000
ParityLenLog = 3000
NumberLenLog = 5000
NumberLenPattern = 2
ComboLenLog = 3000
ReactiveLenLog = 2000
AiWindow = 10

DECISION_MODE = 'большинство'

default_triggers = {
    "color": [
        ['К', 'К', 'К'],
        ['Ч', 'Ч', 'Ч'],
        ['К', 'К', 'К', 'К'],
        ['Ч', 'Ч', 'Ч', 'Ч'],
        ['К', 'Ч', 'К', 'Ч'],  # цветовой маятник
        ['Ч', 'К', 'Ч', 'К']   # обратный маятник
    ],
    "parity": [
        ['even', 'even', 'even'],
        ['odd', 'odd', 'odd'],
        ['even', 'even', 'even', 'even'],
        ['odd', 'odd', 'odd', 'odd'],
        ['even', 'odd', 'even', 'odd'],  # маятник
        ['odd', 'even', 'odd', 'even']   # маятник обратный
    ],
    "range": [
        ['HIGH', 'HIGH', 'HIGH'],
        ['LOW', 'LOW', 'LOW'],
        ['MID', 'MID', 'MID'],
        ['LOW', 'LOW', 'HIGH'],          # скачок вверх
        ['HIGH', 'HIGH', 'LOW'],         # скачок вниз
        ['MID', 'HIGH', 'MID'],          # волна через верх
        ['LOW', 'MID', 'LOW'],           # волна снизу
        ['HIGH', 'MID', 'HIGH']          # волна сверху
    ]
}
