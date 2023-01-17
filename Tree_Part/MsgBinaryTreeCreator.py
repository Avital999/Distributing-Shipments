from eckity.creators.creator import Creator
from eckity.genetic_encodings.gp.tree.functions import f_add, f_sub, f_mul, f_div
from eckity.fitness.gp_fitness import GPFitness
from eckity.genetic_encodings.gp.tree.tree_individual import Tree
from eckity.creators.gp_creators.tree_creator import GPTreeCreator
import numpy as np
import BinTree
from BinTree import BinNode
from BinTree import BinTree
import random

from abc import abstractmethod


class MsgBinaryTreeCreator(Creator):
    def __init__(self,
                 couriers_num: int,
                 terminal_set,
                 init_depth=None,
                 function_set=None,
                 erc_range=None,
                 bloat_weight=0.001,
                 events=None):

        self.bloat_weight = bloat_weight
        packages_num = len(terminal_set)

        if couriers_num < 1:
            raise Exception("no couriers")

        if init_depth is None:
            # complete tree with packages_num leaves depth's is between (int)log2(package_num)
            # to (int)log2(package_num)+1.
            min_length = int(np.log2([packages_num])[0])
            max_length = int(np.log2([packages_num])[0]) + 1
            self.init_depth = (min_length, max_length)
        else:
            self.init_depth = init_depth

        if function_set is None:
            self.function_set = ["Change courier", "Keep going"]
        else:
            self.function_set = function_set

        super().__init__(events=events)
        self.couriers_num = couriers_num
        self.terminal_set = terminal_set

    def create_individuals(self, n_individuals, higher_is_better):
        min_depth, max_depth = self.init_depth[0], self.init_depth[1]
        individuals = [BinTree(fitness=GPFitness(bloat_weight=self.bloat_weight, higher_is_better=higher_is_better))
                       for _ in range(n_individuals)]
        for ind in individuals:
            self.create_tree(ind, max_depth)
        self.created_individuals = individuals

        return individuals

    def create_tree(self, tree_ind, max_depth):
        # a complete tree with n leaves (the terminal_set) has n-1 internal nodes (the function_set)
        internal_nodes = len(self.terminal_set)-1
        # if there are more couriers the packages we still create tree for all couriers
        num_nodes = np.maximum([internal_nodes], [self.couriers_num-1])[0]
        # create array with size=num_nodes - number of internal nodes
        nodes = [0 for i in range(num_nodes)]
        # fill array with couriers_num "Change courier"s and the rest of the array with "Keep going"s
        for i in range(self.couriers_num-1):
            nodes[i] = "Change courier"
        for i in range(len(nodes) - self.couriers_num+1):
            nodes[i + self.couriers_num-1] = "Keep going"
        random.shuffle(nodes)
        # enter all the internal nodes randomly
        for i in range(len(nodes)):
            tree_ind.add(nodes[i])
        leaves = self.terminal_set.copy()
        random.shuffle(leaves)
        # enter leaves randomly
        for leave in leaves:
            tree_ind.add(leave)

