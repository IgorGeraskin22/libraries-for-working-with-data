Библиотеки для работы с данными
# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
********************************************************************************************
Libraries for working with data.
  # The dungeon was dug by lizard-like monsters next to an anomalous river that constantly overflows its banks.
# Because of this, the dungeon is regularly flooded, the monsters survive, but not the heroes who dared to go down to them in search of
# adventures.
# Sensing impunity, the lizards began to raid the nearest villages. Not enough to protect all the villages
# soldiers and you, as a hero known in these parts, were hired to save them.
#
# The dungeon map is a json file called rpg.json. Each location in the maze is described by an object,
# which contains a single key with a name corresponding to the format "Location_<N>_tm<T>",
# where N is the location number (integer) and T (real number) is the time,
# which is needed to go to this location. For example, if the player enters the location "Location_8_tm30000",
# then it spends 30000 seconds on it.
# This key contains a list that contains lines with descriptions of monsters and other locations.
# Description of the monster is a string in the format "Mob_exp<K>_tm<M>", where K (integer) is the amount of experience,
# that the player gets by destroying this monster, and M (real number) is the time,
# that the player will spend to destroy this monster.
# For example, destroying the monster "Boss_exp10_tm20", the player will spend 20 seconds and get 10 experience points.
# It is guaranteed that at the beginning of the path there will be two locations and one monster
# (i.e. the root json object contains a list containing two json objects, one monster and nothing else).
#
# The player is given 123456.0987654321 seconds to complete the game.
# The goal of the game is to find a way out ("Hatch") in the allotted time
#
# As you go deeper into the dungeon, it starts to flood, so
# each location can only be entered once,
# and you can't get out of it (that is, you can only move forward).
#
# To open the hatch ("Hatch") and get out through it to the surface, you need to have at least 280 experience points.
# If time ends before opening the hatch - the hero suffocates and dies, resurrecting before entering the dungeon,
# ready for the next try (game restarts).
#
# It is guaranteed that there is only one path to find, so be careful!
# If the decimal library is used incorrectly, the person playing with your script runs the risk of never finding the path.
#
# Also, every time the player moves, your script should remember the following information:
# - current location
# - current amount of experience
# - current date and time (for this use the datetime library)
# After the successful or unsuccessful completion of the game, you need to record
# all collected information in csv file dungeon.csv.
# Column names for csv file: current_location, current_experience, current_date
#
#
# Example of interaction with the player:
#
# You are in Location_0_tm0
# You have 0 experience and 123456.0987654321 seconds left before the flood
# Elapsed time: 00:00
#
# Inside you see:
# - Entrance to the location: Location_1_tm1040
# - Entrance to the location: Location_2_tm123456
# Select an action:
# 1. Attack the monster
# 2. Go to another location
# 3. Give up and quit the game
#
# You have chosen to go to location Location_2_tm1234567890
#
# You are in Location_2_tm1234567890
# You have 0 experience and 0.0987654321 seconds left before the flood
# Elapsed time: 20:00
#
# Inside you see:
# - Monster Mob_exp10_tm10
# - Entrance to the location: Location_3_tm55500
# - Entrance to the location: Location_4_tm66600
# Select an action:
# 1. Attack the monster
# 2. Go to another location
# 3. Give up and quit the game
#
# You chose to fight the monster
#
# You are in Location_2_tm0
# You have 10 experience and -9.9012345679 seconds left before the flood
#
# You didn't have time to open the hatch!!! FLOOD!!! Alarm!
#
# Your eyes are getting dark... goodbye, princess...
# But what is it?! You resurrected at the entrance to the cave... No wonder your mother gave you a charm :)
# Well, this time you will succeed! Tremble, monsters!
# You carefully enter the cave... (the text of death/resurrection can be your own;)
#
# You are in Location_0_tm0
# You have 0 experience and 123456.0987654321 seconds left before the flood
# It's already past 0:00:00
# Inside you see:
# ...
# ...
#
# etc...
