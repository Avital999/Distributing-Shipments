from random import sample, shuffle, uniform, randint
import math
from eckity.genetic_operators.genetic_operator import GeneticOperator
from Vector_Part.MsgVector import MsgVector


class MsgVectorDeliveriesMutation(GeneticOperator):

    def __init__(self, probability=0.5, arity=0, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        for ind in individuals:
            if uniform(0, 1) <= 0.05:
                self.change_places_in_vector(ind)
            elif uniform(0, 1) <= 0.1:
                self.shuffle_random_part_in_vector(ind)
            else:
                self.shuffle_courier_deliveries(ind)
        return individuals


    def change_places_in_vector(self, individual):
        """
        Switch between log(vector's length) pairs of cells
        """
        mutations_num = int(math.log2(individual.length))
        for i in range(mutations_num):
            cells_to_switch = sample(range(0, individual.length), 2)
            individual = individual.switch_two_cells(cells_to_switch[0], cells_to_switch[1])
        return individual

    def shuffle_random_part_in_vector(self, individual):
        """
        Shuffle random part of the vector
        """
        random_part = individual.random_vector_part()
        while len(random_part) == 0:
            random_part = individual.random_vector_part()

        start_index_random = individual.get_vector().index(random_part[0])
        shuffle(random_part)
        individual.replace_vector_part(inserted_part=random_part, start_index=start_index_random)

    def shuffle_courier_deliveries(self, individual):
        """
        Shuffle the deliveries (cells values) of one of the couriers
        """
        random_courier = randint(1, individual.get_couriers_num())
        couriers_indexes = individual.get_couriers_indexes()
        start_ind = 0
        if random_courier > 1:
            start_ind = couriers_indexes[random_courier-2]
        if random_courier == individual.get_couriers_num():
            end_ind = 0
        else:
            end_ind = couriers_indexes[random_courier-1]
        vector_part = individual.get_vector_part(index=start_ind, end_i=end_ind)
        shuffle(vector_part)
        individual.replace_vector_part(inserted_part=vector_part, start_index=start_ind)







