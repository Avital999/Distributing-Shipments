from eckity.creators.creator import Creator
from eckity.fitness.simple_fitness import SimpleFitness
import random
from Vector_Part.MsgVector import MsgVector


class MsgVectorCreator(Creator):
    def __init__(self,
                 couriers_num: int,
                 places_num: int,
                 gene_creator=None,
                 events=None):
        if events is None:
            events = ["after_creation"]
        super().__init__(events)
        if gene_creator is None:
            gene_creator = self.default_gene_creator
        self.gene_creator = gene_creator

        self.type = MsgVector
        self.places_num = places_num
        self.couriers_num = couriers_num

    def create_individuals(self, n_individuals, higher_is_better):
        individuals = [MsgVector(couriers_num=self.couriers_num,
                                 places_num=self.places_num,
                                 fitness=SimpleFitness(higher_is_better=higher_is_better))
                       for _ in range(n_individuals)]
        for ind in individuals:
            self.create_vector(ind)
        self.created_individuals = individuals
        return individuals

    def create_vector(self, individual):
        vector = list(range(1, self.places_num+1))
        random.shuffle(vector)
        individual.set_vector(vector)
        print(vector)

    def default_gene_creator(individual, index):
        return individual.get_random_number_in_bounds(index)



