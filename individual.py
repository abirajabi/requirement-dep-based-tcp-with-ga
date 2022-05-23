'''
    Individual is a chromosome that contains a set of gene, with its metadata
'''


class Individual:
    def __init__(self, genes):
        # TCP related
        self.chromosome = genes
        self.apfd_score = 0
        self.req_dep_score = 0

        # NSGA related
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        # self.features = None
        # self.objectives = None

    def calculate_fitness(self, chromosome, rdw):
        self.apfd_score = self.calculate_apfd(chromosome)
        self.req_dep_score = self.calculate_req_dep(chromosome, rdw)

    # calculate the apfd as objective function of an individual

    def calculate_apfd(self, chromosome):
        weight = 0
        number_of_test_cases_in_set = len(chromosome)
        number_of_faults = len(chromosome[0].tf)

        for i in range(0, number_of_faults):
            for j in range(0, number_of_test_cases_in_set):
                # if test case(j) found the fault(i)
                if chromosome[j].tf[i]:
                    weight += j + 1
                    break

                if j == len(self.chromosome) - 1:
                    weight += number_of_test_cases_in_set + 1

        apfd = 1 - (weight / (number_of_faults * number_of_test_cases_in_set)
                    ) + 1 / (2 * number_of_test_cases_in_set)
        return apfd

    # calculate the requirement dependency score as objective function of an individual
    def calculate_req_dep(self, chromosome, rdw):
        # calculate dependency coverage rate by
        dcr = 0

        number_of_test_cases_in_set = len(chromosome)
        number_of_test_cases_conducted = 0

        for i in range(0, number_of_test_cases_in_set):
            auc = 0
            if i == 0:
                auc = chromosome[i].dw/2
            else:
                w = 0
                auc += chromosome[i].dw/2
                for j in range(0, i):
                    w += chromosome[j].dw
                auc += w
            dcr += auc

        return dcr

        # for i in range(0, number_of_test_cases_in_set):
        #     number_of_test_cases_conducted += 1
        #     for j in range(0, number_of_test_cases_conducted):
        #         weight += chromosome[j].dw / number_of_test_cases_conducted
        # return weight/number_of_test_cases_in_set

    # dominates by maximization
    def dominates(self, other_individual):
        my_fitness = (self.apfd_score, self.req_dep_score)
        other_fitness = (other_individual.apfd_score,
                         other_individual.req_dep_score)

        and_condition = True
        or_condition = False

        for mine, others in zip(my_fitness, other_fitness):
            and_condition = and_condition and mine >= others
            or_condition = or_condition or mine > others

        return (and_condition and or_condition)
