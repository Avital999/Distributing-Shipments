import itertools
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from Vector_Part.MsgVector import MsgVector


class MsgVectorEvaluator(SimpleIndividualEvaluator):
    def __init__(self, places_matrix, max_distance: int, couriers_num: int, delay_for_courier: int):
        super().__init__()
        self.places_matrix = places_matrix
        self.max_distance = max_distance
        self.couriers_num = couriers_num
        self.delay_for_courier = delay_for_courier

    def courier_deliveries_time(self, route, courier_ind: int):
        # Case 1: courier doesn't need to deliver packages
        if len(route) == 0:
            return []

        # Case 2: courier has packages to deliver
        curr_time = round(self.places_matrix[0][route[0]], 2) + self.delay_for_courier*courier_ind
        times = [curr_time]

        for i in range(len(route)-1):
            curr_time = round(curr_time + self.places_matrix[route[i]][route[i+1]], 2)
            times.append(curr_time)

        return times

    def get_all_times(self, routes):
        times = []
        for i in range(len(routes)):
            times.append(self.courier_deliveries_time(route=routes[i], courier_ind=i))
        return list(itertools.chain(*times))

    def get_routes(self, individual: MsgVector):
        inds = [0] + individual.get_couriers_indexes() + [individual.length]
        routes = []

        if len(inds) <= 2:
            raise Exception("No couriers!")

        for j in range(len(inds) - 1):
            routes.append(individual.get_vector_part(index=inds[j], end_i=inds[j + 1]))

        return routes

    def get_route_dist(self, route):
        if len(route) == 0:
            return 0
        sum = self.places_matrix[0][route[0]]
        for i in range(len(route)-1):
            sum = sum + self.places_matrix[route[i]][route[i+1]]
        sum = sum + self.places_matrix[-1][0]
        return sum


    def _evaluate_individual(self, individual: MsgVector):
        routes = self.get_routes(individual=individual)
        del_times = self.get_all_times(routes)
        total_time = sum(del_times)
        return total_time

