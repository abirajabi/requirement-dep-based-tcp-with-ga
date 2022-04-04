'''

    Author: Naufal Rajabi

    Purpose: Parse RD-TCP input matrices


    Desc:

    This class should be able to parse 3 different matrices from CSV to python 

    data type.

    - RDR, requirement dependency matrix

    - TF, test case and fault traceability matrix

    - TR, test cae and requirement traceability matrix
'''


import csv


class CSVParser:

    def parse_rdr_matrix(self, path):
        '''Parse RDR matrix from CSV to an array of tuple
            params: path (String) to an RDR matrix file
            return type: array of tuple
            e.g. --> [
                ('r1', [0, 0, 0.352, 0.085, 0, 0]),
                ('r2', [0.066, 0, 0, 0.146, 0, 0]),
            ]
        '''

        # TODO : add try catch mechanism

        requirements = []
        with open(path, mode='r') as file:

            csv_reader = csv.reader(file, )
            for row in csv_reader:
                req_depend = []

                for column in row[1:]:
                    val = float(column)
                    req_depend.append(val)
                requirements.append((row[0], req_depend))
        file.close()
        return requirements

    def parse_test_cases(self, tr_path, tf_path):
        test_cases = []

        with open(tr_path, mode='r') as tr_file, open(tf_path, mode='r') as tf_file:
            tr_reader = csv.reader(tr_file)
            tf_reader = csv.reader(tf_file)

            for row in tr_reader:
                faults_covered = []
                requirements_covered = []
                for column in row[1:]:
                    val = int(column)
                    requirements_covered.append(val)

                for column in list(tf_file)[tr_reader.line_num - 1]:
                    val = int(column)
                    faults_covered.append(val)

                test_cases.append(
                    (row[0], requirements_covered, faults_covered))

            return test_cases
