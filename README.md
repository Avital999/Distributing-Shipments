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





