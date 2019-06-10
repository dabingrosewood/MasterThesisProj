import sys, os, re
import numpy as np


class PARAMETERS_EXTRACTOR:
    def __init__(self, dir,problem_set):
        self.target_dir = dir
        self.problem_set=problem_set

    def output_analyzer(self,f):
        recorder = [] #lv1
        tuning_data_for_one_system = () #lv2
        data_for_one_problem = [] #lv3
        problem_index=0
        for line in f.readlines():

            # find the system name to categorized all log.
            if re.search(r'now testing ([A-Za-z0-9]*) system', line):
                system_name = re.search(r'now testing ([A-Za-z0-9]*) system', line).group(1)

                if len(tuning_data_for_one_system) != 0:
                    # in the case of it already have data, which mean we encounter another system. Finish the data from previous one and rebuild new data list.
                    tuning_data_for_one_system[1].append(data_for_one_problem)
                    recorder.append(tuning_data_for_one_system)
                    tuning_data_for_one_system = (system_name, [])
                else:
                    tuning_data_for_one_system = (system_name, [])

            # catch stat of each iteration of hyper-parameter tuning
            if re.search(r'iteration ([0-9]*), objective value:\s(\d+(\.\d+)?)', line):
                cur_iteration_num = int(re.search(r'iteration ([0-9]*), objective value:\s(\d+(\.\d+)?)',
                                              line).group(1))
                cur_fitness_value = float(re.search(r'iteration ([0-9]*), objective value:\s(\d+(\.\d+)?)',
                                              line).group(2))

                if len(data_for_one_problem)==0:
                    #in the case of the lv3 list is empty, input the name of problem and the first group of data
                    data_for_one_problem.append(self.problem_set[problem_index])
                    problem_index+=1
                    data_for_one_problem.append([cur_iteration_num, cur_fitness_value])

                elif data_for_one_problem[-1][0] < cur_iteration_num:
                    #for most
                    data_for_one_problem.append([cur_iteration_num, cur_fitness_value])
                elif data_for_one_problem[-1][0] > cur_iteration_num:
                    tuning_data_for_one_system[1].append(data_for_one_problem) #end the previous problem
                    data_for_one_problem=[self.problem_set[problem_index]]
                    problem_index+=1
                    if problem_index==len(self.problem_set):
                        problem_index=0
                    data_for_one_problem.append([cur_iteration_num, cur_fitness_value])

        tuning_data_for_one_system[1].append(data_for_one_problem)
        recorder.append(tuning_data_for_one_system)
        print(recorder,'\n')


    def run(self):
        files = os.listdir(self.target_dir)
        for file in files:
            with open(os.path.join(os.getcwd(), self.target_dir, file)) as f:

                if file.startswith('output'):
                # This file is standard output of test (nohup command)
                    print('current file is ',file)
                    self.output_analyzer(f)
                else:
                    pass


if __name__ == "__main__":
    defaultz_log_dir = "../log/"
    problem_set=['mux11','ant','string_match']

    extractor = PARAMETERS_EXTRACTOR(defaultz_log_dir,problem_set)
    extractor.run()