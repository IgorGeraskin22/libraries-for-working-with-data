# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
from decimal import *
from termcolor import cprint
from message import *
import csv



REMAINING_TIME = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']
RPG = "rpg.json"
DUNGEON = "dungeon.csv"
# если изначально не писать число в виде строки - теряется точность!
with open(RPG, "r") as read_file:
    game_file = json.load(read_file)


class Game:
    def __init__(self, in_file):
        self.my_action = None
        self.action = None
        self.color = None
        self.choose_action = None
        self.location = None
        self.count = None
        self.surrender = None
        self.remaining_time = Decimal(REMAINING_TIME)  #
        self.start_time = datetime.timedelta(seconds=0)  # время после старта
        self.experience = 0  # опыт
        self.locations_with_monsters = []  # местоположение и монстры
        self.path_game = in_file
        self.path_after_end = in_file
        self.path_beginning = 'у входа в пещеру'
        self.pattern_time = r'tm\d*.\d*'
        self.pattern_exp = r'_exp\d*'
        self.counting_actions = 0
        self.step = None
        self.indicators = []

    def writing_file(self, *args):
        self.indicators.extend((str(args[0]), str(args[1]), str(args[2])))
        with open(DUNGEON, mode="a", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            if os.stat(DUNGEON).st_size == 0:
                file_writer.writerow(field_names)
            else:
                file_writer.writerow(self.indicators)

            self.indicators.clear()

    def message_output(self, *args):
        self.color = None
        if len(args) == 3 and ATTACK not in args \
                and GO not in args \
                and LOG_OFF not in args:
            print(f'{args[0]}\n', " " * 50, f'{args[1]}\n{args[0]}')

        elif len(args) == 2 and 'Сдаться и выйти из игры' not in args:
            print(f'{args[0]} {args[1]}')

        elif 'Сдаться и выйти из игры' in args:
            cprint(f'{self.surrender} => Сдаться и выйти из игры', color='blue')

        elif len(args) == 1 and 'Показатели' not in args and 'Сдаться и выйти из игры' not in args:

            if ANOTHER_ROAD in args:
                self.color = 'red'

            elif EXIT_VICTORY in args:
                self.color = 'green'

            elif SELECT_ACTION in args:
                self.color = 'blue'

            cprint(args[0], self.color)

        elif 'Показатели' in args:
            cprint((f'Показатели: Опыт {self.experience}, Время {self.start_time}, '
                    f'До наводнения {self.remaining_time} секунд'), color='yellow')

        elif ATTACK in args or GO in args or LOG_OFF in args:
            if ATTACK in args:
                self.action = ATTACK
            elif GO in args:
                self.action = GO
            elif LOG_OFF in args:
                self.action = LOG_OFF

            cprint(f'{self.counting_actions} {self.action} {self.choose_action}', color='blue')

    def start_over(self):
        if self.path_game == 'You are winner':
            self.message_output(NOT_ENOUGH_POINTS, NOT_OPEN_HATCH)  # НЕ ДОСТАТОЧНО БАЛЛОВ, НЕ ОТКРЫТЫЙ ЛЮК

        elif self.remaining_time <= 0:
            self.message_output(TIME_IS_OVER)  # ВРЕМЯ ВЫШЛО, НАВОДНЕНИЕ

        elif self.remaining_time > 0:
            self.message_output(ANOTHER_ROAD)  # ДРУГАЯ ДОРОГА
        self.remaining_time = Decimal(float(REMAINING_TIME))
        self.start_time = datetime.timedelta(seconds=0)
        self.experience = 0
        self.locations_with_monsters = []
        self.path_game = self.path_after_end
        self.path_beginning = PATH_BEGINNING
        self.see()

    def my_location(self):
        self.message_output(INSIDE_YOU_SEE)  # 'Внутри Вы видите:'
        if isinstance(self.path_game, dict):  # проверяем, является ли self.path_game словарем
            for self.location in self.path_game.keys():  # где я нахожусь
                if self.location.startswith('L'):  # Возвращает флаг, указывающий на то, начинается ли строка с указанного префикса L
                    self.locations_with_monsters.append(self.location)
                    self.message_output(ENTRANCE_TO, self.location)  # 'Вход в '
                elif self.location.startwith('M'):
                    self.locations_with_monsters.append(self.location)
                    self.message_output(MONSTER, self.location)  # 'Монстр'

        if isinstance(self.path_game, list):
            for i_see in self.path_game:  # что я вижу
                if isinstance(i_see, dict):
                    self.locations_with_monsters.append(list(i_see.keys())[0])
                    self.message_output(ENTRANCE_TO, list(i_see.keys())[0])
                elif isinstance(i_see, str):
                    self.locations_with_monsters.append(i_see)
                    self.message_output(THE_MONSTER, i_see)

    def see(self, after_monster=0):
        self.message_output('Показатели')
        self.message_output(YOUR_LOCATION, self.path_beginning)
        self.writing_file(self.path_beginning, self.experience, self.start_time)

        if after_monster == 0:
            self.my_location()
            self.game_over(self.action_choice())
        else:
            if len(self.locations_with_monsters) == 0:
                self.start_over()
            else:
                self.message_output(INSIDE_YOU_SEE)
                for choise in self.locations_with_monsters:
                    if str(choise).startswith('L'):
                        self.message_output(choise)
                    elif str(choise).startswith('M'):
                        self.message_output(THE_MONSTER, choise)
                    elif str(choise).startswith('H'):
                        self.message_output('Выход - ', choise)
                self.game_over(step=self.action_choice())

    def action_choice(self):  # выбор действия
        self.counting_actions = 0
        self.message_output(SELECT_ACTION)  # 'Выберите действие:'
        for self.choose_action in self.locations_with_monsters:  # выбор действие
            if str(self.choose_action).startswith('M') or str(self.choose_action).startswith('B'):
                self.my_action = ATTACK

            elif str(self.choose_action).startswith('L'):
                self.my_action = GO

            elif str(self.choose_action).startswith('H'):
                self.my_action = LOG_OFF
            self.counting_actions += 1
            self.message_output(self.my_action, self.counting_actions, self.choose_action)
        self.surrender = self.counting_actions + 1  # сдаюсь
        self.message_output(QUIT_GAME, self.surrender)
        return self.step_selection()

    def step_selection(self):
        while True:
            step_choise = input('')
            if not str(step_choise).isdigit() or int(step_choise) not in range(1, self.counting_actions + 2):
                self.message_output(f'{INCORRECT_NUMBER} {self.counting_actions + 1}')  # Введено неверное число

            elif int(step_choise) == self.surrender:
                self.message_output(DONT_GIVE_UP, LETS_TRY_AGAIN)  # Не сдавайтесь! Выход есть! , Попробуем еще разок?

                step_choise = input('1 - Пробую, 2 - Сдаюсь. Выбрать: ')
                if int(step_choise) == 1:
                    self.remaining_time = Decimal(REMAINING_TIME)
                    self.start_time = datetime.timedelta(seconds=0)
                    self.experience = 0
                    self.locations_with_monsters = []
                    self.path_game = self.path_after_end
                    self.see()
                else:
                    return False
            else:
                break
        return int(step_choise) - 1

    def game_over(self, step):  # ход игры
        if step is False:
            self.message_output(END_GAME)
            return 'End'
        self.location_check(step)

    def location_check(self, step):
        if str(self.locations_with_monsters[step]).startswith('L'):
            get_time = str(re.search(self.pattern_time, self.locations_with_monsters[step]))[42:-2:]
            location_time = float(get_time)
            self.remaining_time -= Decimal(float(location_time))
            self.start_time += datetime.timedelta(seconds=int(location_time))
            if isinstance(self.path_game, dict):
                for choise in self.path_game.keys():
                    if choise == self.locations_with_monsters[step]:
                        self.path_game = self.path_game[choise]
                        self.path_beginning = choise
                        break
            elif isinstance(self.path_game, list):
                count = -1
                for choise in self.path_game:
                    count += 1
                    if isinstance(choise, dict) and list(choise.keys())[0] == self.locations_with_monsters[step]:
                        self.path_game = self.path_game[count][list(choise.keys())[0]]
                        self.path_beginning = self.locations_with_monsters[step]
            self.locations_with_monsters.clear()
            if self.remaining_time < 0:
                self.start_over()
            else:
                self.see(after_monster=0)
        self.monster_check(step)

    def monster_check(self, step):
        if str(self.locations_with_monsters[step]).startswith('M') or str(
                self.locations_with_monsters[step]).startswith('B'):
            monster_time = str(re.search(self.pattern_time, self.path_game[step]))[42:-2:]
            self.remaining_time -= Decimal(float(monster_time))
            exp = str(re.findall(self.pattern_exp, self.locations_with_monsters[step]))[6:-2:]
            self.experience += int(exp)
            self.start_time += datetime.timedelta(seconds=int(monster_time))
            del self.locations_with_monsters[step]
            if self.remaining_time < 0:
                self.start_over()
            else:
                self.see(after_monster=1)
        if str(self.locations_with_monsters[step]).startswith('H'):
            get_time = str(re.search(self.pattern_time, self.locations_with_monsters[step]))[41:-2:]
            location_time = float(get_time)
            self.remaining_time -= Decimal(float(location_time))
            self.path_game = 'You are winner'
            if self.experience >= 280 and self.remaining_time > 0:
                self.message_output(EXIT_VICTORY)
                quit()
            else:
                self.start_over()


game = Game(in_file=game_file)
game.see()

# зачет!
