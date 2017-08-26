from requests import get
import unicodedata
from bs4 import BeautifulSoup
from urllib import parse
import html.parser
import lxml
import re
import urllib
import collections
import pickle
import matplotlib.pyplot as plt

BASE_TITLE = 'http://www.machinelearning.ru/wiki/index.php?title='
BASE = 'http://www.machinelearning.ru'

PATTERN_REF = re.compile('/wiki/index.*')
PATTERN_CATEGORY = re.compile('Категория.*')


def is_ref(url):
    if PATTERN_REF.match(url):
        return True
    else:
        return False


def is_article(url):
    if ':' in parse.unquote(url):
        return False

    if '&' in parse.unquote(url):
        return False

    return True


def is_category(url):
    if PATTERN_CATEGORY.match(parse.unquote(url)):
        return True
    else:
        return False


def clear(url):
    return url.replace('/wiki/index.php?title=', '')


def only_unique_articles(ref_list):
    articles = []
    visited_articles = collections.defaultdict(bool)
    for ref in ref_list:
        if is_article(ref) and not visited_articles[ref]:
            visited_articles[ref] = True
            articles.append(parse.unquote(ref))
    return articles


def get_refs(address):
    get_address = BASE_TITLE + address
    page = get(get_address)

    soup = BeautifulSoup(page.text, 'lxml')
    body_cont = soup.find('div', id='bodyContent')

    if body_cont is None:
        return []

    refs = []
    for href in body_cont.findAll('a'):
        if 'href' in href.attrs:
            ref = href['href']
            if is_ref(ref):
                refs.append(clear(ref))
    return refs


def collect_articles(start_page, filename):
    articles = []

    with open(filename, 'w') as output:
        visited_pages = collections.defaultdict(bool)
        page_queue = [start_page]

        for page in page_queue:
            if visited_pages[page]:
                continue
            print('page=', parse.unquote(page))
            visited_pages[page] = True

            page_refs = get_refs(page)

            for ref in page_refs:
                # print ('unquote ref=', parse.unquote(ref))
                if not is_article(ref):
                    if is_category(ref):
                        page_queue.append(ref)
                else:
                    output.write(parse.unquote(ref + "\n"))
                    articles.append(ref)


def clear_graph(graph):
    for ref in graph.keys():
        neighbours_to_pop = []
        for neighbour in graph[ref]:
            if neighbour not in graph.keys():
                neighbours_to_pop.append(neighbour)
        for neighbour in neighbours_to_pop:
            graph[ref].remove(neighbour)


def create_graph(filename):
    with open(filename, 'r') as infile:
        visited_pages = collections.defaultdict(bool)
        graph = collections.defaultdict(list)
        real = 0
        pred = 0
        for ref in infile:
            pred = pred + 1
            if (visited_pages[ref]):
                continue
            real = real + 1
            visited_pages[ref] = True
            ref = ref.strip()

            if (real % 5 == 0):
                print(real, pred, 'ref=', ref)
            graph[ref] = only_unique_articles(get_refs(parse.quote(ref)))
            print(graph[ref])
            if (real % 5 == 0):
                print(len(graph[ref]))

        return graph


def create_reversed_graph(graph):

    reversed_graph = collections.defaultdict(list)

    for vertex in graph:
        reversed_graph[vertex]
        for neighbor in graph[vertex]:
            reversed_graph[neighbor].append(vertex)

    return reversed_graph


def save_graph(graph, filename):
    with open(filename, 'wb') as dest:
        pickle.dump(graph, dest)


def load_graph(filename):
    with open(filename, 'rb') as dest:
        graph = pickle.load(dest)
    return graph


def page_ranks(graph, save_rank=0.15, friend_rank=0.8, free_rank=0.05, iterations=100):

    ranks = collections.defaultdict(int)
    for page in graph.keys():
        ranks[page] = 1

    for i in range(iterations):
        next_ranks = ranks

        for page in graph.keys():
            next_ranks[page] = save_rank * ranks[page] + free_rank

        for page in graph.keys():
            if len(graph[page]) == 0:
                continue
            share_rank = friend_rank * ranks[page] / len(graph[page])
            for neighbour in graph[page]:
                next_ranks[neighbour] = next_ranks[neighbour] + share_rank
        ranks = next_ranks

        avg_rank = 0.0
        for rank in ranks.values():
            avg_rank = avg_rank + rank

        avg_rank = avg_rank / len(graph)

        for page in graph.keys():
            ranks[page] = ranks[page] / avg_rank

    return ranks


def graph_analytics(graph, filename, calc_ranks=False):
    with open(filename, 'w') as output:
        print('size of this graph is = ', len(graph))

        graph_counts = []
        graph_lens = []

        for vertex in graph.keys():
            graph_counts.append([len(graph[vertex]), parse.unquote(vertex)])
            graph_lens.append(len(graph[vertex]))

        graph_counts.sort()
        graph_lens.sort()

        for el in graph_counts:
            # print (el)
            output.write(str(el[0]) + " " + el[1] + '\n')

        if calc_ranks:
            with open('page_rank_' + filename, 'w') as pr_output:
                ranks = page_ranks(graph)
                graph_ranks = []
                for vertex in graph.keys():
                    graph_ranks.append([ranks[vertex], parse.unquote(vertex)])
                graph_ranks.sort()
                ranks = []
                for el in graph_ranks:
                    # print(el)
                    ranks.append(el[0])
                    pr_output.write(str(el[0]) + " " + el[1] + '\n')

                axis = []

                for i in range(len(graph)):
                    axis.append(i)

                plt.figure(figsize=(20, 12))
                plt.xlim(0, len(axis))
                plt.ylim(0, ranks[-1])
                plt.plot(axis, ranks)
                plt.show()

        sum = 0.0
        for lenc in graph_lens:
            sum = sum + lenc
        print('average degree=', sum / len(graph_lens))

        axis = []

        for i in range(len(graph)):
            axis.append(i)

        plt.figure(figsize=(20, 12))
        plt.xlim(0, len(axis))
        plt.ylim(0, graph_lens[-1])
        plt.plot(axis, graph_lens)
        plt.show()


def main():

    # Запускаем поиск всех статей из корня сайта, сохраняем найденный урлы статей в файл output.txt
    collect_articles(parse.quote('Категория:Статьи'), 'output.txt')

    # Выгружаем все статьи и строим по ним граф вида статья -> список ссылок из нее
    graph = create_graph('output.txt')

    # Сохраняем граф
    save_graph(graph, 'middle.txt')

    # Выгружаем граф (сделано на тот случай, если мы закомментили предыдущие строки кода)
    graph = load_graph('middle.txt')

    # Приводим граф к нормальному виду -- удаляем ссылки,
    # которые ведут в вершины, находящиеся вне графа
    clear_graph(graph)

    # сохраняем почищенный граф
    save_graph(graph, 'graph.txt')

    # развернутый граф ссылок, которые приходят в статью, а не выходят
    reversed_graph = create_reversed_graph(graph)

    # сохраняем развернутый граф
    save_graph(reversed_graph, 'reversed_graph.txt')

    # Опять выгружаем граф (как видим, этот скрипт многофазовый)
    graph = load_graph('graph.txt')

    # Выгружаем развернутый граф
    reversed_graph = load_graph('reversed_graph.txt')

    # Анализ графа с подсчетом ранков и графиком распределения по числу исходящих ссылок
    graph_analytics(graph, calc_ranks=True, filename='graph_analytics.txt')

    # Анализ развернутого графа с графиком распределения по числу входящих ссылок
    graph_analytics(reversed_graph, filename='reversed_graph_analytics.txt')

if __name__ == '__main__':
    main()
