'''
    Requirement Dependency Based TCP with Genetic Algorithm
    Author: Naufal Rajabi
    Reference: 
        1. TCP: https://github.com/dathpo/test-case-prioritisation-ga
        2. NSGA-II: https://github.com/baopng/NSGA-II
'''
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

from csv_parser import CSVParser
from genetic import GeneticAlgorithm


def main():
    # method = "WEIGHTED"
    # method = "BINARY"
    sut = "CS2"

    # load and parse the three matrix
    parser = CSVParser(
        tf_path="./casestudy/" + sut + "/tf.csv",
        tr_path="./casestudy/" + sut + "/tr.csv",
        rdr_path="./casestudy/" + sut + "/rdr_ami.csv"
    )

    # parse rdr matrix first to fill rdw
    test_cases = parser.parse_test_cases()
    # construct a population of test cases order permutation
    ga = GeneticAlgorithm(test_cases)

    # return pareto optimal solution
    non_dominated_tcp_solutions = ga.run()

    total_apfd, total_dcr = 0, 0

    max_apfd, max_dcr = 0, 0
    for individual in non_dominated_tcp_solutions:
        total_apfd += individual.objectives[0]
        total_dcr += individual.objectives[1]

        if (individual.objectives[0] > max_apfd):
            max_apfd = individual.objectives[0]
        
        if (individual.objectives[1] > max_dcr):
            max_dcr = individual.objectives[1]
        
        # pop_data.append(
        #     (individual.objectives[0], individual.objectives[1], method, sut, [tc.tc_number for tc in individual.chromosome]))

    print(total_apfd/len(non_dominated_tcp_solutions),
          total_dcr/len(non_dominated_tcp_solutions), max_apfd, max_dcr)

    # columns = ["APFD", "DCR", "METHOD", "SUT", "TEST_SET"]
    # pareto_df = pd.DataFrame(data=pop_data, columns=columns)
    # pareto_df.to_csv('demo.csv', mode='a', index=False, header=False)
    # print(pareto_df.head())

    # sns.scatterplot(data=pareto_df, x="DCR", y="APFD")
    # plt.show()


if __name__ == "__main__":
    main()
