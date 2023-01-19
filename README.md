# Distributing-Shipments
### Mini Project - Topics in Computer Science, VRP optimization through Evolutionary Algorithms.<br>
By Avital Vinograd and Noa Levin.<br>

*Python 3.11 is required to run the code.*

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
1. Creating a new individual, a complete binary tree
2. Adjusting the vector individual from the EC-Kity package to match the problem

### Defining the problem:
**Goal : Minimize the time it takes to deliver all the shipments.** <br>

couriers_num - Number of couriers.<br>
delay = Difference (in minutes) between the departure time of each courier. <br>
places_matrix = neighborhood symmetric matrix which represents the locations where the deliveries need to arrive, the location of the restaurant, and the distances between each pair of them (Distance is measured in minutes).<br>
*In our project, we have a function that creates a random symmetric neighborhood matrix M such that Mij is the distance (in minutes) from the address of delivery number i to the address of delivery number j. The central position is at the middle point.*<br>


## Solution Description
We used the EC-Kity package in order to implement an evolutionary algorithm that will help us to minimize the total delivery time required to complete all the orders.
As stated previously, we create 2 representations to find possible solutions:
1. ‘BinTree’ - a complete binary tree, a new individual.
2. ‘MsgVector’ - expansion of the vector class.
We can choose which individual representation to run the algorithm with. 
Each individual in the population represents a possible solution to the problem. Therefore, each individual includes information on the courier leave order, and the deliveries tasked to each one.  We can calculate the delivery time for each order using the places_matrix. 
For each individual, in every generation, we calculate the total delivery package time and use it to mark the individual's fitness.  
The lower our fitness, the better it is.
The best result in all generations is saved, and this is our solution.


### Tree representation:
We created a new individual (a class that inherits from ‘Individual’) In the form of a complete binary tree. The leaves of the tree represent the deliveries, with the internal nodes being one of 2 functions: <br>
1. “change courier” - the next orders will be tasked to the next courier.
2. “keep going” - continue assigning deliveries to the current courier.
Traversing the tree in an in-order manner will result in an array of values including all tree nodes. Next, we iterate the array to determine the delivery distribution between couriers. 
Starting from i=0, all viewed deliveries will be assigned to member i until we view an occurrence of “change courier”. Afterward, we promote i, s.t. the next orders are assigned to the next member, and so on.<br> 

For the new individual, we created a new crossover operator. Similar to the crossover function in the EC-Kity package, the operator first goes over the sub-population of trees and selects a random subtree from every tree in the sub-population. Afterward, going over the sub-population for each tree, a random subtree will be replaced with a subtree previously selected from the next tree. <br>
For our representation, each random subtree will be the same height, set to be ⅓ of the tree height. Additionally, each new individual has been tested s.t. all deliveries appear exactly one time.   <br>
In addition, we created two types of mutation operators. <br>
The first mutation goes over the nodes and determines with a fixed probability whether to swap the right and left sons of each node. The mutation starts from the root and recursively traverses the tree. <br>
The second mutation takes 2 random subtrees from the current tree and swaps them. The randomly selected subtrees are always the same height, the upper bound of ⅓ of the tree height. <br>

The classes we created for the complete binary tree are: <br>
 
class BinNode <br>
class BinTree(Individual)<br>
class MsgBinaryTreeCreator(Creator)<br>
class MsgSubtreeCrossover(GeneticOperator)<br>
class MsgSubtreeMutation(GeneticOperator)<br>
class MsgTreeEvaluator(SimpleIndividualEvaluator)<br>
 
So that we can run the algorithm we added the file tree_main.<br>


### Vector representation
 
 
We created a new Vector (a class that inherits from Vector) called MsgVector.<br>
In EC-Kity, the vector is represented as a list. The MsgVector’s list is a permutation of the numbers from 1 to the number of locations. Each element is an address index matching the corresponding index in the places_matrix.<br>
The MsgVector has two fields in addition to the Vector’s field:<br>
1. couriers_num - number of couriers
2. couriers_indexes - a sorted list, representing the first index in the vector from which each courier starting with the second courier takes the shipments.
The first courier that is leaving the restaurant will take the shipments to the locations vector[0],...., vector[couriers_indexes[0]-1].The second courier will take the shipments to the location vector[couriers_indexes[1]], ..., vector[courier_indexes[2]-1], and so on.<br>
For example couriers_indexes[0] = 4, this means that deliveries 0 to 3 are assigned to the first courier.

We created a new crossover operator for MsgVector, called ‘MsgVectorKPointsCrossover’ which inherits EC-Kity’s genetic operator named ‘VectorKPointsCrossover’.
The ‘apply’ method of the new crossover calls the ‘apply’ method from ‘VectorKPointsCrossover’. After applying the crossover, the vector is corrected so each number between 1 and the number of locations that appeared previously will exist in the modified vector.<br>
In addition, we added the class ‘MsgVectorCouriersMutation’ which inherits the class ‘GeneticOperator’ from EC-Kity. In the apply method, we update every individual’s couriers_indexes in the following form: we change one index to a different number that doesn’t appear in the list, randomly selected between 1 and the number of locations. Afterward, we make sure the list remains sorted.<br>
Another operator we added is ‘MsgVectorDeliveriesMutation’ which also inherits the class ‘GeneticOperator’ from EC-Kity. For each individual separately, with different probabilities, the operator activates one of the following mutations:<br>
1. change places in vector - switch between k pairs of cells, while k=log(vector’s length).
2. shuffle random part in vector - shuffle a random part of the vector.
3. shuffle courier deliveries - shuffle the deliveries (cell values) of one of the couriers.

The classes we created for the vector<br>
MsgVector (Vector) <br>
class MsgVectorCouriersMutation(GeneticOperator)<br>
class MsgVectorCreator(Creator)<br>
class MsgVectorDeliveriesMutation(GeneticOperator)<br>
class MsgVectorEvaluator(SimpleIndividualEvaluator)<br>
class MsgVectorKPointsCrossover(VectorKPointsCrossover)<br>
<br>
So that we can run the algorithm we added the file vector_main.<br>



### Calculating Fitness
Both individual representations allow the extraction of the relevant information required to calculate the fitness function. 
Each location has a unique corresponding index in the place_matrix, ranging from 1 to the number of locations.<br>
Assuming we want to calculate the time it takes to deliver the package to location number X in some individual. <br>
The i courier that leaves the restaurant should deliver the shipment to location number X. It is the k delivery in the courier’s route. <br>
We will mark the time it takes to deliver the shipment as T(i,k). <br>
If there is at least one shipment that the courier should deliver before X, we will mark the number of the location before X in the courier’s route as Y.
<br><br>
*if k=1, T(i,k) = placesmatrix[0][X] + delay(i-1)<br>*
*if k>1, T(i,k) = T(i,k-1) + placesmatrix[Y][X]<br>*

*Please note, placesmatrix[a,b] marks distance locations a and b, with 0 marking the departure origin point (restaurant location).
We will add up the time it took to bring each shipment separately, and the sum we will get is the individual’s fitness.*


## Running examples:

In our examples, we wanted to refer to realistic situations as much as possible.
Based on our familiarity with the restaurant delivery business, we chose the following example:
couriers_num = 7
delay (between one courier to the next one) - 5 (minutes)
places_matrix - appears in the file Running_Examples/formatted_mat.csv 
In our location matrix, the center (restaurant) is in the center of a map that includes all the locations. The size of the map is 60*60 and there are 30 locations on the map.

Based on the example we stated the following goals and limitations:
As each courier will most likely be tasked with several deliveries, each can be up to 42.5 minutes away from the restaurant, we decided on a total time of 90 minutes for each courier to perform its given tasks.
Assuming order preparation takes 30 minutes, and based on the places_matrix we chose, the food must arrive in up to 60 minutes. In addition, we’ll sort the order the couriers leave time, such that each one will leave 5 minutes after the previous one.
# Tree running example:

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
generation #120<br>
subpopulation #0<br>
best fitness 1885.44<br>
worst fitness 4250.83<br>
average fitness 2433.4098<br>
<br>
 …<br>
generation #299<br>
subpopulation #0<br>
best fitness 1974.8<br>
worst fitness 4053.61<br>
average fitness 2482.8885<br>


the Tree - in order - [9, 'Keep going', 29, 'Keep going', 16, 'Keep going', 25, 'Change courier', 28, 'Keep going', 22, 'Keep going', 30, 'Keep going', 19, 'Keep going', 18, 'Change courier', 1, 'Change courier', 26, 'Change courier', 2, 'Keep going', 8, 'Keep going', 21, 'Keep going', 12, 'Change courier', 13, 'Change courier', 7, 'Change courier', 6, 'Keep going', 14, 'Change courier', 27, 'Change courier', 4, 'Change courier', 11, 'Keep going', 17, 'Change courier', 3, 'Change courier', 23, 'Change courier', 10, 'Keep going', 5, 'Change courier', 15, 'Change courier', 24, 'Change courier', 20]

**1885.44**

# Vector running example:
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

## Findings

As we explained earlier, we created several mutation types both for the tree and for the vector. We performed multiple running tests in order to compare the efficiency of the different mutations. 
We used the same example input in all the algorithm runs.

### choosing the best mutation - Tree
We created 2 types of mutations for the tree representation.
We performed 30 tests to compare their efficiency:
Best result of each running example:

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/treemutations.png" width="500"/>

<br>
the best result we got: was 1776.37 using the second mutation<br>

We would like to show the differences between the results of using the first mutation and the second mutation:<br>
Best Results comparing both mutations:<br>

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20trees's%20mutations%20-%20box%20graph.png" width="500"/>

Each box in the graph represents the best fitness results in the 30 runs with the relevant mutation. <br>
Average results: <br>
First tree mutation: 1984.4 <br>
Second tree mutation: 1996.2<br>

In the following scatter plot, we see results received from 30 running examples, for each tree mutation used. Each point in the graph represents the ‘best fitness’ of one of the runs:<br>


<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20tree's%20mutations%20-%20scatter%20plot.png" width="500"/>

### Choosing the best mutation - vector
We created 3 different mutations that change the order of deliveries in the vector.<br> Therefore, we wanted to check which one achieves the best results.<br> For the purpose of finding the most efficient mutation, we adjusted the probabilities in the method ‘apply’ of the operator ‘MsgVectorDeliveriesMutation’ such that in each run only one mutation will occur.<br>
We performed 30 runs with each mutation, with a population size of 100, and 400 generations for each algorithm run.<br>

These are the results we got, in every run, we kept the best fitness.<br>
The following table displays the best fitness received for each run, using one mutation:<br>

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/vector%20running%20examples%20table.png" width="500"/>

Average results:<br>
First Vector’s Mutation - 2282.2<br>
Second Vector’s Mutation - 1762.97<br>
Third Vector’s Mutation - 1653.1<br>

Best result: 1458.2<br>
The results are shown in a box plot:<br>

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20vector's%20mutations%20-%20box%20graph.png" width="500"/>

Each box in the graph represents the best fitness results in  the 30 runs with the relevant mutation.

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20vector's%20mutations-%20%20scatter%20plot.png" width="500"/>

In the scatter plot, we can see the results of the 30 running examples we got for each mutation tested. Each point in the graph represents the ‘best fitness’ for each run.<br>

The following chart compares performance results between the two individual representations (both with the mutation that got the best results): <br>

<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20vector%20and%20tree.png" width="500"/>


## conclusions:

- On average when running the vector algorithm we got significantly better results with the third mutation, in comparison to the first two. Moreover, the first mutation had the highest delivery times, such that the best-case result received is less optimal than the worst-case found in the second mutation. Therefore, we can conclude that the third mutation is the most preferred choice.<br>


- We see no major difference when comparing the results received from the first and second tree mutations. However, based on the scattering graph we see that the results of the first mutation have a lower deflection. Meaning, it’s less likely to get a result significantly higher than the average result. Based on this, we’d prefer to use the first mutation. <br>


- When comparing the results of the preferred mutation in both representations, we see that the vector representation leads to better results in almost all the cases, the difference is significant in most of them. Therefore, we can conclude it is better to use the vector’s algorithm.<br>


- Since each delivery should arrive at its destination in 60 minutes, the desired output of the fitness algorithm would be less than 1800. And indeed, with the vector representation, in 96% of cases, the third mutation succeeded the objective, with an average time of 1653.1 minutes to deliver all the packages. Meaning, in case of a failure (higher than 1800) an additional run of the algorithm will likely grant the desired output.<br>

## Bonus information: Competing Google Algorithm
Toward the submission of the project, in order to define a good benchmark, we searched for an existing efficient algorithm to solve our problem.  <br>
We found out that Google has published a code, based on their own library “or-tools”, that solves a similar problem. Their algorithm receives a distance matrix (as our places matrix), number of vehicles, number of locations, and depot. <br>
The purpose of google’s algorithm is to find the ideal routes for the messenger while taking into account that the messengers also have to return to the starting point.
This algorithm returns the messenger routes and their lengths. <br>
In order to compare both algorithms, we made a slight adjustment to our algorithm by changing the fitness function. <br>
For each individual, the new fitness is the sum of the messenger route lengths, including the time it takes to get from the last point of the route to the starting point. <br>


In the example presented by google, this is the illustration of the distance matrix:<br>
<img src="https://github.com/Avital999/Distributing-Shipments/blob/main/Results/comparing%20vector%20and%20tree.png" width="500"/>
<br>The corresponding solution provided by Google’s algorithm: <br>
<img src="hhttps://github.com/Avital999/Distributing-Shipments/blob/main/Results/solution%20-%20google%20algorithm.png" width="500"/>

The total distance of all roads is 6208. <br>

Using the same distance matrix, number of couriers, and number of locations as in google’s example, and a delay of 0 minutes. <br><br>
*link to more information about Google’s example and distance matrix mentioned in the Bibliography section.* <br>

We ran our adapted algorithm 30 times and got an average fitness of 6137. <br>
It’s important to note that Google's algorithm limits the maximum distance each vehicle can travel, while our algorithm has no such limitation. <br>

## Bibliography
1. ‘Computational Complexity CSC 5802’, Professor: Tom Altman <br>
     http://cse.ucdenver.edu/~cscialtman/complexity/Report.pdf <br>
2. EC-KitY GitHub:<br>
     https://github.com/EC-KitY/EC-KitY <br>
3. Vehicle Routing Problem - Google for developers <br>
     https://developers.google.com/optimization/routing/vrp <br>







