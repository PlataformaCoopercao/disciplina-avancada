import csv
import numpy
import pandas as pd
import random
import time
import timeit
from math import sqrt


class Node:

    def __init__(self, latitude, longitude):
        self.latitude = int(latitude)
        self.longitude = int(longitude)
        # self.time_limit = time_limit

    def __repr__(self):
        return ' '.join([str(self.latitude), str(self.longitude)])

    def get_distance(self, destination_node):
        distance = sqrt((self.latitude - destination_node.latitude)**2 +
                        (self.longitude - destination_node.longitude)**2)
        return distance


def calculate_distance(node_graph):
    distance = 0
    for index, node in enumerate(node_graph):
        if node != node_graph[-1]:
            distance += node.get_distance(node_graph[index+1])
    return distance


def random_hillclimbing(route, opt=1, testing=False):
    # import ipdb; ipdb.set_trace()
    if opt <= 10:
        new_route = []
        old_route = route.copy()
        for node in route:
            new_node = random.choice(old_route)
            new_route.append(new_node)
            # import ipdb; ipdb.set_trace()
            old_route.remove(new_node)
        if calculate_distance(new_route) > calculate_distance(old_route):
            return new_route
        return random_hillclimbing(route, opt=opt+1)
    return route


def random_hillclimbing_opt(route, opt_limit, opt=1, results=[]):
    # import ipdb; ipdb.set_trace()
    if opt <= opt_limit:
        new_route = []
        old_route = route.copy()

        for node in route:
            new_node = random.choice(old_route)
            new_route.append(new_node)
            old_route.remove(new_node)

        results.append(new_route)
        return random_hillclimbing_opt(new_route, opt_limit, opt=opt+1, results=results)

    return results


def random_hillclimbing_final(route, opt_limit, opt=1):
    # import ipdb; ipdb.set_trace()
    if opt <= opt_limit:
        new_route = []
        old_route = route.copy()

        for node in route:
            new_node = random.choice(old_route)
            new_route.append(new_node)
            old_route.remove(new_node)

        if calculate_distance(new_route) < calculate_distance(route):
            return random_hillclimbing_final(new_route, opt_limit, opt=opt+1)
        else:
            return random_hillclimbing_final(route, opt_limit, opt=opt+1)
    return route


def test_opts(opt_range, test_range):
    with open('results.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        spamwriter.writerow(['Original'] + list(['{}_opt'.format(x)
                                                 for x in range(1,
                                                                opt_range+1)]))
        for x in range(test_range):
            route = []
            for x in range(4):
                route.append(Node(random.randrange(50),
                                  random.randrange(100),
                                  10))
            print(list(route))
            # import ipdb; ipdb.set_trace()
            original = calculate_distance(route)
            # glutonous = calculate_distance(random_hillclimbing(route))
            optimized = random_hillclimbing_opt(route, opt_range, results=[])
            # se não resetar o valor de results ele acumula (wtf)
            opt = [calculate_distance(result) for result in optimized]
            spamwriter.writerow([original] + list(opt))
            # time.sleep(1)


def test_final(opt_limit, test_range):
    with open('results_opt{}.csv'.format(opt_limit), 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        spamwriter.writerow(
            ['original', '{}_opt'.format(opt_limit), 'improvement'])
        for x in range(test_range):
            route = []
            for x in range(4):
                route.append(Node(random.randrange(50),
                                  random.randrange(100),
                                  10))
            # print(list(route))
            # import ipdb; ipdb.set_trace()
            original = calculate_distance(route)
            # glutonous = calculate_distance(random_hillclimbing(route))
            # import ipdb; ipdb.set_trace()
            optimized = calculate_distance(random_hillclimbing_final(route=route, opt_limit=opt_limit))
            improvement = (original - optimized)*100/original
            # se não resetar o valor de results ele acumula (wtf)
            spamwriter.writerow([original, optimized, improvement])

# route = []
# for x in range(4):
#     route.append(Node(random.randrange(5), random.randrange(10), 10))
# print(list(route))
# print(calculate_distance(route))
# print('*'*30)
# print(calculate_distance(random_hillclimbing(route)))
# print('*'*30)
# print(calculate_distance(random_hillclimbing_opt(route, opt_limit=3)))
# print(timeit.timeit("calculate_distance(random_hillclimbing(route, opt=3))", globals=globals()))
# print(timeit.timeit("calculate_distance(random_hillclimbing_opt(route, opt_limit=3))", globals=globals()))


def analyze_data_opts():
    test(10, 10000)

    dataframe = pd.read_csv('results.csv')

    columns = dataframe.columns
    diffs = [dataframe['Original'] - dataframe[column] for column in columns[1::]]
    diff_means = [numpy.mean(diff) for diff in diffs]
    maxes = [max(dataframe[column]) for column in dataframe.columns]
    mins = [min(dataframe[column]) for column in dataframe.columns]
    import ipdb; ipdb.set_trace()


def analyze_data_final(opt_limit, execution_count):
    test_final(opt_limit, execution_count)
    dataframe = pd.read_csv('results_opt{}.csv'.format(opt_limit))

    columns = dataframe.columns
    diffs = [dataframe['original'] - dataframe['{}_opt'.format(opt_limit)]]
    diff_means = [numpy.mean(diff) for diff in diffs]
    improvement_mean = numpy.mean(dataframe['improvement'])
    max_improvement = float(max(dataframe['improvement']))
    # min_improvement = float(min(dataframe['improvement']))
    zeros = pd.value_counts(dataframe['improvement'].values, sort=False)[0]
    zero_percentage = 100 - ((execution_count - zeros)*100)/execution_count

    with open('data_{}.csv'.format(opt_limit), 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        spamwriter.writerow(['improvement_mean', 'max', 'zero_percentage'])
        spamwriter.writerow(
            [improvement_mean, max_improvement, zero_percentage])


# route = []
# for x in range(4):
#     route.append(Node(random.randrange(50),
#                       random.randrange(100),
#                       10))
# print(route)
# for opt_limit in range(1, 51):
#     # analyze_data_final(opt_limit, 10000)
#     with open('data_{}.csv'.format(opt_limit), 'a') as f:

#         time = timeit.timeit(
#             "random_hillclimbing_final(route, opt_limit={})".format(opt_limit), globals=globals(), number=10000)
#         f.write(str(time))
