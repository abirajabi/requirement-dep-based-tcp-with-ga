'''
    Requirement Dependency Based TCP with Genetic Algorithm
    Author: Naufal Rajabi
    Reference: 
        1. TCP: https://github.com/dathpo/test-case-prioritisation-ga
        2. NSGA-II: https://github.com/baopng/NSGA-II
'''

from csv_parser import CSVParser
from genetic import GeneticAlgorithm


def calculate_aprc(test_case_set):
    weight = 0
    number_of_test_cases_in_set = len(test_case_set)
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

def main():
    # load and parse the three matrix
    parser = CSVParser(
        tf_path="./case_study_generated/CS1/tf.csv",
        tr_path="./case_study_generated/CS1/tr.csv",
        rdr_path="./case_study_generated/CS1/rdr.csv"
    )

    # parse rdr matrix first to fill rdw
    rdw = parser.parse_rdr_matrix()
    test_cases = parser.parse_test_cases(rdw)

    # construct a population of test cases order permuatation
    ga = GeneticAlgorithm(test_cases, rdw, pop_size=100, mutation_rate=0.1)

    # return pareto front
    non_dominated_tcp_solutions = ga.run()
    print("Berhasil dapet front")

    # Average Precentage of Requirement Covered (APRC)
    # hitung APRC untuk setiap individu pada pareto front
    # rata-ratakan ARPC
    # visualisasi dengan BoxPlot
    # uji signifkansi

    # calculate APRC, put into a list
    # average APRC value

if __name__ == "__main__":
    main()
