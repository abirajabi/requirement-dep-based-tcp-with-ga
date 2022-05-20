import random
from gene import Gene


class GeneticAlgorithm:

    def __init__(self, rdr_matrix, test_cases, pop_size, cr, mr):
        self.rdr_matrix = rdr_matrix
        self.test_cases = test_cases
        self.pop_size = pop_size
        self.cr = cr
        self.mr = mr

    def run():
        pop = self.generate_population()
        
        # calculate the fitness function
        # do the crossover --> make sure the chromosome is fiable
        # do the mutation

        # run NSGA
        # store APFD value to csv

        # calculate fitness value
        # if fitness value converged then stop GA

    def generate_population(self):
        population = []
        for i in range(0, self.pop_size):
            chromosome = []
            for j in range(0, len(self.test_cases)):
                self.populate(j, chromosome)

            population.append(chromosome)
        return population

    def populate(self, j, chromosome):
        random_index = random.randint(1, len(self.test_cases))

        # here chromosome is just an int
        chromosome.append(self.test_cases[random_index - 1])

        if j > 0:
            if self.is_duplicate_found(chromosome):
                chromosome.pop()
                self.populate(j, chromosome)

    @staticmethod
    def is_duplicate_found(chromosome):
        duplicate_checker = []
        for genes in chromosome:
            duplicate_checker.append(genes.tc_number)

        return len(duplicate_checker) != len(set(duplicate_checker))
