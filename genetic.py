import random
from individual import Individual
from population import Population
from gene import Gene


class GeneticAlgorithm:

    def __init__(self, test_cases, rdw, pop_size=100, cr=0.9, mr=0.01, number_of_generation=1000, tournament_prob=0.9):
        self.test_cases = test_cases
        self.rdw = rdw
        self.pop_size = pop_size
        self.cr = cr
        self.mr = mr
        self.number_of_generation = number_of_generation

    def run(self):
        # generate pop and init each individual with objective function score
        pop = self.create_initial_population()
        generation_number = 0

        for i in range(0, len(pop)):
            print(i + 1)
            print(pop.population[i].apfd_score)
            print(pop.population[i].req_dep_score)

        # iterate as many as number_of_generation
        # for i in range(0, self.number_of_generation):
        #     generation_number += 1

            # do fast non-dominated sorting

            # do tournament selection

        # do the crossover --> make sure the chromosome is fiable
        # do the mutation

        # run NSGA
        # store APFD value to csv

        # calculate fitness value
        # if fitness value converged then stop GA

    def create_initial_population(self):
        population = Population()
        for i in range(0, self.pop_size):
            chromosome = []
            for j in range(0, len(self.test_cases)):
                self.populate(j, chromosome)

            individual = Individual(chromosome)
            individual.calculate_fitness(chromosome, self.rdw)
            population.append(individual)
        return population

    def populate(self, j, chromosome):
        random_index = random.randint(1, len(self.test_cases))

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

    @staticmethod
    def crossover_point():
        value = random.random()
        return value

    def fast_nondominated_sort(self, population):
        population_fronts = [[]]
        for individual in population:
            individual.dmo
