import csv

from gene import Gene


class CSVParser:
    def parse_rdr_matrix(self, path):
        requirements = []
        with open(path, mode='r', encoding="utf-8-sig") as rdr_file:

            csv_reader = csv.reader(rdr_file)
            for row in csv_reader:
                req_depend = []

                for column in row:
                    val = float(column)
                    req_depend.append(val)
                requirements.append((csv_reader.line_num, req_depend))
        rdr_file.close()
        return requirements

    def parse_test_cases(self, tf_path, tr_path):
        tr = []
        tf = []
        tc = []

        with open(tf_path, mode='r', encoding="utf-8-sig") as tf_file:
            tf_reader = csv.reader(tf_file)

            for row in tf_reader:
                faults_covered = []
                for column in row:
                    val = int(column)
                    faults_covered.append(val)

                tf.append((tf_reader.line_num, faults_covered))

        with open(tr_path, mode='r', encoding="utf-8-sig") as tr_file:
            tr_reader = csv.reader(tr_file)

            for row in tr_reader:
                requirements_covered = []
                for column in row:
                    val = int(column)
                    requirements_covered.append(val)

                tr.append((tr_reader.line_num, requirements_covered))

        for tf_item, tr_item in zip(tf, tr):
            tc.append(Gene(tf_item[0], tf_item[1], tr_item[1]))
        return tc
