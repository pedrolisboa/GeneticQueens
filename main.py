from genetic_algorithm import genetic_algorithm

if __name__ == "__main__":
    dimension=60
    population_size = 30
    mating_pool_ratio = 0.5
    mutation_probability = 0.1
    patience = 500

    # Example usage
    results = genetic_algorithm(population_size=population_size, dimension=dimension, 
                        mating_pool_ratio=mating_pool_ratio, mutation_probability=mutation_probability,
                        patience=patience)
    print(f"Best Fitness: {results['best_fitness']}")
    print(f"Rounds: {results['rounds']}, Rounds Without Improvement: {results['rounds_without_improvement']}")
