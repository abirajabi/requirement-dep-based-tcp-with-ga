'''
    Gene is a single test case representation in GA problem.
    Test case can find several fault and cover several requirement.
    Gene contains test case number, fault coverage matrix,
    requirement coverage matrix, test case dependency weight.

    Test case depenency weight (dw) is calculated by iterating the TR matrix 
    and assigning the dependency weight from RDR matrix.
'''

class Gene:
    def __init__(self, tc_number, tf, tr, dw):
        self.tc_number = tc_number
        self.tf = tf
        self.tr = tr
        self.dw = dw

    #     self.n_covered_requirement = self.count_covered_requirement(tr)
    #     self.sum_req_dep = sum_req_dep

    # def count_covered_requirement(reqlist):
    #     return sum(1 for item in reqlist if item == 1)
