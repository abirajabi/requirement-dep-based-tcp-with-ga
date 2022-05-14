class Gene:
    def __init__(self, tc_number, tf, tr):
        self.tc_number = tc_number
        self.tf = tf
        self.tr = tr

    #     self.n_covered_requirement = self.count_covered_requirement(tr)
    #     self.sum_req_dep = sum_req_dep

    # def count_covered_requirement(reqlist):
    #     return sum(1 for item in reqlist if item == 1)
