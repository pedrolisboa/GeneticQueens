import wandb
import sys
from datetime import datetime
from genetic_algorithm import genetic_algorithm
from multiprocessing import Pool, cpu_count

from hasher import *

sys.path.append("./")

sweep_config = {
    'method': 'grid',  # Can be "grid", "random", or "bayes"
    'metric': {
        'name': 'fitness',
        'goal': 'maximize'   
    },
    'parameters': {
        "dimension": {
            "values": list(range(6, 27, 2))#[5, 8, 30, 40]
        },
        "population_size": {
            "values": [32, 64, 128, 256, 512, 1024]#list(range(10, 100, 20))
        },
        "mating_pool_ratio": {
            "values": [0.3, 0.5, 0.8]
        },
        "mutation_probability": {
            "values": [0.1, 0.3, 0.5]
        },
        "patience": {
            "values": [500]
        },
        "init": {
            "values": list(range(10))
        }
    }
}

def optimize(config=None):
    c = datetime.now()
    print('Starting sweep. current Date and Time is:', c)
    with wandb.init(config=config) as run:
        config = run.config
        
        config_hash = generate_hash(config)
        if has_been_run(config_hash):
            print("Configuration has already been run. Skipping...")
            wandb.log({"duplicate": True})
            return

        dimension = config.dimension
        population_size = config.population_size
        mating_pool_ratio = config.mating_pool_ratio
        mutation_probability = config.mutation_probability
        patience = config.patience

        hash_id = generate_hash(config, include_init=False)

        results = genetic_algorithm(population_size=population_size, dimension=dimension, 
                                    mating_pool_ratio=mating_pool_ratio, mutation_probability=mutation_probability,
                                    patience=patience, log_fn=wandb.log)

        wandb.log({
            "best_fitness": results["best_fitness"],
            "best_individual": results["best_individual"],
            "aes": results["aes"],
            "evaluations": results["evaluations"],
            "duplicate": False,
            "hash": hash_id
        })

        store_hash(config_hash)


    c = datetime.now()
    print('Finishing sweep at:', c)

def main():
    wandb.login()
    sweep_id = wandb.sweep(sweep_config, project="genetic-queens-mk1")

    # Determine the number of CPUs to use
    num_cpus = cpu_count()

    # Create a pool of workers
    with Pool(processes=num_cpus) as pool:
        pool.starmap(wandb.agent, [(sweep_id, optimize)] * num_cpus)

if __name__ == "__main__":
    main()
