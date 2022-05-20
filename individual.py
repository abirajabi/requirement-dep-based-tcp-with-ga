'''
    Individual is a chromosome that contains a set of gene, with its metadata
'''


class Individual:
    def __init__(self, genes):
        self.chromosome = genes
        self.apfd_score = self.calculate_apfd(genes)
        self.req_dep_score = self.calculate_req_dep(genes)

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

                if j == len(self.chromosome - 1):
                    weight += number_of_test_cases_in_set + 1

        apfd = 1 - (weight / (number_of_faults * number_of_test_cases_in_set)
                    ) + 1 / (2 * number_of_test_cases_in_set)
        self.apfd_score = apfd

    # calculate the requirement dependency score as objective function of an individual
    def calculate_req_dep(self, chromosome):
        sum = 0
        number_of_test_cases_in_set = len(chromosome)
        number_of_requirements = len(chromosome[0].tr)

        for i in range(0, number_of_requirements):
            for j in range(0, number_of_test_cases_in_set):
                sum += chromosome[j].tr[i]

        self.req_dep_score = sum
