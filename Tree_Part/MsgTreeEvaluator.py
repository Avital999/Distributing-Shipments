from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from BinTree import *
import itertools


def get_routes(res):
    """

    :param res: A list values including numbers or the strings: 'Change courier' or 'Keep going'
    :return: list of courier's routes
    """
    routes = []
    curr_route = []
    for r in res:
        if type(r) == int:
            curr_route.append(r)
        elif type(r) == str:
            if r == 'Change courier':
                routes.append(curr_route)
                curr_route = []
            elif r != 'Keep going':
                raise Exception("Val of node is illegal str: {r}".format(r=r))
        else:
            raise Exception("Val of node is illegal:{r}".format(r=r))
    routes.append(curr_route)
    return routes


def count_delays(del_times, max_time):
    late_deliveries_counter = 0

    for time in del_times:
        if time > max_time:
            late_deliveries_counter += 1

    return late_deliveries_counter


class MsgTreeEvaluator(SimpleIndividualEvaluator):

    def __init__(self, places_matrix, couriers_num: int, delay_for_courier: int):
        super().__init__()
        self.places_matrix = places_matrix
        self.couriers_num = couriers_num
        self.delay_for_courier = delay_for_courier

    def courier_deliveries_time(self, route, courier_ind):
        """

        :param route:  One courier's route as list of integers representing place's indexes.
        courier_ind: This courier is going out as the courier_ind's courier
        :return: list of numbers: times, times[i] represents the time it took to deliver
         the package from place 0 to route[i].
        """
        if len(route) == 0:
            return []


        curr_time = round(self.places_matrix[0][route[0]], 2) + self.delay_for_courier*courier_ind
        times = [curr_time]

        if len(route) > 1:
            for i in range(len(route)-1):
                curr_time = round(curr_time + self.places_matrix[route[i]][route[i+1]], 2)
                times.append(curr_time)

        return times

    def get_all_couriers_deliveries_times(self, routes):
        times = []
        for i in range(len(routes)):
            times.append(self.courier_deliveries_time(route=routes[i],courier_ind=i) )
        del_times = list(itertools.chain(*times))
        return del_times


    def ev_ind2(self, individual:BinTree):
        # Get all the delivery times and sum them
        res = individual.inOrder(individual.root)
        routes = get_routes(res)
        del_times = self.get_all_couriers_deliveries_times(routes)
        return round(sum(del_times), 2)

    def _evaluate_individual(self, individual: BinTree):
        return self.ev_ind2(individual)

