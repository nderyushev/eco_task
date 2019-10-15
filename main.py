import json
import csv
import os


class CommandsUpdater(object):

    class Rows:
        # Индексы для csv, чтоб без хардкода
        MODULE = 0
        NAME = 1
        FUNCTION = 2

    def __init__(self, data_path, users_path):
        # Указываем пути к json файлу и к файлам users
        self.data_path = data_path
        self.users_path = users_path

    @staticmethod
    def write_data(path, data):
        # Записывает json в файл
        with open(path, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @staticmethod
    def read_user_data(path):
        # Читает csv файл юзера и возвращает его команды в виде списка кортежей
        with open(path) as file:
            reader = csv.reader(file, delimiter=';')
            user_data_rows = list(map(lambda command: tuple(command), reader))
        return user_data_rows

    def get_all_commands_with_users(self):
        # Вспомогательный метод, формирует dict с парами команда-список пользователей
        all_commands = {}
        
        for user_file in os.listdir(self.users_path):
            user_abs_path = f'{self.users_path}/{user_file}'
            user_title = user_file.split('.')[0]
            user_commands = self.read_user_data(user_abs_path)

            for command in user_commands:
                if command not in all_commands:
                    all_commands[command] = [user_title]
                else:
                    all_commands[command].append(user_title)
        return all_commands

    def collect_data(self):
        # Главный метод, обновляет данные json
        all_commands = self.get_all_commands_with_users()
        data = {'commands': []}

        for command, users in all_commands.items():
            data_command = {
                'function': command[self.Rows.FUNCTION],
                'name': command[self.Rows.NAME],
                'module': command[self.Rows.MODULE],
                'param': [
                    {'user': user_title} for user_title in users
                ]
            }
            data['commands'].append(data_command)
        
        self.write_data(self.data_path, data)


if __name__ == "__main__":
    updater = CommandsUpdater('data/data.json', 'data/users')
    updater.collect_data()
    print('Done!')