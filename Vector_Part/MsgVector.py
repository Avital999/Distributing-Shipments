from random import randint
from random import sample
from eckity.genetic_encodings.ga.vector_individual import Vector


class MsgVector(Vector):

    def __init__(self, fitness, couriers_num: int, places_num: int):
        """

        :param fitness: Fitness
        Fitness handler class, responsible of keeping the fitness value of the individual.
        :param places_num: int
         Number of places to deliver packages, not including starting point
        """
        # check if bound include last value!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        super().__init__(fitness=fitness, length=places_num, bounds=(1, places_num+1))
        self.couriers_num = couriers_num

        if couriers_num == 0:
            raise Exception("Cannot use the algorithm with 0 couriers!")
        elif couriers_num == 1:
            self.couriers_indexes = []
            if places_num == 1:
                raise Exception("You have only one courier and one package. Just give the package to the courier!!!!")
        else:
            # Create a sorted list of couriers_indexes
            # couriers_indexes[i] represents the cell index that starts
            # the places the i+1 courier should deliver the packages to.
            if places_num < couriers_num:
                raise Exception("Places num is smaller then couriers num. "
                                "Just give every courier one package. You don't need to run the algorithm! :)")
            self.couriers_indexes = sample(range(1, places_num), couriers_num-1)
            self.couriers_indexes.sort()

    def get_couriers_indexes(self):
        return self.couriers_indexes

    def update_courier_indexes(self, courier_indexes):
        self.couriers_indexes = courier_indexes

    def get_couriers_num(self):
        return self.couriers_num


    def get_possible_values(self):
        """

        :return: possible Values that don't appear in the vector
        """
        used_values = {}

        # Add all the values already appears in the vector to the used_values
        for i in range(self.size()):
            used_values[self.cell_value(i)] = True

        # Make a list of all the possible values that are not inside the vector
        possible_values = []
        for i in range(1, self.length+1):
            if i not in used_values.keys():
                possible_values.append(i)

        return possible_values

    def switch_two_cells(self, ind1, ind2):
        if ind1 >= self.length:
            raise Exception("First cell's index is out of bound:{ind}".format(ind=ind1))
        if ind2 >= self.length:
            raise Exception("Second cell's index is out of bound:{ind}".format(ind=ind2))

        val1 = self.cell_value(ind1)
        val2 = self.cell_value(ind2)
        self.set_cell_value(index=ind1, value=val2)
        self.set_cell_value(index=ind2, value=val1)
        return self


    def get_random_number_in_bounds(self, index):
        """
        Return a random number of available cell values

        Parameters
        ----------
        index : int
            cell index

        Returns
        -------
        int
            random value according to bounds field
        """
        possible_values = self.get_possible_values()
        return possible_values[randint(0, len(possible_values)-1)]


    def show(self):
        print("The vector: {v}".format(v=self.vector))
        inds = [0]+self.couriers_indexes
        print("Index of first delivery of every courier: {lst}".format(lst=inds))

    def legal_vector(self):
        # Return if all the values between 1 to places_num(including) appeared exactly once in the vector.

        values_in_vector = {}
        for v in self.vector:
            if v in values_in_vector.keys():
                return False  # value appeared more the once
            else:
                values_in_vector[v] = 1

        for i in range(1, self.length+1):
            if i not in values_in_vector.keys():
                return False  # value didn't appear

        return True




