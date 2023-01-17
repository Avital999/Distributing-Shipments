from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from Vector_Part.MsgVectorCreator import MsgVectorCreator
from Vector_Part.MsgVectorDeliveriesMutation import MsgVectorDeliveriesMutation
from Vector_Part.MsgVectorEvaluator import MsgVectorEvaluator
from Vector_Part.MsgVectorKPointsCrossover import MsgVectorKPointsCrossover
from Vector_Part.MsgVectorCouriersMutation import MsgVectorCouriersMutation


def run_vector_algo(places_matrix, couriers_num: int, max_distance, courier_delay):
    # places_matrix includes the center as the first place
    packages_num = len(places_matrix) - 1

    algo = SimpleEvolution(
        Subpopulation(creators=MsgVectorCreator(couriers_num=couriers_num, places_num=packages_num),
                      population_size=100,
                      # user-defined fitness evaluation method
                      evaluator=MsgVectorEvaluator(places_matrix=places_matrix,
                                                   max_distance=max_distance,
                                                   couriers_num=couriers_num,
                                                   delay_for_courier=courier_delay
                                                   ),
                      # minimization problem (fitness is MAE), so higher fitness is worse
                      higher_is_better=False,
                      elitism_rate=1 / 300,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          MsgVectorKPointsCrossover(probability=0.3, k=1),
                          MsgVectorDeliveriesMutation(probability=0.8, arity=1),
                          MsgVectorCouriersMutation(probability=0.95, arity=1)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=3, higher_is_better=True), 1)
                      ]
                      ),
        breeder=SimpleBreeder(),
        max_workers=4,
        max_generation=350,

        termination_checker=ThresholdFromTargetTerminationChecker(optimal=0, threshold=0.0),
        statistics=BestAverageWorstStatistics()
    )
    # evolve the generated initial population
    algo.evolve()

