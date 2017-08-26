# -*- coding: utf-8 -*-

import argparse
import re
import random
import collections

test_string = """
Горец
На пороге класса появились две ученицы: Жданова и Питиримова.
– Здравствуйте, – сказали они.
– До свидания, – холодно ответил Готов.
Девушки замялись.
Трудно передать словами макияж юных особ. Только полотна художников-абстракционистов могут
послужить сравнением.
– Нам можно пройти? – спросила Питиримова и надула большой пузырь из жвачки.
Пузырь лопнул, ошметки жевательной резинки повисли на носу.
– Я же сказал до свидания, – тяжело вздохнул Готов.
Жданова повиляла бедрами, построила Готову глазки и нежно, с придыханием сказала:
– Рудольф Вениаминович, что здесь такого, мы всего на пять минут опоздали?
Готов улыбнулся девушкам и подмигнул:
– Я вас знаю: ты Роза Люксембург, а ты Клара Цеткин.
Несомненно, девочкам можно опоздать даже на десять минут.
А ну, убирайтесь отсюда!!!
Жданова медленно закрыла глаза, так же медленно открыла и тихо проговорила:
- Мы больше так не будем, простите нас, Рудольф Вениаминович… можете нас наказать.
В классе послышались редкие смешки. Жданова с Питиримовой нахально переминались с ноги на ногу.
Готов сел на стул и взглянул на ноги опоздавших.
– Когда я жил в Москве, – сказал он, – мы с друзьями частенько посещали ВДНХ, пиво там пили.
 вот однажды, совершенно случайно забрели
на сельскохозяйственную выставку, где деревенские жители коров демонстрировали.
Подошли к одному стенду и увидели: две девчонки корову пеструю представляют.
Девки эти вылитые вы: на губах по килограмму помады, тени черные,
как будто на глазах фингалы, щеки румяные-румяные.
Про одежду вообще молчу. Не красота спасет мир, а барахолка мир погубит…
И смотрим мы с друзьями, понять не можем: что за животные такие.
Корова вот она стоит – черно-белая, а эти две кто? Не человек точно, определенно какая-то скотина…
Сошлись, с друзьями, во мнении – чернобыльские мутанты.
– Че к чему? – поняла намек Питиримова.
– К тому, девочки, к тому. Будете в большом городе проездом: осторожно.
Поймают, в зоопарк к обезьянам в клетку посадят.
А то и в кунсткамеру отдадут.
Класс смеялся. Мужская часть выкрикивала:
– Обезьяны!
– Коросты!
– Капусты!
– Шлюхи!
Готов вскочил со стула и запротестовал:
– Ребята, это вы зря. Они не шлюхи. Они хуже! Пошли вон отсюда!!! Лохудры!
Выдворив девушек, Готов начал урок:
– Я один из немногих оставшихся. Пилигрим судьбы, шутка провидения.
Кто если не я способен оставить потомкам память о моих странствиях и страданиях.
Учитель медленно провел ладонью по лицу.
– Когда-то нас было много – умерших, но воскресших. Бессмертных.
Правило гласило: «Остаться должен только один».
Я родился в 1564 году, в шотландской деревушке.
Рос в семье кузнеца. Когда мне исполнилось 23 года, женился на прекрасной односельчанке и
прожили мы с ней счастливых 5 лет.
Но однажды ночью эта дрянь пырнула меня, спящего, ножом в живот. Пописала, сучка.
Позже я очнулся: рана затянулась на глазах, жены след простыл, настроение препаршивейшее.
Лежу, лежу… е-мое! Я ж бессмертный оказывается.
Прошел год. Работаю в поле, и вдруг сильнейшее чувство беспокойства обуяло меня.
Гляжу, в мареве появляется фигура мужика, с мечом в руке.
Подходит он ко мне и говорит: «В живых останется только один».
 Я ему: «Тебе чё надо? Курить? Извини не курю, спичками не балуюсь, денег мало, только на хлеб».
Продолжаю картошку копать, а этот мудак, как давай шашкой махать и главное все в голову норовит.
Шибанул я ему, пару раз лопатой по шеям, башка то и отвалилась.
Невесть откуда молнии появились. Током меня шваркнуло, 380, не меньше.
Потом-то мне объяснили, что миссия моя: идти через века и рубить головы всем бессмертным,
а силу их себе забирать.
Как всех порублю, стану самым сильным на земле человеком и смогу принять руководство планетой.
Вот такие пироги… а до сих пор где я только не был, что только ни делал…
Принимал участие во французской буржуазной революции;
служил солдатом в наполеоновской армии;
был лакеем у Александра Сергеевича Пушкина и секундантом у Лермонтова;
нянчил Льва Толстого и, будучи на каторге, валил в Сибири лес.
Анка чапаевская от меня без ума была.
За это по фурмановскому доносу работал землекопом на строительстве Беломорканала.
Да… вот, забыл, у Ленина в должности печника числился.
Со стройки века сбежал в Европу (назад в Шотландию тянуло),
а попал, будь оно неладно, в фашистскую Германию.
В сорок первом, солдатом Вермахта, на Матушку Русь обратно пошел. Взяли в плен.
Что не верблюд, доказать не получилось и до осени 1953 года в Магадане… ой, мама не горюй.
В застойные времена на родину в Шотландию меня никто не пускал,
а с перестройки и до сих пор денег нет.
Одно удивляет меня: за все эти годы, я не встретил ни одного бессмертного.
Тешу себя надеждой, вдруг поубивали они друг дружку…
Не пора ли провозглашать себя императором всея Земли?
– Это вы фильм «Горец» посмотрели? – спросил Вася Кошкин.
– Это я тебя только что из школы отчислил, – ответил Готов.
"""


def possibilities(items):
    posses = {}
    #possess = collections.defaultdict(int)
    for element in items:
        if element not in posses:
            posses[element] = 0
        posses[element] = posses[element] + 1

    for key in posses.keys():
        posses[key] = (posses[key] + 0.0)/len(items)

    return dict(posses)


def choose_key(dict_with_probs):
    # print (dict_with_probs)
    p = random.uniform(0.0, 1.0)
    cur = 0.0
    for key, value in dict_with_probs.items():
        cur = cur + value
        if (cur >= p):
            return key


def is_clear(el):
    pattern1 = re.compile('^[0-9]*$')
    pattern2 = re.compile('^[a-z]*$')
    return pattern1.match(el) or pattern2.match(el)


def divide(el):
    pattern = re.compile('^[0-9a-z]*$')
    if not pattern.match(el) or is_clear(el):
        return [el]

    bound = 0

    while(bound + 1 < len(el) and is_clear(el[0:bound + 1])):
        bound = bound + 1

    return [el[:bound], el[bound:]]


class Analyzer:

    def __init__(self):
        self.strings = []

    def tokenize_string(self, text):
        li = re.split('(\W)', text)
        washed_li = []
        for element in li:

            if len(element) > 0:
                element = divide(element)
                for sub_element in element:
                    washed_li.append(sub_element)

        return washed_li

    def tokenize_normally(self, text):
        li = re.split('\W', text)
        washed_li = []
        for element in li:
            if len(element) > 0 and element != ' ':
                washed_li.append(element)

        return washed_li

    def tokenize_string_normally(self, text):
        li = re.split('(\W)', text)
        washed_li = []
        for element in li:
            if (
                len(element) > 0 and
                element != ' ' and
                '-' not in element and
                '—' not in element and
                '»' not in element and
                '«' not in element
            ):
                washed_li.append(element)

        return washed_li

    def add_text(self, text, func):
        self.strings.append(func(text))

    def markowize(self, depth):
        self.map_tokens = {}

        for string in self.strings:

            token_line = []
            for token in string:

                token_line.append(token)

                last = token_line[len(token_line) - 1]
                line = tuple(token_line[:-1])

                for d in range(0, depth + 1):
                    if len(line) < d:
                        continue
                    markow_line = tuple(line[len(line) - d:])

                    if markow_line not in self.map_tokens.keys():
                        self.map_tokens[markow_line] = []
                    self.map_tokens[markow_line].append(last)

                if (len(token_line) == depth + 1):
                    token_line = token_line[1:]

        self.map_tokens_possibilities = {}

        for key, value in self.map_tokens.items():
            self.map_tokens_possibilities[key] = possibilities(value)

        # print (self.map_tokens_possibilities)
        return self.map_tokens_possibilities

    def get_next(self, chain):

        if chain in self.map_tokens_possibilities:
            possible_moves = self.map_tokens_possibilities[chain]
        else:
            return '.'

        key = choose_key(possible_moves)
        return key


def tokenize(args, strings):
    text = ''
    for string in strings:
        text = text + string
    tokens = analyzer.tokenize_string(text)
    for token in tokens:
        print (token)


def set_posses(args, strings):

    for string in strings:
        analyzer.add_text(string, func=analyzer.tokenize_normally)

    map_tokens_possibilities = analyzer.markowize(args.depth)
    keys_list = list(map_tokens_possibilities.keys())
    keys_list.sort()
    for key in keys_list:
            print (' '.join(list(key)))

            destines = list(map_tokens_possibilities[key].keys())
            destines.sort()
            for dest in destines:
                print (' ', dest + ':',  '%.2f' % map_tokens_possibilities[key][dest])


def generate(args, strings):

    for string in strings:
        analyzer.add_text(string, analyzer.tokenize_string_normally)

    depth = args.depth
    size = args.size

    analyzer.markowize(depth)

    result = []

    chain = tuple('')

    while len(result) < size:
        token = analyzer.get_next(chain)
        if chain == tuple(''):
            if not token[0].isupper():
                continue

        result.append(token)

        if (token == ''):
            chain = tuple('')
        else:
            chain = chain[1:]
            chain_list = list(chain)
            chain_list.append(token)
            chain = tuple(chain_list)

    txt = ''
    counter = 0

    for element in result:
        txt = txt + element + ' '

    txt = txt.replace(' ,', ',')
    txt = txt.replace(' .', '.')
    txt = txt.replace(' …', '…')
    txt = txt.replace(' ?', '?')
    txt = txt.replace(' !', '!')

    print (txt)


class Unit_args():
    size = 100
    depth = 100


def unit_test(args, strings):

    strings = test_string.split('\n')
    args = Unit_args()

    text = ''
    for string in strings[:5]:
        text = text + string.strip() + ' '
    print ('test tokenize function!')
    tokenize(args, text)

    print ('test probabilities function!')
    set_posses(args, strings[:5])

    print ('test generate function!')
    generate(args, strings)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_tokenize = subparsers.add_parser('tokenize', help='to crop an image')
    parser_tokenize.set_defaults(func=tokenize)

    parser_probs = subparsers.add_parser('probabilities', help='show probabilities')
    parser_probs.add_argument('--depth', type=int, default=1)
    parser_probs.set_defaults(func=set_posses)

    parser_generate = subparsers.add_parser('generate', help='generate sequence')
    parser_generate.add_argument('--depth', type=int, default=1)
    parser_generate.add_argument('--size', type=int, default=10)
    parser_generate.set_defaults(func=generate)

    parser_unit_test = subparsers.add_parser('test', help='for unit test')
    parser_unit_test.set_defaults(func=unit_test)

    fin = open('input.txt')

    arg_line = fin.readline()
    args = parser.parse_args(arg_line.split())

    content = ''

    strings = []

    while True:
        text = fin.readline().strip()
        if len(text) > 0:
            content = content + text
            strings.append(text)
        else:
            break

    args.func(args, strings)


analyzer = Analyzer()

if __name__ == '__main__':
    main()
