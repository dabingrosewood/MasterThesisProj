#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Yitan Lou
@email: dabing930714@gmail.com
        y.lou@liacs.leidenuniv.nl
"""
import numpy as np
import datetime
import re,os,traceback
from datetime import datetime
from BayesOpt import BO
from BayesOpt.Surrogate import RandomForest
from BayesOpt.SearchSpace import ContinuousSpace, NominalSpace, OrdinalSpace
from multiprocessing import Pool
import platform
import time

from util.para_list_reader import get_space



def run_gges(cmd):
    try:
        std_out = os.popen(cmd).read()
        # print(std_out)
        #todo: bug here
        fitness = re.search(r'(.*?)(\d+\.\d*)((.*?)\nend)', std_out).group(2)
        # fitness = re.search(r'(.*?)(\d+\.\d*)', std_out).group(2)
        print('current parameter has the fitness of ', fitness)
    except:
        fitness=np.nan
        print("error, fitness got value='NAN' ")

    return fitness

def obj_func(x):
    '''
    This fucntion calls GGES and feed hyper-parameters by modifying it's default configuration in ggse.c file.
    Warning: Previous character could possibly causes problem in multi-processing. It's safer to call this solely.
    :param x:
    :return:
    '''
    GGES_dir = os.getcwd()
    # print("sge_dir=", sge_dir)


    # by modifying the config file to feed parameters.
    f_old = open(GGES_dir + '/src/gges_backup.c', 'r')
    f_new = open(GGES_dir + '/src/gges.c', 'w+')

    for line in f_old:
        newline = line
        if re.search('def->population_size', line):
            newline = line.replace(re.findall(r'\d+', line)[0], str(x['POPULATION_SIZE']))

        if re.search('def->generation_count', line):
            newline = line.replace(re.findall(r'\d+', line)[0], str(x['NUMBER_OF_ITERATIONS']))

        if re.search('def->tournament_size', line):
            newline = line.replace(re.findall(r'\d+', line)[0], str(x['TOURNAMENT_SIZE']))

        if re.search('def->crossover_rate', line):
            newline = line.replace(re.findall(r'\d\.\d+', line)[0], str(x['PROB_CROSSOVER']))

        if re.search('def->mutation_rate', line):
            newline = line.replace(re.findall(r'\d\.\d+', line)[0], str(x['PROB_MUTATION']))

        f_new.write(newline)
    f_old.close()
    f_new.close()

    # test part
    os.system("make clean")
    cmd='./dist/suite_'+x['PROBLEM']+' ./bnf/suite/'+x['PROBLEM']+'.bnf'
    print("command inputed is ", cmd)
    # check the command inputed here

    tmp = 0
    err = 0
    result = []
    valid_result=[]

    pool = Pool(processes=5)
    for i in range(5):
        result.append(pool.apply_async(run_gges, args=(cmd,)))
    # pool.join()
    for i in result:
        fitness = i.get()

        # print('fitness=',fitness)
        if fitness == np.nan:
            err += 1
        else:
            valid_result.append(float(fitness))

    pool.close()

    f = np.average(valid_result)
    dev=np.std(valid_result)
    print("std_dev=",dev)
    print("avg=",f)

    # os.chdir('../')
    file = open(r"log/summary_of_GGES_" + str(x['PROBLEM']) + platform.uname()[1] + ".log", 'a+')
    file.writelines("cmd inputed is [" + cmd + "]\n")
    file.writelines("fitness=" + str(f) + '\n')
    file.close()

    return f


def hyper_parameter_tuning_GGES(n_step,n_init_sample,eval_type='dict', max_eval_each=100000, problem_set=['ant','string_match','mux11'],para_list='/util/hyper_para_list_GGES.json'):

    root_dir=os.getcwd()
    os.chdir("GGES")

    if not os.path.exists('log'):
        os.mkdir('log')

    for problem in problem_set:
        minimize_problem=True
        # by default, it will be a minimize problem.

        paralist_filename = root_dir + para_list
        system_name = 'GGES'

        #main parameter
        POPULATION_SIZE = get_space('POPULATION_SIZE', filename=paralist_filename, system_name=system_name)
        TOURNAMENT_SIZE = get_space('TOURNAMENT_SIZE', filename=paralist_filename, system_name=system_name)
        PROB_CROSSOVER = get_space('PROB_CROSSOVER', filename=paralist_filename, system_name=system_name)
        PROB_MUTATION = get_space('PROB_MUTATION', filename=paralist_filename, system_name=system_name)

        #others/Static parameters
        EVAL_BUDGET = OrdinalSpace([max_eval_each, max_eval_each + 1], 'EVAL_BUDGET')
        PROBLEM = NominalSpace([problem], 'PROBLEM')
        NUMBER_OF_ITERATIONS=OrdinalSpace([10, 10 + 1], 'NUMBER_OF_ITERATIONS')

        search_space = PROBLEM + POPULATION_SIZE + TOURNAMENT_SIZE + PROB_CROSSOVER + PROB_MUTATION + NUMBER_OF_ITERATIONS + EVAL_BUDGET

        model = RandomForest(levels=search_space.levels)

        opt = BO(search_space, obj_func, model, max_iter=n_step,
                 n_init_sample=n_init_sample,
                 n_point=1,  # number of the candidate solution proposed in each iteration
                 n_job=1,  # number of processes for the parallel execution
                 minimize=minimize_problem,
                 eval_type=eval_type,  # use this parameter to control the type of evaluation
                 verbose=True,  # turn this off, if you prefer no output
                 optimizer='MIES')

        xopt, fitness, stop_dict = opt.run()
        f = open(r"../log/out_GGES_" + problem + '_' + str(int(time.time())) + platform.uname()[1] + ".txt", 'w+')
        print('parameters: {}'.format(search_space.name), file=f)
        print('xopt: {}'.format(xopt), file=f)
        print('fopt: {}'.format(fitness), file=f)
        print('stop criteria: {}'.format(stop_dict), file=f)
        f.close()



if __name__ == "__main__":
    hyper_parameter_tuning_GGES(5,5)