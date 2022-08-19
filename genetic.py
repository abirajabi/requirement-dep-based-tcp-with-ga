'''
    Author: Naufal Rajabi
'''

import random
import copy
from individual import Individual
from population import Population
from gene import Gene
from itertools import chain


class GeneticAlgorithm:

    def __init__(self, test_cases, pop_size=100, crossover_rate=0.95, mutation_rate=0.01, number_of_generation=100, tournament_prob=0.9):
        self.test_cases = test_cases
        # self.rdw = rdw
        self.population = None
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.number_of_generation = number_of_generation
        self.tournament_prob = tournament_prob
        self.chromosome_size = self.get_chromosome_size()

    def get_chromosome_size(self):
        return len(self.test_cases)

    def run(self):
        # print("CREATING INITAL POPULATION")
        self.population = self.create_initial_population()

        # print("BEGIN SORT")
        self.fast_nondominated_sort(self.population)
        
        # print("DONE SORTING, CALCULATING CROWDING DISTNANCE")
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)
        children = self.create_children(self.population)

        returned_population = None
        for i in range(self.number_of_generation):
            print("GENERATION NUMBER ", i + 1)
            self.population.extend(children)
            self.fast_nondominated_sort(self.population)
            new_population = Population()

            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.pop_size:
                self.calculate_crowding_distance(
                    self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            self.calculate_crowding_distance(
                self.population.fronts[front_num])
            self.population.fronts[front_num].sort(
                key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(
                self.population.fronts[front_num][0:self.pop_size-len(new_population)])
            returned_population = self.population

            self.population = new_population
            self.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.calculate_crowding_distance(front)
            children = self.create_children(self.population)

        return returned_population.fronts[0]

    def create_initial_population(self):
        population = Population()
        for i in range(0, self.pop_size):
            # print("CREATING CHROMOSOME: ", i)
            chromosome = []

            while (len(chromosome) != self.chromosome_size):
                self.populate(chromosome)

            individual = Individual(chromosome)
            individual.calculate_fitness()
            population.append(individual)
        return population

    def populate(self, chromosome):
        random_index = random.randint(1, len(self.test_cases))

        if not self.check_duplicate(self.test_cases[random_index - 1], chromosome):
            chromosome.append(self.test_cases[random_index - 1])

    def check_duplicate(self, new_tc, chromosome):
        if new_tc in chromosome:
            return True
        return False

    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.rank = None
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1

            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)

        i = 0
        while len(population.fronts[i]) > 0:
            # print("FRONT LENGTH ", i, len(population.fronts[i]))
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])

                front[0].crowding_distance = 10**9
                front[solutions_num - 1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0:
                    scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (
                        front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def get_crossover_point(self):
        return random.randint(0, self.chromosome_size)

    def get_two_sorted_crossover_point(self):
        crossover_point1 = self.get_crossover_point()
        crossover_point2 = crossover_point1
        while crossover_point1 == crossover_point2:
            crossover_point2 = self.get_crossover_point()

        point = [crossover_point1, crossover_point2]
        point.sort()
        return point[0], point[1]

    def choose_with_prob(self, prob):
        value = random.random()
        return value < prob

    def create_children(self, population):
        children = []

        while len(children) < len(population):
            # get parents candidate for crossvoer
            parents_candidate = []
            parent1 = self.tournament_selection(population)
            parent2 = parent1

            while parent1 == parent2:
                parent2 = self.tournament_selection(population)

            parents_candidate.append(parent1)
            parents_candidate.append(parent2)

            pre_mutation_generation = self.check_for_crossover(
                parents_candidate)
            new_generation = self.mutate(pre_mutation_generation)
            children.extend(new_generation)

        return children

    # return type: Individual
    def tournament_selection(self, population):
        # number of tournament participants equals to 2
        participants = random.sample(population.population, 2)
        best = None

        for partipant in participants:
            if best is None or (self.crowding_operator(partipant, best) == 1 and self.choose_with_prob(self.tournament_prob)):
                best = partipant

        return best

    def two_point_crossover(self, individual1, individual2):
        start, end = self.get_two_sorted_crossover_point()

        #  preserved gene
        preserved1 = individual1.chromosome[start:end+1]
        preserved2 = individual2.chromosome[start:end+1]
        # print("PRESERVED1: ", [tc.tc_number for tc in preserved1])
        # print("PRESERVED2: ", [tc.tc_number for tc in preserved2])

        # take element from other parent that is not in preserved gene
        offspring_set1 = [
            gene for gene in individual2.chromosome if not gene in preserved1]
        offspring_set2 = [
            gene for gene in individual1.chromosome if not gene in preserved2]

        preserved1.reverse()
        preserved2.reverse()

        for gene1, gene2 in zip(preserved1, preserved2):
            offspring_set1.insert(start, gene1)
            offspring_set2.insert(start, gene2)

        # print("OFFSPEING1: ", [tc.tc_number for tc in offspring_set1])
        # print("OFFSPRING2: ", [tc.tc_number for tc in offspring_set2])

        new_individual1 = Individual(offspring_set1)
        new_individual1.calculate_fitness()
        new_individual2 = Individual(offspring_set2)
        new_individual2.calculate_fitness()

        return new_individual1, new_individual2

    def crossover(self, individual1, individual2):
        # do single point crossover
        first_child_test_case_set = []
        second_child_test_case_set = []

        crossover_point = self.get_crossover_point()
        first_parent_copy = individual1.chromosome.copy()
        second_parent_copy = individual2.chromosome.copy()

        i = 0
        for test_case_a, test_case_b in zip(individual1.chromosome, individual2.chromosome):
            i += 1
            if i <= crossover_point:
                first_child_test_case_set.append(test_case_a)
                if test_case_b in first_parent_copy:
                    first_parent_copy.remove(test_case_b)
                else:
                    first_parent_copy.pop()
                second_child_test_case_set.append(test_case_b)
                if test_case_a in second_parent_copy:
                    second_parent_copy.remove(test_case_a)
                else:
                    second_parent_copy.pop()
            else:
                first_child_test_case_set.extend(second_parent_copy)
                second_child_test_case_set.extend(first_parent_copy)
                break

        new_individual1 = Individual(first_child_test_case_set)
        new_individual1.calculate_fitness()
        new_individual2 = Individual(second_child_test_case_set)
        new_individual2.calculate_fitness()

        return new_individual1, new_individual2

    def check_for_crossover(self, parents_candidate):
        new_generation = []

        if self.choose_with_prob(self.crossover_rate):
            # children_duo = self.crossover(
            #     parents_candidate[0], parents_candidate[1])
            children_duo = self.two_point_crossover(
                parents_candidate[0], parents_candidate[1])

            for child in children_duo:
                new_generation.append(child)
        else:
            ind1 = Individual(parents_candidate[0].chromosome)
            ind1.calculate_fitness()
            ind2 = Individual(parents_candidate[1].chromosome)
            ind2.calculate_fitness()

            new_generation.append(ind1)
            new_generation.append(ind2)
        return new_generation

    def swap_test_cases(self, test_case_index):
        random_index = random.randint(0, self.chromosome_size - 1)
        if random_index is not test_case_index:
            return random_index
        else:
            return self.swap_test_cases(test_case_index)

    def mutate(self, generation):
        new_generation = []
        for individual in generation:
            for test_case in individual.chromosome:
                if self.choose_with_prob(self.mutation_rate):
                    current_index = individual.chromosome.index(test_case)
                    random_index = self.swap_test_cases(current_index)
                    individual.chromosome[current_index], individual.chromosome[
                        random_index] = individual.chromosome[random_index], individual.chromosome[current_index]
            new_generation.append(individual)
        return new_generation
