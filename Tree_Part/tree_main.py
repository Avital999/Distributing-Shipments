from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from MsgSubtreeCrossover import MsgSubtreeCrossover
from MsgSubtreeMutation import MsgSubtreeMutation
from MsgTreeEvaluator import *
from MsgBinaryTreeCreator import MsgBinaryTreeCreator
from Others import Places

def run_tree_algo(places_matrix, couriers_num: int, max_distance, courier_delay):
    terminal_set = list(range(1, len(places_matrix)))
    algo = SimpleEvolution(
        Subpopulation(creators=MsgBinaryTreeCreator(couriers_num=couriers_num,
                                                    terminal_set=terminal_set,
                                                    init_depth=None,
                                                    function_set=None),
                      population_size=100,

                      # user-defined fitness evaluation method
                      evaluator=MsgTreeEvaluator(places_matrix=places_matrix, max_distance=max_distance,
                                                 couriers_num=couriers_num, delay_for_courier=courier_delay),
                      # minimization problem (fitness is MAE), so higher fitness is worse
                      higher_is_better=False,
                      elitism_rate=0.5,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[

                          MsgSubtreeCrossover(probability=0.8, arity=2),
                          MsgSubtreeMutation(probability=0.6, arity=1),
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=False), 1)
                      ]
                      ),
        breeder=SimpleBreeder(),
        max_workers=4,
        max_generation=300,
        # random_seed=0,
        termination_checker=ThresholdFromTargetTerminationChecker(optimal=0, threshold=0.001),
        statistics=BestAverageWorstStatistics()
    )

    # evolve the generated initial population
    algo.evolve()
