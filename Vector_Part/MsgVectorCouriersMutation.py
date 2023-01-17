from random import randint, uniform
from eckity.genetic_operators.genetic_operator import GeneticOperator
from Vector_Part.MsgVector import MsgVector

class MsgVectorCouriersMutation(GeneticOperator):
    def __init__(self, probability=0.5, arity=0, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):

        # case 1: more couriers than packages, cannot mutate
        if individuals[0].length <= individuals[0].couriers_num:
            return individuals

        # case 2: more packages than couriers
        for ind in individuals:
                self.change_couriers_indexes(ind)
        return individuals

    def change_couriers_indexes(self, individual):
        current_indexes = individual.get_couriers_indexes()
        couriers_num = individual.couriers_num

        rand_index = randint(1, individual.length)
        while rand_index in current_indexes:
            rand_index = randint(1, individual.length)

        rand_courier_index = randint(0, couriers_num-2)

        current_indexes[rand_courier_index] = rand_index
        current_indexes.sort()
        individual.update_courier_indexes(current_indexes)



