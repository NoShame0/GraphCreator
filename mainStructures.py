# Модуль mainStructures содержит функции создания классических графов
import json

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot


class CreateError(Exception):
    pass


class ListOfInt(list):
    def __init__(self, *args):
        super(ListOfInt, self).__init__(set(sorted(map(int, args[0].split()))))


def check_right(data: list, count_vars: int = 1, *args):

    variables = []

    args = list(args)
    if len(args) > count_vars:
        raise AttributeError

    if len(args) < count_vars:
        args.extend([int] * (count_vars - len(args)))

    for i in range(count_vars):
        try:
            var = args[i](data[i])
        except TypeError:
            raise CreateError
        else:
            variables.append(var)

    for v in variables:
        if isinstance(v, int) and v < 0:
            raise CreateError
        elif isinstance(v, ListOfInt):

            if len(v) == 0:
                raise CreateError
            else:
                for el in v:
                    if el < 1:
                        raise CreateError

    if count_vars == 1:
        return variables[0]

    return variables


def picture_graph_create(graph, num):

    matplotlib.pyplot.clf()
    with open('seetings.json', 'r') as file:
        settings = json.load(file)

    nx.draw(graph, with_labels=num, node_size=settings['node_size'], node_color=settings['node_color'])


def circulant_create(data, num):

    n, elements = check_right(data, 2, int, ListOfInt)
    graph = nx.circulant_graph(n, elements)
    picture_graph_create(graph, num)


def balanced_tree_create(data: list, num):

    a, b = check_right(data, 2)
    graph = nx.balanced_tree(a, b)
    picture_graph_create(graph, num)


def hypercube_create(data: list, num):

    a = check_right(data)
    graph = nx.hypercube_graph(a)
    picture_graph_create(graph, num)


def binomal_tree_create(data, num):

    a = check_right(data)
    graph = nx.binomial_tree(a)
    picture_graph_create(graph, num)


def barbell_graph_create(data, num):

    m1, m2 = check_right(data, 2)
    graph = nx.barbell_graph(m1, m2)
    picture_graph_create(graph, num)


def grid_graph_create(data, num):

    a = check_right(data, 1, ListOfInt)
    graph = nx.grid_graph(a)
    picture_graph_create(graph, num)


def star_graph_create(data, num):

    a = check_right(data)
    graph = nx.star_graph(a)
    picture_graph_create(graph, num)


def wheel_graph_create(data, num):

    a = check_right(data)
    graph = nx.wheel_graph(a)
    picture_graph_create(graph, num)


def ladder_graph_create(data, num):

    a = check_right(data)
    graph = nx.ladder_graph(a)
    picture_graph_create(graph, num)


def turan_graph_create(data, num):

    a, b = check_right(data, 2)
    graph = nx.turan_graph(a, b)
    picture_graph_create(graph, num)


def dorogovtsev_graph_create(data, num):

    a = check_right(data)
    graph = nx.dorogovtsev_goltsev_mendes_graph(a)
    picture_graph_create(graph, num)

