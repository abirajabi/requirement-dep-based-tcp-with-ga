'''
    Author: Naufal Rajabi
    Reference: David T. Pocock

    tf = Test Case Fault
    tr = Test Requirement Fault 
    rdr = Requirement Dependency 
    irf = Internal Requirement Factor
'''

import csv
from gene import Gene


class CSVParser:

    
    def __init__(self, tf_path, tr_path, rdr_path, irf_path):
        self.tf_path = tf_path
        self.tr_path = tr_path
        self.rdr_path = rdr_path
        self.irf_path = irf_path

    # return type: List of Gene. Gene represent a single test case with metadata
    def parse_test_cases(self):
        rdw = self.parse_rdr_matrix()

        tr = []
        tf = []
        tc = []

        # test dependency weight
        tdw = []

        # internal requirement factor for each requirement
        irf = self.parse_internal_req_data()

        # internal requirement test case weight
        itw = []

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
                itw.append(self.calculate_irtw(requirements_covered, irf))

        tf_file.close()
        tr_file.close()

        for tf_item, tr_item, tdw_item, itw_item in zip(tf, tr, tdw, itw):
            tc.append(Gene(tf_item[0], tf_item[1], tr_item, tdw_item, itw_item))
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
        # print("RDW MATRIX", rdw)
        return rdw

    def calc_dep_weight(self, tr, rdw):
        tdw = 0
        for i in range(0, len(tr)):
            if tr[i] == 1:
                tdw += rdw[i]

        return tdw

    #  return a list of value internal requirement factor where
    #  IRF comes from summing requirement impact, complexity, and change
    def parse_internal_req_data(self):
        irf_list = []
        
        with open(self.irf_path, mode='r', encoding="utf-8-sig") as irf_file:
            irf_reader = csv.reader(irf_file)

            for row in irf_reader:
                irf_list.append(sum(map(float, row)))
        irf_file.close()

        return irf_list

    def calculate_irtw(self, covered_requirement, irf):
        irtw = 0
        for i in range(0, len(covered_requirement)):
            if covered_requirement[i] == 1:
                irtw += irf[i]

        return irtw
