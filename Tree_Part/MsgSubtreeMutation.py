from random import uniform

from eckity.fitness.fitness import Fitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from BinTree import BinNode, BinTree


class MsgSubtreeMutation(GeneticOperator):
    def __init__(self, probability=1, arity=1, init_depth=None, events=None):
        super().__init__(probability=probability, arity=arity, events=events)
        self.init_depth = init_depth

    def apply(self, individuals):
        for ind in individuals:
            root = ind.get_root()
            self.apply_node_mutation1(node=root)

        return individuals

    def apply_node_mutation1(self, node: BinNode, const_prob: float = 0.3):
        """
               Perform subtree mutation on Binary Tree:
               We will check every internal node in the tree,
               if it has left and right, with a low probability,
               we will switch between it's left and right nodes.

               """
        if const_prob < 0 or const_prob > 1:
            raise Exception("const_prob is not between 0 to 1")

        if uniform(0, 1) <= const_prob:
            node.switch_left_and_right()

        if node.get_left() is not None:
            self.apply_node_mutation1(node.get_left())

        if node.get_right() is not None:
            self.apply_node_mutation1(node.get_right())

    def apply_node_mutation2(self, node: BinNode, const_prob: float = 0.3):
        if const_prob < 0 or const_prob > 1:
            raise Exception("const_prob is not between 0 to 1")

        if uniform(0, 1) <= const_prob:
            tree = BinTree(Fitness())
            tree.root = node
            subtree = tree.randomSubtree()
            tree.replace_subtree(subtree)
