import sys, os, re
import numpy as np
import json
import csv
import matplotlib.pyplot as plt
import pandas as pd

class PARAMETERS_EXTRACTOR:
    '''
    This class is used to extract and analyze data from log files, which are generated by management.py

    '''

    def __init__(self, dir, problem_set, para_dir='../util/hyper_para_list_PonyGE2.json'):
        self.target_dir = dir
        self.problem_set = problem_set
        self.para_dir = para_dir

    def getpara(self, system_name):
        '''
        This funciton is used to extract the name of tuned HYPER_PARAMETER in the test, by reading the json file which control hyper-parameters in.
        :param system_name:
        :return:
        '''
        llist = []

        # todo: this part need modicication (systemname need to be uniformed)
        if system_name == 'ponyge2':
            para_file = '../util/hyper_para_list_PonyGE2.json'
            llist.append('PROBLEM')
            llist.append('EVAL_BUDGET')
        elif system_name == 'SGE':
            para_file = '../util/hyper_para_list_SGE.json'

        with open(para_file, 'r') as load_f:
            data = json.load(load_f)
            for parameter in data:
                if parameter['name']:
                    llist.append(parameter['name'])

        if system_name == 'SGE':
            llist.append('EVAL_BUDGET')
            llist.append('PROBLEM')
            # llist.append('NUMBER_OF_ITERATIONS')

        return llist

    def output_analyzer(self, f):
        '''
        This funciton extract data from std_out of test.
        Due to the fact i use the command like ' nohup python3 management.py >log/output_node112_3.txt 2>&1 &', std_out
        are stored in those files with the name of 'output_MACHINE_NAME_IDNEX.txt'

        :param f:
        :return: A List with following structure:[level1,level1,[...]]
            Level1:(SYSTEM_NAME,[level2],[level2],[...])
            Level2:[PROBLEM_NAME,[level3],[level3],[...]]
            Level3:[[Iteration_number,Fitness_value],[Iteration_number,Fitness_value],[...]]

        '''
        recorder = []  # lv1
        tuning_data_for_one_system = ()  # lv2
        data_for_one_problem = []  # lv3
        problem_index = 0
        for line in f.readlines():

            # find the system name to categorized all log.
            if re.search(r'now testing ([A-Za-z0-9]*) system', line):
                system_name = re.search(r'now testing ([A-Za-z0-9]*) system', line).group(1)

                if len(tuning_data_for_one_system) != 0:
                    # in the case of it already have data, which mean we encounter another system. Finish the data from previous one and rebuild new data list.
                    tuning_data_for_one_system[1].append(data_for_one_problem)
                    data_for_one_problem = []  # need to clear all used data
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

                if len(data_for_one_problem) == 0:
                    # in the case of the lv3 list is empty, input the name of problem and the first group of data
                    data_for_one_problem = [self.problem_set[problem_index], []]
                    problem_index += 1
                    data_for_one_problem[1].append([cur_iteration_num, cur_fitness_value])

                elif data_for_one_problem[1][-1][0] < cur_iteration_num:
                    # for most
                    data_for_one_problem[1].append([cur_iteration_num, cur_fitness_value])
                elif data_for_one_problem[1][-1][0] > cur_iteration_num:
                    tuning_data_for_one_system[1].append(data_for_one_problem)  # end the previous problem
                    data_for_one_problem = [self.problem_set[problem_index], []]
                    problem_index += 1
                    if problem_index == len(self.problem_set):
                        problem_index = 0
                    data_for_one_problem[1].append([cur_iteration_num, cur_fitness_value])

        tuning_data_for_one_system[1].append(data_for_one_problem)
        recorder.append(tuning_data_for_one_system)
        return recorder

    def out_analyzer(self, system_name, f):
        '''
        In the benchmark test, for every problem the system will store its best-founded hyper-parameters settings, under
        the name of out_SYSTEMNAME_PROBLEM_TIME_MACHINENAME.txt
        This funciton is used to extract the best founded hyper-parameter setting stored in one file f.
        A dict includes the parameter_name and it's value will be returned.
        :param system_name:
        :param f:
        :return:
        '''
        while 1:
            line = f.readline()
            if not line:
                break
            if line.startswith("xopt"):
                tmp = line.strip("xopt: [").replace(']\n', '\n').replace("'", "").replace(" ", "")
                parameter_dict = dict(zip(self.getpara(system_name), tmp.split(',')))

        return parameter_dict

    def csv_writer(self, data):
        '''
        This function is used to write data into csv file for further usage.
        :param data:
        :return:
        '''
        if not os.path.exists('tmp'):
            os.mkdir('tmp/')
        for system in data:
            # print(system[0]) #system[0] is system name
            for problem in system[1]:
                data_to_write = []
                for element in problem[1]:
                    data_to_write.append(element[1])

                with open('tmp/'+system[0] + '_' + problem[0] + '.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file, dialect='excel')
                    writer.writerow(data_to_write)

    def run(self):
        '''
        main funciton of class PARAMETERS_EXTRACTOR
        all other fucntions are called here.
        :return:
        '''
        files = os.listdir(self.target_dir)
        for file in files:
            with open(os.path.join(os.getcwd(), self.target_dir, file)) as f:

                if file.startswith('output'):
                    # This file is standard output of test (nohup command), extract all data and store them in global_data.
                    data_of_one_output = self.output_analyzer(f)
                    self.csv_writer(data_of_one_output)
                else:
                    # print('current file is ',file)
                    system_name = re.search(r'out_([A-Za-z0-9]*)_([A-Za-z0-9]*)_', file).group(1)
                    problem_name = re.search(r'out_([A-Za-z0-9]*)_([A-Za-z0-9_]*)_', file).group(2)

                    # print(type(self.out_analyzer(system_name,f)))
                    # todo: every out_file is a dict now. to be continued.


def system_analyzer(target_dir='tmp/',show = False):
    '''
    draw comparison graph for each problem. but No std_dev is included.
    :param target_dir:
    :return:
    '''
    problem_set=[]
    system_set=[]

    files = os.listdir(target_dir)
    #first analyze the system and problem
    for file in files:
        tmp_sys=re.search(r'([A-Za-z0-9]*)_([A-Za-z0-9_]*).csv',file).group(1)
        tmp_pro = re.search(r'([A-Za-z0-9]*)_([A-Za-z0-9_]*).csv',file).group(2)

        if not tmp_sys in system_set:
            system_set.append(tmp_sys)

        if not tmp_pro in problem_set:
            problem_set.append(tmp_pro)


    for problem_tested in problem_set:
        plt.title(problem_tested)
        for system_tested in system_set:
            filename=system_tested+'_'+problem_tested+'.csv'
            cur_data=pd.read_csv(target_dir+filename,header=None,delimiter=',')
            cur_data.mean(0).plot(label=system_tested)
        plt.legend()
        plt.xlabel('Iteration number')
        plt.ylabel('Fitness')
        plt.savefig(problem_tested+".jpg")
        if show:
            plt.show()

if __name__ == "__main__":
    defaultz_log_dir = "../log/"
    problem_set = ['mux11', 'ant', 'string_match']
    para_list = '/util/hyper_para_list_PonyGE2.json'

    extractor = PARAMETERS_EXTRACTOR(defaultz_log_dir, problem_set)
    extractor.run()
    system_analyzer(target_dir='tmp/',show=True)