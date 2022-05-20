'''
    Requirement Dependency Based TCP with Genetic Algorithm
    Author: Naufal Rajabi
    Reference: https://github.com/dathpo/test-case-prioritisation-ga
'''

from csv_parser import CSVParser
from genetic import GeneticAlgorithm


def main():
    # load and parse the three matrix
    parser = CSVParser(
        tf_path="./case_study_generated/CS1/tf.csv",
        tr_path="./case_study_generated/CS1/tr.csv",
        rdr_path="./case_study_generated/CS1/rdr.csv"
    )

    # parse rdr matrix first to fill rdw
    parser.parse_rdr_matrix()
    test_cases = parser.parse_test_cases()

    # construct a population of test cases order permuatation
    # ga = GeneticAlgorithm(rdr, test_cases, 100, 0, 0)
    # ga.run()


if __name__ == "__main__":
    main()
