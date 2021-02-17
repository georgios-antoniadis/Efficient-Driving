# Efficient-Driving
3rd Year Project for the school of Physics and Astronomy of the University of Nottingham. 

The aim of the algorithm is to simulate a car's engine and through machine learning teach itself to drive in the most efficient way possible.

The NEAT (Neuro evolution of augmented topologies) algorithm is used (see Efficient Evolution of Neural Network Topologies by Kenneth O. Stanley and Risto Miikkulainen) as the implementation of machine learning in this case. 

The population size of each generation is 20 individuals.

The function used is a different version of the ReLU function called leaky ReLU f(x) = mod(x) if x > 0 or f(x) = -0.01x if x <= 0.

The tool is built so that the user can change the test scenarios in a few lines of code or even by changing specific variables inside the code.
