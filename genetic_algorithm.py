import numpy as np
from typing import Tuple, Dict

def initialize_population(population_size, dimension) -> np.ndarray:
    return np.array([np.random.permutation(np.arange(1, dimension + 1)) for _ in range(population_size)])

def fitness(x):
    checks = compute_checks_array(x)
    return -checks

def mutate(individual: np.ndarray, dimension, mutation_probability) -> np.ndarray:
    if np.random.rand() < mutation_probability:
        swap_indices = np.random.choice(dimension, 2, replace=False)
        individual[swap_indices[0]], individual[swap_indices[1]] = individual[swap_indices[1]], individual[swap_indices[0]]
    return individual

def crossover(parent1,parent2):
    D = len(parent1)
    assert (len(parent2) == D), "Parents are not of the same size"
    crossover_point = np.random.choice(D)
    if (crossover_point == 0):
        crossover_point = crossover_point+1
    
    children_1 = np.zeros((D))
    children_2 = np.zeros((D))
    
    children_1[0:crossover_point-1] = parent1[0:crossover_point-1]
    children_2[0:crossover_point-1] = parent2[0:crossover_point-1] 

    complement_1 = parent2
    complement_2 = parent1
    for i in range(0,crossover_point):
        complement_1 = complement_1[complement_1 != children_1[i]]
        complement_2 = complement_2[complement_2 != children_2[i]]
    
    children_1[crossover_point-1:] = complement_1[:]
    children_2[crossover_point-1:] = complement_2[:]
    return children_1,children_2

def compute_checks_array(p,DEBUG=False):
    assert (len(p) == len(set(p))), "Invalid Individual"
    checks = 0
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if (p[i] + (j-i) == p[j]):
                checks = checks + 1
            elif (p[i] - (j-i) == p[j]):
                checks = checks + 1
                    
    return checks

def selection(fitnesses: np.ndarray, population_size) -> Tuple[int, int]:
    probabilities = np.exp(fitnesses)
    probabilities /= probabilities.sum()
    return tuple(np.random.choice(population_size, 2, replace=False, p=probabilities))

def genetic_algorithm(population_size: int, dimension: int, mating_pool_ratio: int, 
                      mutation_probability: float, patience: int,
                      log_fn=None) -> Dict[str, any]:
    population = initialize_population(population_size, dimension)
    best_fitness = -np.inf
    best_individual = None
    best_possible_fitness = 0 #self.dimension * (self.dimension - 1) / 2
    rounds_without_improvement = 0
    rounds = 0
    evaluations = 0
    mating_pool_size = int(population_size * mating_pool_ratio)

    population_fitness = np.array([fitness(ind) for ind in population])
    while best_fitness != best_possible_fitness and rounds_without_improvement < patience:

        max_fitness_index = np.argmax(population_fitness)
        if population_fitness[max_fitness_index] > best_fitness:
            best_fitness = population_fitness[max_fitness_index]
            best_individual = population[max_fitness_index]

        children = []
        for _ in range(mating_pool_size):
            p1, p2 = selection(population_fitness, population_size)
            c1, c2 = crossover(population[p1], population[p2])
            c1, c2 = mutate(c1, dimension, mutation_probability), mutate(c2, dimension, mutation_probability)
            children.extend([c1, c2])
        
        children = np.array(children)
        population = np.concatenate([population, children], axis=0)
        population_fitness = np.array([fitness(indv) for indv in population])
        evaluations += len(population)

        sorted_indices = np.argsort(population_fitness)[::-1]
        population = population[sorted_indices][:population_size]
        population_fitness = population_fitness[sorted_indices][:population_size]
        rounds += 1

        if best_fitness == population_fitness[max_fitness_index]:
            rounds_without_improvement += 1
        else:
            rounds_without_improvement = 0

        log_fn({
                "round": rounds, 
                "fitness": best_fitness, 
                "rounds_without_improvement": rounds_without_improvement,
 
        })    

    return {
        "best_individual": best_individual,
        "best_fitness": best_fitness,
        "rounds_without_improvement": rounds_without_improvement,
        "rounds": rounds,
        "aes": evaluations/rounds,
        "evaluations": evaluations
    }

