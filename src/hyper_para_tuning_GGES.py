#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Yitan Lou
@email: dabing930714@gmail.com
        y.lou@liacs.leidenuniv.nl
"""
import numpy as np
import re,os
from BayesOpt import BO
from BayesOpt.Surrogate import RandomForest
from BayesOpt.SearchSpace import NominalSpace, OrdinalSpace
from multiprocessing import Pool
import platform
import time

from src.para_list_reader import get_space

def build_cmd(x,parameter_name,cmd):
    '''
    only used for build command for GGES system
    :param x:
    :param parameter_name:
    :param cmd:
    :return:
    '''
    # used in obj_func()
    if x.get(parameter_name):
        cmd=cmd+('  -p '+parameter_name+'=').lower()+str(x[parameter_name])
    return cmd


def run_gges(cmd):
    try:
        std_out = os.popen(cmd).read()
        # std_out,std_err = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()

        print('std_out is :',std_out)

        #todo: bug here
        fitness = re.search(r'(.*?)(\d+\.\d*)((.*?)\nend)', std_out).group(2)

        print('Current Fitness has the fitness of ', fitness)
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
    # f_old = open(GGES_dir + '/src/gges_backup.c', 'r')
    # f_new = open(GGES_dir + '/src/gges.c', 'w+')
    #
    # for line in f_old:
    #     newline = line
    #     if re.search('def->population_size', line):
    #         newline = line.replace(re.findall(r'\d+', line)[0], str(x['POPULATION_SIZE']))
    #
    #     if re.search('def->generation_count', line):
    #         newline = line.replace(re.findall(r'\d+', line)[0], str(x['NUMBER_OF_ITERATIONS']))
    #
    #     if re.search('def->tournament_size', line):
    #         newline = line.replace(re.findall(r'\d+', line)[0], str(x['TOURNAMENT_SIZE']))
    #
    #     if re.search('def->crossover_rate', line):
    #         newline = line.replace(re.findall(r'\d\.\d+', line)[0], str(x['PROB_CROSSOVER']))
    #
    #     if re.search('def->mutation_rate', line):
    #         newline = line.replace(re.findall(r'\d\.\d+', line)[0], str(x['PROB_MUTATION']))
    #
    #     f_new.write(newline)
    # f_old.close()
    # f_new.close()
    # os.system("make & clean")


    # cmd='./dist/suite_'+x['PROBLEM']+' ./bnf/suite/'+x['PROBLEM']+'.bnf'


    # by modifying the command to feed parameters.
    cmd='./dist/suite_'+x['PROBLEM']+' ./bnf/suite/'+x['PROBLEM']+'.bnf' # basic command

    cmd=build_cmd(x,'pop_size',cmd)
    cmd=build_cmd(x,'tourn_size',cmd)
    cmd=build_cmd(x,'crossover_rate',cmd)
    cmd=build_cmd(x,'mutation_rate',cmd)
    cmd=build_cmd(x,'init_codon_count',cmd)
    cmd=build_cmd(x,'representation',cmd)
    # cmd=build_cmd(x,'search_method',cmd)
    cmd = build_cmd(x, 'GENERATIONS', cmd)


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
    os.system("make ")

    if not os.path.exists('log'):
        os.mkdir('log')

    for problem in problem_set:
        minimize_problem=True
        # by default, it will be a minimize problem.

        paralist_filename = root_dir + para_list
        system_name = 'GGES'

        #main parameters
        POPULATION_SIZE = get_space('pop_size', filename=paralist_filename, system_name=system_name)
        TOURNAMENT_SIZE = get_space('tourn_size', filename=paralist_filename, system_name=system_name)
        PROB_CROSSOVER = get_space('crossover_rate', filename=paralist_filename, system_name=system_name)
        PROB_MUTATION = get_space('mutation_rate', filename=paralist_filename, system_name=system_name)
        INIT_CODON_COUNT = get_space('init_codon_count',filename=paralist_filename, system_name=system_name)
        REPRESENTATION = get_space('representation',filename=paralist_filename, system_name=system_name)
        # SEARCH_METHOD = get_space('search_method',filename=paralist_filename, system_name=system_name)

        #others/Static parameters
        EVAL_BUDGET = OrdinalSpace([max_eval_each, max_eval_each + 1], 'EVAL_BUDGET')
        PROBLEM = NominalSpace([problem], 'PROBLEM')
        GENERATIONS=OrdinalSpace([50, 50 + 1], 'GENERATIONS')

        search_space = PROBLEM + POPULATION_SIZE + TOURNAMENT_SIZE + PROB_CROSSOVER + PROB_MUTATION + INIT_CODON_COUNT + REPRESENTATION + GENERATIONS + EVAL_BUDGET

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
        f = open(r"../logs/out_GGES_" + problem + '_' + str(int(time.time())) + platform.uname()[1] + ".txt", 'w+')
        print('parameters: {}'.format(search_space.name), file=f)
        print('xopt: {}'.format(xopt), file=f)
        print('fopt: {}'.format(fitness), file=f)
        print('stop criteria: {}'.format(stop_dict), file=f)
        f.close()



if __name__ == "__main__":
    hyper_parameter_tuning_GGES(5,5)