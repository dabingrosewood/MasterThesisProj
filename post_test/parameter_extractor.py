import sys, os, re
import numpy as np
import json
import csv
import matplotlib.pyplot as plt
import pandas as pd


class PARAMETERS_EXTRACTOR:
    """
    This class is used to extract and analyze data from log files, which are generated by running management.py
    """

    def __init__(self, dir, problem_set):
        '''
        :param dir: location of log
        :param problem_set: tested problem
        '''
        self.target_dir = dir
        self.problem_set = problem_set
        # self.para_dir = para_dir

    def getpara(self, system_name):
        '''
        This funciton is used to extract the name of tuned HYPER_PARAMETER in the test, by reading the json file which
        control hyper-parameters in.
        :param system_name:
        :return:
        '''
        llist = []

        # other parameter before the main group
        if system_name == 'ponyge2' or system_name == 'PonyGE2':
            para_file = '../util/hyper_para_list_PonyGE2.json'
            llist.append('PROBLEM')
        elif system_name == 'SGE':
            para_file = '../util/hyper_para_list_SGE.json'
            llist.append('PROBLEM')
        elif system_name == 'GGES':
            para_file = '../util/hyper_para_list_GGES.json'
            llist.append('PROBLEM')

        with open(para_file, 'r') as load_f:
            data = json.load(load_f)
            for parameter in data:
                if parameter['name']:
                    llist.append(parameter['name'])

        # other parameter before the main group
        if system_name == 'SGE':
            llist.append('NUMBER_OF_ITERATIONS')
            llist.append('EVAL_BUDGET')

            llist.remove('MAX_REC_LEVEL')

        if system_name == 'SGE':
            llist.append('EVAL_BUDGET')

        return llist

    def output_analyzer(self, f):
        """
        This funciton extract data from std_out of test.
        Due to the fact i use the command like ' nohup python3 management.py >log/output_node112_3.txt 2>&1 &', std_out
        are stored in those files with the name of 'output_MACHINE_NAME_IDNEX.txt'

        :param f:
        :return: A List with following structure:[level1,level1,[...]]
            Level1:(SYSTEM_NAME,[level2],[level2],[...])
            Level2:[PROBLEM_NAME,[level3],[level3],[...]]
            Level3:[[Iteration_number,Fitness_value],[Iteration_number,Fitness_value],[...]]

        """
        recorder = []  # lv1
        tuning_data_for_one_system = ()  # lv2
        data_for_one_problem = []  # lv3
        problem_index = 0
        buffer_flat_space = ''
        for line in f.readlines():

            # find the system name to categorized all log.
            if re.search(r'now testing ([A-Za-z0-9]*) system', line):
                system_name = re.search(r'now testing ([A-Za-z0-9]*) system', line).group(1)

                if len(tuning_data_for_one_system) != 0:
                    # in the case of it already have data, which mean we encounter another system.
                    # finish the data from previous one and rebuild new data list.
                    tuning_data_for_one_system[1].append(data_for_one_problem)
                    data_for_one_problem = []  # need to clear all used data
                    problem_index = 0
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
                    data_for_one_problem[1].append([cur_iteration_num, cur_fitness_value])

                elif data_for_one_problem[1][-1][0] > cur_iteration_num:
                    #the case of met a new iteration
                    tuning_data_for_one_system[1].append(data_for_one_problem)  # end the previous problem
                    data_for_one_problem = [self.problem_set[problem_index], []]
                    problem_index += 1
                    if problem_index >= len(self.problem_set):
                        problem_index = 0
                    data_for_one_problem[1].append([cur_iteration_num, cur_fitness_value])

            if re.search(r'flat objective value after taking 2 samples', line):
                # to handle the case of No
                print('flat initial space for problem ', 'in', f.name, 'for system', system_name,
                      'This part of data  will be ignored')

                if buffer_flat_space != line:
                    problem_index += 1
                    buffer_flat_space = line

        tuning_data_for_one_system[1].append(data_for_one_problem)
        recorder.append(tuning_data_for_one_system)
        # print(f.name,recorder)
        return recorder

    def out_analyzer(self, system_name, f,type):
        '''
        In the benchmark test, for every problem the system will store its best-founded hyper-parameters settings, under
        the name of out_SYSTEMNAME_PROBLEM_TIME_MACHINENAME.txt
        This funciton is used to extract the best founded hyper-parameter setting stored in one file f.
        A dict includes the parameter_name and it's value will be returned.
        :param system_name:
        :param f: file handle
        :param type: returned type
        :return:
        '''
        while 1:
            line = f.readline()
            if not line:
                break
            if line.startswith("xopt"):
                tmp = line.strip("xopt: [").replace(']\n', '\n').replace("'", "").replace(" ", "")
                parameter_dict = dict(zip(self.getpara(system_name), tmp.split(',')))

        if type=='list':
            return tmp.split(',')
        elif type=='dict':
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

                with open('tmp/' + system[0] + '_' + problem[0] + '.csv', 'a') as csv_file:
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
            with open(os.path.join(os.getcwd(), self.target_dir, file), encoding='utf-8') as f:

                if file.startswith('output'):
                    # This file is standard output of test (nohup command), extract all data and store them in global_data.
                    # pass
                    data_of_one_output = self.output_analyzer(f)
                    self.csv_writer(data_of_one_output)
                elif file.startswith('out_'):
                    # print('current file is ', file)

                    system_name = re.search(r'out_([A-Za-z0-9]*)_([A-Za-z0-9]*)_', file).group(1)
                    problem_name = re.search(r'out_([A-Za-z0-9]*)_([A-Za-z0-9_]*)_', file).group(2)

                    data_of_out_log=self.out_analyzer(system_name,f,'list')

                    if not os.path.exists('tmp_para'):
                        os.mkdir('tmp_para/')
                    with open('tmp_para/configurations_'+system_name+'_'+problem_name+'.csv','a') as record_file:
                        # print(data_of_out_log)
                        writer = csv.writer(record_file)
                        writer.writerow(data_of_out_log[0:-1])



def system_analyzer(target_dir='tmp/', show=False):
    '''
    draw comparison graph for each problem. but No std_dev is included.
    :param target_dir:
    :return:
    '''
    problem_set = []
    system_set = []

    files = os.listdir(target_dir)
    # first analyze the system and problem
    for file in files:
        if file.startswith('.'):
            continue

        tmp_sys = re.search(r'([A-Za-z0-9]*)_([A-Za-z0-9_]*).csv', file).group(1)
        tmp_pro = re.search(r'([A-Za-z0-9]*)_([A-Za-z0-9_]*).csv', file).group(2)

        if not tmp_sys in system_set:
            system_set.append(tmp_sys)

        if not tmp_pro in problem_set:
            problem_set.append(tmp_pro)

    for problem_tested in problem_set:
        plt.title(problem_tested)
        for system_tested in system_set:
            filename = system_tested + '_' + problem_tested + '.csv'
            cur_data = pd.read_csv(target_dir + filename, header=None, delimiter=',')
            # cur_data is a DataFrame

            # -----------------no deviation version-----------------------
            # cur_data.mean(0).plot(label=system_tested)
            # -----------------no deviation version-----------------------

            # -----------------with std_dev version-----------------------


            mean_value = cur_data.mean(0)
            std_value = cur_data.std(0)

            x = np.arange(0,100,1)
            y = mean_value
            y1 = mean_value+std_value
            y2 = mean_value-std_value


            if system_tested == 'PonyGE2':
                plt.plot(x, y, color='orange', label='PonyGE2')
                plt.plot(x, y1, color='orange', alpha=0.4, linestyle='dotted')
                plt.plot(x, y2, color='orange', alpha=0.4, linestyle='dotted')
            elif system_tested=='SGE':
                plt.plot(x, y, color='blue', label='SGE')
                plt.plot(x, y1, color='blue', alpha=0.4, linestyle='dotted')
                plt.plot(x, y2, color='blue', alpha=0.4, linestyle='dotted')
            else:
                pass
                # in the case new system added, please modify this part.
            # -----------------with std_dev version-----------------------


            # -----------------For thesis data-----------------------
            print('final result for problem',problem_tested,' in ',system_tested, 'is ',pd.Series.as_matrix(y)[-1])
            print(problem_tested,' in ',system_tested,'fitst result=',pd.Series.as_matrix(y)[0],
                  'final result=',pd.Series.as_matrix(y)[-1],
                  'improvement=',(pd.Series.as_matrix(y)[0]-pd.Series.as_matrix(y)[-1])/pd.Series.as_matrix(y)[-1])
            # -----------------For thesis data-----------------------


        plt.legend()
        plt.xlabel('Iteration number')
        plt.ylabel('Fitness')
        plt.savefig(problem_tested + ".jpg")
        if show:
            plt.show()


def csv_conveger_for_sys(target_dir='tmp_para/'):
    '''
    Used to converge all .csv files in target directory into one file by by systems.
    :param target_dir:
    :return:
    '''

    system_list=['PonyGE2','SGE']

    for sys_name in system_list:
        files=os.listdir(target_dir)
        # print(files)
        for file in files:
            if re.search(sys_name,file):
                fr = open(os.path.join(target_dir,file), 'rb').read()
                with open(target_dir+'/result_'+sys_name+'.csv', 'ab') as f:
                    f.write(fr)
                f.close()

    files = os.listdir(target_dir)
    print(files)
    for file in files:
        if file.startswith('result'):

            print('dealing ', file)
            sys_name = re.search(r'result_([A-Za-z0-9]*)', file).group(1)

            if sys_name == 'SGE':
                schema = ['problem', 'population_size', 'elitism', 'tournament_size', 'crossover_rate',
                          'mutation_rate', 'iteration_num']

            elif sys_name == 'PonyGE2':
                schema = ['problem', 'initialization', 'crossover_rate', 'crossover_type', 'mutation',
                          'mutation_probability',
                          'mutation_event_subtree', 'mutation_event_flip', 'selection_proportion', 'selection',
                          'tournament_size', 'elite_size', 'codon_size', 'max_genome_size', 'population_size']

            data = pd.read_csv(os.path.join(target_dir, file), header=None)
            data.columns = schema

            if sys_name == 'PonyGE2':

                initialization_mapping = {'rhh': 1, 'PI_grow': 2, 'uniform_tree': 3}
                data['initialization'] = data['initialization'].map(initialization_mapping)

                crossover_type_mapping = {'variable_onepoint': 1, 'variable_twopoint': 2, 'fixed_twopoint': 3,
                                          'fixed_onepoint': 4}
                data['crossover_type'] = data['crossover_type'].map(crossover_type_mapping)

                mutation_mapping = {'int_flip_per_codon': 1, 'subtree': 2, 'int_flip_per_ind': 3}
                data['mutation'] = data['mutation'].map(mutation_mapping)

                selection_mapping = {'tournament': 1, 'truncation': 2, }
                data['selection'] = data['selection'].map(selection_mapping)

            data.to_csv(os.path.join(target_dir, file), sep=',', header=True, index=False)


def conf_analyzer(target_dir='tmp_para/', show=False):
    '''
    This function is not useable right now since the generated parallel coordinates looks bad.
    Currently use https://app.rawgraphs.io/ to draw the graph
    :param target_dir:
    :param show:
    :return:
    '''

    import pandas as pd
    from pandas.tools.plotting import parallel_coordinates

    files = os.listdir(target_dir)
    for file in files:
        if file.startswith('.'):
            continue

        if file.startswith('result'):
            sys_name = re.search(r'result_([A-Za-z0-9]*)',file).group(1)


            if sys_name=='SGE':
                schema=['problem','population_size','elitism','tournament_size','crossover_rate','mutation_rate']

            elif sys_name=='PonyGE2':
                schema=['problem','initialization','crossover_rate','crossover_type','mutation','mutation_probability',
                        'mutation_event_subtree','mutation_event_flip','selection_proportion','seletion',
                        'tournament_size','elite_size','codon_size','max_genome_size',]

            data = pd.read_csv(os.path.join(target_dir,file),header=0)
            # data.columns = schema



            print(data)
            parallel_coordinates(data,0)
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fancybox=True, shadow=False)
            plt.show()


if __name__ == "__main__":
    defaultz_log_dir = "../logs/"

    # Orders of given problems matters
    # dealing_problem_set = ['parity5']
    # dealing_problem_set = ['ant','string_match','vladislavleva4','mux11']

    # extract information for original log files.
    # extractor = PARAMETERS_EXTRACTOR(defaultz_log_dir, dealing_problem_set)
    # extractor.run()

    # comparison between different GE systems on different benchmark problems.
    system_analyzer(target_dir='tmp/', show=True)

    # used to converge all .csv based on the tested systems' name.
    # csv_conveger_for_sys('tmp_para')


    #
    # coordinate parallel
    # conf_analyzer('tmp_para',True)