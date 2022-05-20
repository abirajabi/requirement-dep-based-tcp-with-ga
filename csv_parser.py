import csv

from gene import Gene


class CSVParser:

    def __init__(self, tf_path, tr_path, rdr_path):
        self.tf_path = tf_path
        self.tr_path = tr_path
        self.rdr_path = rdr_path
        self.rdw = []

    def parse_test_cases(self):
        tr = []
        tf = []
        tc = []
        dw = []

        with open(self.tf_path, mode='r', encoding="utf-8-sig") as tf_file:
            tf_reader = csv.reader(tf_file)

            for row in tf_reader:
                faults_covered = []
                for column in row:
                    val = int(column)
                    faults_covered.append(val)

                tf.append((tf_reader.line_num, faults_covered))

        with open(self.tr_path, mode='r', encoding="utf-8-sig") as tr_file:
            tr_reader = csv.reader(tr_file)

            for row in tr_reader:
                requirements_covered = []
                for column in row:
                    val = int(column)
                    requirements_covered.append(val)

                tr.append(requirements_covered)
                dw.append(self.calc_dep_weight(requirements_covered))

        for tf_item, tr_item, dw_item in zip(tf, tr, dw):
            tc.append(Gene(tf_item[0], tf_item[1], tr_item, dw_item))
        return tc

    def parse_rdr_matrix(self):
        requirements = []
        with open(self.rdr_path, mode='r', encoding="utf-8-sig") as rdr_file:

            csv_reader = csv.reader(rdr_file)
            for row in csv_reader:
                req_depend = []

                for column in row:
                    val = float(column)
                    req_depend.append(val)
                requirements.append((csv_reader.line_num, req_depend))
        rdr_file.close()

        for item in requirements:
            self.rdw.append(sum(item[1]))

    def calc_dep_weight(self, tr):
        tdw = 0
        for i in range(0, len(tr)):
            if tr[i] == 1:
                tdw += self.rdw[i]

        return tdw
