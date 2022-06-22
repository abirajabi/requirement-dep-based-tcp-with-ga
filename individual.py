'''
    Author: Naufal Rajabi
    Individual is a chromosome that contains a set of gene, with its metadata
'''


class Individual:
    def __init__(self, genes):
        # TCP related
        self.chromosome = genes

        # NSGA related
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.objectives = []

    def calculate_fitness(self):
        self.objectives.append(self.calculate_apfd())
        self.objectives.append(self.calculate_req_dep())

    # calculate the apfd as objective function of an individual
    def calculate_apfd(self):
        weight = 0
        number_of_test_cases_in_set = len(self.chromosome)
        number_of_faults = len(self.chromosome[0].tf)

        for i in range(0, number_of_faults):
            for j in range(0, number_of_test_cases_in_set):
                # if test case(j) found the fault(i)
                if self.chromosome[j].tf[i]:
                    weight += j + 1
                    break

                if j == len(self.chromosome) - 1:
                    weight += number_of_test_cases_in_set + 1

        apfd = 1 - (weight / (number_of_faults * number_of_test_cases_in_set)
                    ) + 1 / (2 * number_of_test_cases_in_set)
        return apfd

    #  Dependency coverage rate (DCR)
    #  calculate the DCR as objective function of an individual
    def calculate_req_dep(self):
        dcr = 0
        total_tdw = 0
        for tc in self.chromosome:
            total_tdw += tc.dw

        number_of_test_cases_in_set = len(self.chromosome)

        for i in range(0, number_of_test_cases_in_set):
            auc = 0
            if i == 0:
                auc = self.chromosome[i].dw/2
            else:
                w = 0
                auc += self.chromosome[i].dw/2
                for j in range(0, i):
                    w += self.chromosome[j].dw
                auc += w
            dcr += auc
        print("TEST CASE SET", [i.tc_number for i in self.chromosome])
        print("TOTAL TDW = ", total_tdw)
        return dcr / (number_of_test_cases_in_set * total_tdw)

    # dominates by maximization of the 2 objectives function
    def dominates(self, other_individual):
        and_condition = True
        or_condition = False

        for mine, others in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and mine >= others
            or_condition = or_condition or mine > others

        return (and_condition and or_condition)
