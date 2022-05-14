'''
    Requirement Dependency Based TCP with Genetic Algorithm
    Author: Naufal Rajabi
    Reference: https://github.com/dathpo/test-case-prioritisation-ga
'''

from csv_parser import CSVParser
from genetic import GeneticAlgorithm

def main():
    # load and parse the three matrix

    parser = CSVParser()
    rdr = parser.parse_rdr_matrix("./case_study_generated/CS1/rdr.csv")
    test_cases = parser.parse_test_cases(
        tf_path="./case_study_generated/CS1/tf.csv", tr_path="./case_study_generated/CS1/tr.csv")

    for i in range(len(test_cases)):
        print(test_cases[i].tc_number)

    # construct a population of test cases order permuatation
    # ga = GeneticAlgorithm(rdr, test_cases, 100, 0, 0)
    # population = ga.generate_population()
    # print(population)

    # do the crossover --> make sure the chromosome is fiable
    # do the mutation
    # calculate fitness value
    # if fitness value converged then stop GA

if __name__ == "__main__":
    main()