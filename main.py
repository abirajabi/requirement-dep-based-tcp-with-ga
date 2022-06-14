'''
    Requirement Dependency Based TCP with Genetic Algorithm
    Author: Naufal Rajabi
    Reference: 
        1. TCP: https://github.com/dathpo/test-case-prioritisation-ga
        2. NSGA-II: https://github.com/baopng/NSGA-II
'''
import pandas as pd
import matplotlib.pyplot as plt

from csv_parser import CSVParser
from genetic import GeneticAlgorithm


def calculate_aprc(individual):
    weight = 0
    number_of_test_cases_in_set = len(individual.chromosome)
    number_of_requirement = len(individual.chromosome[0].tr)

    for i in range(0, number_of_requirement):
        for j in range(0, number_of_test_cases_in_set):
            if individual.chromosome[j].tr[i]:
                weight += j + 1
                break

            if j == len(individual.chromosome) - 1:
                weight += number_of_test_cases_in_set + 1

    return 1 - (weight / (number_of_requirement * number_of_test_cases_in_set)
                ) + 1 / (2 * number_of_test_cases_in_set)


def main():
    # load and parse the three matrix
    parser = CSVParser(
        tf_path="./casestudy/iTrust/tf.csv",
        tr_path="./casestudy/iTrust/tr.csv",
        # rdr_path="./casestudy/iTrust/rdr.csv"
        rdr_path="./casestudy/iTrust/rdr_weight.csv"
    )

    # parse rdr matrix first to fill rdw
    rdw = parser.parse_rdr_matrix()
    test_cases = parser.parse_test_cases(rdw)

    # construct a population of test cases order permutation
    ga = GeneticAlgorithm(test_cases, rdw, number_of_generation=10)

    # return pareto optimal solution
    non_dominated_tcp_solutions = ga.run()

    pop_data = []
    method = "WEIGHTED"
    # method = "BINARY"
    sut = "iTrust"

    for individual in non_dominated_tcp_solutions:
        aprc = calculate_aprc(individual)
        pop_data.append(
            (individual.objectives[0], individual.objectives[1], aprc, method, sut, [tc.tc_number for tc in individual.chromosome]))

    # columns=["APFD", "DCR", "METHOD", "SUT", "TEST_SET"]
    pareto_df = pd.DataFrame(data=pop_data, columns=[
                             "APFD", "DCR", "APRC", "METHOD", "SUT", "TEST_SET"])
    pareto_df.to_csv('test.csv', mode='a', index=False, header=False)
    # print(pareto_df.head())

    # print("POPULATION LENGTH", len(ga.population))
    # print("OPTIMAL FRONT LENGTH", len(non_dominated_tcp_solutions))
    # sns.scatterplot(data=pareto_df, x="DCR", y="APFD")
    # plt.show()

    # Average Precentage of Requirement Covered (APRC)
    # calculate APRD for each individual on pareto optimal solution
    # rata-ratakan ARPC
    # visualisasi dengan BoxPlot
    # uji signifkansi

    # calculate APRC, put into a list
    # average APRC value


if __name__ == "__main__":
    main()
