from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from Vector_Part.MsgVector import MsgVector
from random import shuffle


class MsgVectorKPointsCrossover(VectorKPointsCrossover):
    def apply(self, individuals):
        individuals = super().apply(individuals)
        for ind in individuals:
            self.correct_ind(ind)
        self.applied_individuals = individuals
        return individuals

    def correct_ind(self, individual:MsgVector):
        """

        :param individual: MsgVector
        Get a vector after crossover. Check each value if it appears more than once and replace it with
        a value in the range that don't appear.
        :return: Vector in the same length with all the values from 1 to vector's length
        """
        values_counter = {}

        for cell_index in range(individual.length):
            val = individual.cell_value(cell_index)
            if val in values_counter.keys():
                values_counter[val] += 1
            else:
                values_counter[val] = 1

        free_values = []
        for num in range(1, individual.length+1):
            if num not in values_counter.keys():
                free_values.append(num)
        shuffle(free_values)

        for cell_index in range(individual.length):
            val = individual.cell_value(cell_index)
            # Switch value that appeared more than once in the vector with value that doesn't appar
            if val in values_counter.keys() and values_counter[val] > 1:
                free_val = free_values.pop()
                individual.set_cell_value(index=cell_index, value=free_val)
                values_counter[val] -= 1
                values_counter[free_val] = 1






