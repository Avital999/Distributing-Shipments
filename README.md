# Distributing-Shipments
Mini Project - Topics in Computer Science, VRP optimization through Evolutionary Algorithms.
By Avital Vinograd and Noa Levin.

## Introduction
Covid-19 caused a global economic recession, leading to immense industry changes. During this financial crisis, delivery businesses bloomed and until today remain an integral part of modern life and an important part of the industry.
Delivery businesses face several challenges. First, goods need to be transferred to multiple varied addresses via a limited number of transporters. Second, to ensure customer satisfaction and keep a high retention rate, deliveries must arrive at the optimal time. In addition, expenses needed for distribution (such as fuel) need to be carefully managed.
 
 A prime example that will be used to present the problem is a restaurant delivery service. Using a limited number of couriers, some will be tasked to deliver several orders. As preparing meals takes time, each courier will leave at a different time. Since the dishes are best served fresh, fast delivery is an important factor. 
Let’s assume that given a list of different addresses that require food delivered, using a fixed number of couriers, and a deadline for each delivery we’d like to find the best way to use each courier so that each delivery will arrive at the customer's address on time.

The problem presented above is an example of a VRP - Vehicle Routing Problem. VRP deals with arranging an optimal set of routes for vehicles to transport deliveries for a given set of customers.  This is a generalization of the Traveling Salesman problem and therefore is classified as NP-Hard. Meaning, while P=NP is unknown we can’t determine that an efficient solution in polynomial time exists.
In our case, we add an additional factor to the VRP. In addition to distributing deliveries between couriers (and therefore setting a route using the delivery address), we also wish to determine the order of departure from the place of origin (the restaurant address in our case). We may not be able to find the most optimal solution, but we’ll set limitations such that a good solution will be provided.
In our project, we used the EC-Kity package, an evolutionary computation tool kit in python. Our purpose was to develop an evolutionary algorithm that will help us to find a solution for distributing deliveries between messengers.

## Problem Description
 
In our project we focused on finding the best solution based on the restaurant example. We limited the number of couriers, and the distance an order can be requested from the restaurant. 
In order to deliver the orders in the shortest possible time we chose to focus on 3 main questions:
1)     How to divide the deliveries between the couriers?
2)     In what order will each courier bring his shipments?
3)     In which order will the couriers leave the restaurant?
Using the EC-Kity package we created two different representations of the problem:
Creating a new individual, a complete binary tree
Adjusting the vector individual from the EC-Kity package to match the problem

### Defining the problem:
Goal: Minimize the time it takes to deliver all the shipments.
couriers_num - Number of couriers.
delay = Difference (in minutes) between the departure time of each courier
places_matrix = neighborhood symmetric matrix which represents the locations where the deliveries need to arrive, the location of the restaurant, and the distances between each pair of them (Distance is measured in minutes).
In our project, we have a function that creates a random symmetric neighborhood matrix M such that Mij is the distance (in minutes) from the address of delivery number i to the address of delivery number j. The central position is at the middle point.

## Solution Description
We used the EC-Kity package in order to implement an evolutionary algorithm that will help us to minimize the total delivery time required to complete all the orders.
As stated previously, we create 2 representations to find possible solutions:
‘BinTree’ - a complete binary tree, a new individual.
‘MsgVector’ - expansion of the vector class.
We can choose which individual representation to run the algorithm with. 
Each individual in the population represents a possible solution to the problem. Therefore, each individual includes information on the courier leave order, and the deliveries tasked to each one.  We can calculate the delivery time for each order using the places_matrix. 
For each individual, in every generation, we calculate the total delivery package time and use it to mark the individual's fitness.  
The lower our fitness, the better it is.
The best result in all generations is saved, and this is our solution.


###Tree representation:
We created a new individual (a class that inherits from ‘Individual’) In the form of a complete binary tree. The leaves of the tree represent the deliveries, with the internal nodes being one of 2 functions:
“change courier” - the next orders will be tasked to the next courier.
“keep going” - continue assigning deliveries to the current courier.
Traversing the tree in an in-order manner will result in an array of values including all tree nodes. Next, we iterate the array to determine the delivery distribution between couriers. 
Starting from i=0, all viewed deliveries will be assigned to member i until we view an occurrence of “change courier”. Afterward, we promote i, s.t. the next orders are assigned to the next member, and so on.

For the new individual, we created a new crossover operator. Similar to the crossover function in the EC-Kity package, the operator first goes over the sub-population of trees and selects a random subtree from every tree in the sub-population. Afterward, going over the sub-population for each tree, a random subtree will be replaced with a subtree previously selected from the next tree. 
For our representation, each random subtree will be the same height, set to be ⅓ of the tree height. Additionally, each new individual has been tested s.t. all deliveries appear exactly one time.   
In addition, we created two types of mutation operators.
The first mutation goes over the nodes and determines with a fixed probability whether to swap the right and left sons of each node. The mutation starts from the root and recursively traverses the tree.
The second mutation takes 2 random subtrees from the current tree and swaps them. The randomly selected subtrees are always the same height, the upper bound of ⅓ of the tree height.

The classes we created for the complete binary tree are:
 
class BinNode
class BinTree(Individual)
class MsgBinaryTreeCreator(Creator)
class MsgSubtreeCrossover(GeneticOperator)
class MsgSubtreeMutation(GeneticOperator)
class MsgTreeEvaluator(SimpleIndividualEvaluator)
 
So that we can run the algorithm we added the file tree_main.

###Vector representation
 
We created a new Vector (a class that inherits from Vector) called MsgVector.
In EC-Kity, the vector is represented as a list. The MsgVector’s list is a permutation of the numbers from 1 to the number of locations. Each element is an address index matching the corresponding index in the places_matrix.
The MsgVector has two fields in addition to the Vector’s field:
couriers_num - number of couriers
couriers_indexes - a sorted list, representing the first index in the vector from which each courier starting with the second courier takes the shipments.
The first courier that is leaving the restaurant will take the shipments to the locations vector[0],...., vector[couriers_indexes[0]-1].The second courier will take the shipments to the location vector[couriers_indexes[1]], ..., vector[courier_indexes[2]-1], and so on.
For example couriers_indexes[0] = 4, this means that deliveries 0 to 3 are assigned to the first courier.
We created a new crossover operator for MsgVector, called ‘MsgVectorKPointsCrossover’ which inherits EC-Kity’s genetic operator named ‘VectorKPointsCrossover’.
The ‘apply’ method of the new crossover calls the ‘apply’ method from ‘VectorKPointsCrossover’. After applying the crossover, the vector is corrected so each number between 1 and the number of locations that appeared previously will exist in the modified vector.
In addition, we added the class ‘MsgVectorCouriersMutation’ which inherits the class ‘GeneticOperator’ from EC-Kity. In the apply method, we update every individual’s couriers_indexes in the following form: we change one index to a different number that doesn’t appear in the list, randomly selected between 1 and the number of locations. Afterward, we make sure the list remains sorted.
Another operator we added is ‘MsgVectorDeliveriesMutation’ which also inherits the class ‘GeneticOperator’ from EC-Kity. For each individual separately, with different probabilities, the operator activates one of the following mutations:
change places in vector - switch between k pairs of cells, while k=log(vector’s length).
shuffle random part in vector - shuffle a random part of the vector.
shuffle courier deliveries - shuffle the deliveries (cell values) of one of the couriers.

The classes we created for the vector:
MsgVector (Vector)
class MsgVectorCouriersMutation(GeneticOperator)
class MsgVectorCreator(Creator):
class MsgVectorDeliveriesMutation(GeneticOperator):
class MsgVectorEvaluator(SimpleIndividualEvaluator):
class MsgVectorKPointsCrossover(VectorKPointsCrossover):

So that we can run the algorithm we added the file vector_main.


###Calculating Fitness
Both individual representations allow the extraction of the relevant information required to calculate the fitness function. 
Each location has a unique corresponding index in the place_matrix, ranging from 1 to the number of locations.
Assuming we want to calculate the time it takes to deliver the package to location number X in some individual. The i courier that leaves the restaurant should deliver the shipment to location number X. It is the k delivery in the courier’s route. 
We will mark the time it takes to deliver the shipment as T(i,k).
If there is at least one shipment that the courier should deliver before X, we will mark the number of the location before X in the courier’s route as Y.
<br>
*if k=1, T(i,k) = placesmatrix[0][X]+delay(i-1)<br>*
*if k>1, T(i,k) = T(i,k-1)+placesmatrix[Y][X]<br>*

*Please note, placesmatrix[a,b] marks distance locations a and b, with 0 marking the departure origin point (restaurant location).
We will add up the time it took to bring each shipment separately, and the sum we will get is the individual’s fitness.*


##Running examples:

In our examples, we wanted to refer to realistic situations as much as possible.
Based on our familiarity with the restaurant delivery business, we chose the following example:
couriers_num = 7
delay (between one courier to the next one) - 5 (minutes)
places_matrix - appears in the file Running_Examples/formatted_mat.csv 
In our location matrix, the center (restaurant) is in the center of a map that includes all the locations. The size of the map is 60*60 and there are 30 locations on the map.

Based on the example we stated the following goals and limitations:
As each courier will most likely be tasked with several deliveries, each can be up to 42.5 minutes away from the restaurant, we decided on a total time of 90 minutes for each courier to perform its given tasks.
Assuming order preparation takes 30 minutes, and based on the places_matrix we chose, the food must arrive in up to 60 minutes. In addition, we’ll sort the order the couriers leave time, such that each one will leave 5 minutes after the previous one.
Tree running example:

generation #0<br>
subpopulation #0<br>
best fitness 2714.03<br>
worst fitness 6519.91<br>
average fitness 3931.0576<br>
<br>
.
.
.
<br>
- generation #120<br>
subpopulation #0<br>
best fitness 1885.44<br>
worst fitness 4250.83<br>
average fitness 2433.4098<br>
<br>
 …<br>
- generation #299<br>
subpopulation #0<br>
best fitness 1974.8<br>
worst fitness 4053.61<br>
average fitness 2482.8885<br>


the Tree - in order - [9, 'Keep going', 29, 'Keep going', 16, 'Keep going', 25, 'Change courier', 28, 'Keep going', 22, 'Keep going', 30, 'Keep going', 19, 'Keep going', 18, 'Change courier', 1, 'Change courier', 26, 'Change courier', 2, 'Keep going', 8, 'Keep going', 21, 'Keep going', 12, 'Change courier', 13, 'Change courier', 7, 'Change courier', 6, 'Keep going', 14, 'Change courier', 27, 'Change courier', 4, 'Change courier', 11, 'Keep going', 17, 'Change courier', 3, 'Change courier', 23, 'Change courier', 10, 'Keep going', 5, 'Change courier', 15, 'Change courier', 24, 'Change courier', 20]

**1885.44**

## Vector running example:
generation #0<br>
subpopulation #0<br>
best fitness 2626.6499999999996<br>
worst fitness 5238.87<br>
average fitness 3745.8202<br>

generation #1<br>
subpopulation #0<br>
best fitness 2733.96<br>
worst fitness 5174.4400000000005<br>
average fitness 3512.7490000000003<br>
<br> ... <br>
generation #232 <br>
subpopulation #0 <br>
best fitness 1812.9599999999998<br>
worst fitness 3604.92<br>
average fitness 2330.9674<br>
<br> ...
<br>
generation #399 <br>
subpopulation #0 <br>
best fitness 1743.7600000000002 <br>
worst fitness 4159.9800000000005 <br>
average fitness 2260.7506999999996 <br> 

The vector: [5, 20, 24, 23, 9, 12, 21, 8, 1, 2, 13, 7, 26, 15, 25, 29, 16, 27, 14, 10, 6, 11, 28, 22, 19, 30, 18, 4, 17, 3]

Index of first delivery of every courier: [0, 5, 9, 14, 20, 24, 27]

**1662.1700000000003**

##Results / Findings

As we explained earlier, we created several mutation types both for the tree and for the vector. We performed multiple running tests in order to compare the efficiency of the different mutations. 
We used the same example input in all the algorithm runs.

#choosing the best mutation - Tree
We created 2 types of mutations for the tree representation.
We performed 30 tests to compare their efficiency:
Best result of each running example:

![alt test](https://github.com/Avital999/Distributing-Shipments/blob/main/Results/treemutations.png)








