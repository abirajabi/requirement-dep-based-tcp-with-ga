'''
    Author: Naufal Rajabi
    Reference: David T. Pocock
'''

import csv
from gene import Gene


class CSVParser:

    def __init__(self, tf_path, tr_path, rdr_path):
        self.tf_path = tf_path
        self.tr_path = tr_path
        self.rdr_path = rdr_path

    # return type: List of Gene. Gene represent a single test case with metadata
    def parse_test_cases(self, rdw):
        tr = []
        tf = []
        tc = []
        tdw = []

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
                tdw.append(self.calc_dep_weight(requirements_covered, rdw))

        for tf_item, tr_item, tdw_item in zip(tf, tr, tdw):
            tc.append(Gene(tf_item[0], tf_item[1], tr_item, tdw_item))
        return tc

    # return type: List of double, containing dependency weight that owned
    # for a certain requirement
    def parse_rdr_matrix(self):
        requirements = []
        rdw = []

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
            rdw.append(sum(item[1]))
        print("RDW MATRIX", rdw)
        return rdw

    def calc_dep_weight(self, tr, rdw):
        tdw = 0
        for i in range(0, len(tr)):
            if tr[i] == 1:
                tdw += rdw[i]

        return tdw
