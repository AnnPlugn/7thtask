import os
def uni(strings : str, *func):
    os.system('cls||clear')
    print(strings)
    command = input('Команда: ')
    if command.isdigit() and int(command) - 1 < len(func) and int(command) - 1 >= 0:
        func[int(command) - 1]()
    elif command.isdigit() and int(command) == len(func) + 1:
        return False
    else:
        print('Такой команды нет...')
    input('\nEnter для продолжения\n')
    return True