from collections import defaultdict
import random


def strongly_connect(input_list):
    build_list = defaultdict(list)
    n = len(input_list)
    extend = int(n * (n - 2) * EXTRA_STRONG_PATHS)
    for i in range(n + random.randint(0, extend)):
        if i < n:
            build_list[i].append((i + 1) % n)
        else:
            k = random.choice([z for z in build_list if len(build_list[z]) < (n - 1)])
            build_list[k].append(random.choice([z for z in build_list if z != k and z not in build_list[k]]))

    result_list = dict()
    for i in range(n):
        result_list[input_list[i]] = list([input_list[j] for j in build_list.pop(i)])

    return result_list


def connect(graph1, graph2):
    try:
        fr = random.choice(list(graph1.keys()))
        to = random.choice(list([x for x in graph2.keys() if x not in graph1[fr]]))
        graph1[fr].append(to)
    except IndexError:
        pass


def weak_connect_graph(clustered_graph):
    rnd = lambda a, b: min(a, b) + random.randint(0, int(a * b * NUMBER_OF_WEAK_PATHS))
    random.shuffle(clustered_graph)
    result_graph = dict()
    for i in range(len(clustered_graph)):
        for j in clustered_graph[i + 1:]:
            for _ in range(rnd(len(clustered_graph[i]), len(j))):
                connect(clustered_graph[i], j)
        result_graph.update(clustered_graph[i])

    return result_graph


def generate_graph(size, number_of_clusters, minimal_size):
    """
    Generate a graph with size 'nodes' where
    number_of_clusters sub-graphs are strongly-connected

    """
    base_list = list(range(size))
    result_list = []
    random.shuffle(base_list)
    for i in range(number_of_clusters - 1):
        size = random.randint(minimal_size, len(base_list) - (number_of_clusters - i - 1) * minimal_size)
        cluster = []
        for n in range(size):
            actual = random.choice(base_list)
            base_list.remove(actual)
            cluster.append(actual)
        result_list.append(strongly_connect(cluster))
    result_list.append(strongly_connect(base_list))

    while len(result_list) < 5:
        result_list.append([])

    print(sorted([len(i) for i in result_list], reverse=True)[:5])

    return weak_connect_graph(result_list)


def make_kosaraju(filename, number_of_nodes, number_of_clusters, smallest_degree):
    """
    create a graph with number_of_clusters strongly-connected nodes.
    clusters are weakly connected.
    The smallest_degree is the size of the smallest cluster

    data is send to 'filename'

    message is the result you obtain for the 5 greatest clusters of the graph
    """

    file = open(filename, 'w')
    tmp = generate_graph(number_of_nodes, number_of_clusters, smallest_degree)
    for i in tmp:
        for j in tmp[i]:
            file.write("{} {}\n".format(i, j))


"""
EXTRA_STRONG_PATHS = .1 (0 .. 1), Add extra paths in strongly-connected cluster
NUMBER_OF_WEAK_PATHS = .3 (0 .. 1), path between weak-connections
0:  minimal amount
1:  maximal amount possible
"""
EXTRA_STRONG_PATHS = .4
NUMBER_OF_WEAK_PATHS = .5

"""
Example:
    Generate a graph with 20 nodes, containing 6 strongly connected clusters
    The smallest size of the cluster is 1 node
    Send all data to scc.txt
"""

make_kosaraju('scc.txt', 20, 2, 1)
