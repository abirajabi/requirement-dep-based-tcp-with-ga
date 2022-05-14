import random
from gene import Gene


class GeneticAlgorithm:

    def __init__(self, rdr_matrix, test_cases, pop_size, cr, mr):
        self.rdr_matrix = rdr_matrix
        self.test_cases = test_cases
        self.pop_size = pop_size
        self.cr = cr
        self.mr = mr

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
        chromosome.append(random_index)

        if j > 0:
            if self.is_duplicate_found(chromosome):
                chromosome.pop()
                self.populate(j, chromosome)

    def fitness(self, chromosome):
        weight = 0
        number_of_tc = len(chromosome)
        number_of_fault = len(chromosome[1])

    @staticmethod
    def is_duplicate_found(chromosome):
        duplicate_checker = []
        for genes in chromosome:
            duplicate_checker.append(genes.tc_number)

        return len(duplicate_checker) != len(set(duplicate_checker))
