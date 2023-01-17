from eckity.genetic_operators.genetic_operator import GeneticOperator


class MsgSubtreeCrossover(GeneticOperator):
    def __init__(self, probability=1, arity=2, events=None):
        self.individuals = None
        self.applied_individuals = None
        super().__init__(probability=probability, arity=arity, events=events)

    def apply(self, individuals):

        assert len(individuals) == self.arity, f'Expected individuals list of size {self.arity}, got {len(individuals)}'

        self.individuals = individuals
        # select a random subtree from each individual's tree
        subtrees = [ind.randomSubtree() for ind in individuals]

        # assign the next individual's subtree to the current individual's tree
        for i in range(len(individuals) - 1):
            individuals[i].replace_subtree(subtrees[i+1])

        # to complete the crossover circle, assign the first subtree to the last individual
        individuals[-1].replace_subtree(subtrees[0])

        self.applied_individuals = individuals
        return individuals


