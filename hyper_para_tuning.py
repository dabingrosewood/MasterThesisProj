#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Yitan Lou
@email: dabing930714@gmail.com
        y.lou@liacs.leidenuniv.nl
"""

from pdb import set_trace

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
import json
from util.para_list_reader import get_space

def runGE(cmd):
    '''
    buiild the command to feed hyper-parameter by using command line methods.
    :param cmd:
    :return fitness: fitness value corresponding to feeded parameters.
    '''
    # run PonyGE2 system
    try:
        p = os.popen(cmd)
        std_out = p.read()
        fitness = re.search(r'(\d+(\.\d+)(e-\d+)?)([\n\s]*Phenotype)', std_out).group(1)
        print('current parameter has the fitness of ', fitness)
    except:
        fitness=np.nan
        print("error, fitness got value='NAN' ")


    return fitness

def build_cmd(x,parameter_name,cmd):
    '''
    only used for build command for PonyGE2 system
    :param x:
    :param parameter_name:
    :param cmd:
    :return:
    '''
    # used in obj_func()
    if x.get(parameter_name):
        cmd=cmd+('  --'+parameter_name+' ').lower()+str(x[parameter_name])
    return cmd

def obj_func(x):
    '''

    :param x: SearchSpace
    :return f:Fitness value
    '''

    # print("currently dealing with probelm ",problem,'\n')

    cmd = 'python3 ponyge.py --parameters '+str(x['PROBLEM'])+'.txt'
    cmd = build_cmd(x, 'EVAL_BUDGET', cmd)

    cmd = cmd + '  --CROSSOVER_PROBABILITY  '.lower() + str(x['CROSSOVER_PROBABILITY'])
    cmd = cmd + '  --INITIALISATION  '.lower() + str(x['INITIALISATION'])
    cmd = cmd + '  --CROSSOVER  '.lower() + str(x['CROSSOVER'])
    cmd = cmd + '  --MUTATION  '.lower() + str(x['MUTATION'])
    cmd = cmd + '  --SELECTION  '.lower() + str(x['SELECTION'])
    cmd = cmd + '  --SELECTION_PROPORTION  '.lower() + str(x['SELECTION_PROPORTION'])
    cmd = cmd + '  --MAX_GENOME_LENGTH  '.lower() + str(x['MAX_GENOME_LENGTH'])
    # cmd = cmd + '  --MAX_INIT_TREE_DEPTH  '.lower() + str(x['MAX_INIT_TREE_DEPTH'])
    # cmd = cmd + '  --MAX_TREE_DEPTH  '.lower() + str(x['MAX_TREE_DEPTH'])
    cmd = cmd + '  --TOURNAMENT_SIZE  '.lower() + str(x['TOURNAMENT_SIZE'])
    cmd = cmd + '  --ELITE_SIZE  '.lower() + str(x['ELITE_SIZE'])
    cmd = cmd + '  --POPULATION_SIZE  '.lower() + str(x['POPULATION_SIZE'])
    cmd = cmd + '  --codon_size  '.lower() + str(x['CODON_SIZE'])
    if str(x['CROSSOVER'])=='subtree':
        cmd = cmd + '  --MUTATION_EVENT  '.lower() + str(x['MUTATION_EVENT_SUBTREE'])
    elif str(x['CROSSOVER'])=='int_flip_per_ind':
        cmd = cmd + '  --MUTATION_EVENT  '.lower() + str(x['MUTATION_EVENT_FLIP'])
    else:
        cmd = cmd + '  --MUTATION_PROBABILITY  '.lower() + str(x['MUTATION_PROBABILITY'])

    cmd = build_cmd(x, 'MAX_INIT_TREE_DEPTH', cmd)
    cmd = build_cmd(x, 'MAX_TREE_DEPTH', cmd)



    print("command inputed is ", cmd)
    # check the command inputed here

    tmp=0
    err=0
    result=[]
    valid_result=[]

    pool = Pool(processes=5)
    for i in range(5):
        result.append(pool.apply_async(runGE, args=(cmd,)))
    # pool.join()
    for i in result:
        fitness = i.get()

        # print('fitness=',fitness)
        if fitness==np.nan:
            err+=1
        else:
            valid_result.append(float(fitness))

    pool.close()
    f=np.average(valid_result)
    print("std_dev=",np.std(valid_result))
    print("avg=",f)

    file= open(r"../log/summary_of_ponyge2_"+str(x['PROBLEM'])+platform.uname()[1]+".log", 'a+')
    file.writelines("cmd inputed is ["+cmd+"]\n")
    file.writelines("fitness="+str(f)+'\n')
    file.close()

    return f

def hyper_parameter_tuning_ponyge2(n_step,n_init_sample,eval_type, max_eval_each=100000, problem_set=['string_match'],para_list='/util/hyper_para_list_PonyGE2.json'):
    np.random.seed(67)
    root_dir=os.getcwd()
    os.chdir("PonyGE2/src/")

    # if not os.path.exists('../log'):
    #     os.mkdir('../log')

    for problem in problem_set:
        # test problems one by one.
        minimize_problem = True
        # by default, it will be a minimize problem.

        if problem in ['classification', 'pymax']:
            minimize_problem = False

        filename = root_dir + para_list
        system_name='PonyGE2'


        #Tunable hyper-parameters

        INITIALISATION = get_space('INITIALISATION',filename=filename,system_name=system_name)
        CROSSOVER = get_space('CROSSOVER',filename=filename,system_name=system_name)
        CROSSOVER_PROBABILITY = get_space('CROSSOVER_PROBABILITY',filename=filename,system_name=system_name)

        MUTATION = get_space('MUTATION',filename=filename,system_name=system_name)
        MUTATION_PROBABILITY = get_space('MUTATION_PROBABILITY',filename=filename,system_name=system_name)
        MUTATION_EVENT_SUBTREE = get_space('MUTATION_EVENT_SUBTREE',filename=filename,system_name=system_name)
        MUTATION_EVENT_FlIP = get_space('MUTATION_EVENT_FlIP',filename=filename,system_name=system_name)

        SELECTION_PROPORTION = get_space('SELECTION_PROPORTION',filename=filename,system_name=system_name)
        SELECTION = get_space('SELECTION',filename=filename,system_name=system_name)
        TOURNAMENT_SIZE = get_space('TOURNAMENT_SIZE',filename=filename,system_name=system_name)
        ELITE_SIZE = get_space('ELITE_SIZE',filename=filename,system_name=system_name)


        CODON_SIZE = get_space('CODON_SIZE',filename=filename,system_name=system_name)
        MAX_GENOME_LENGTH = get_space('MAX_GENOME_LENGTH',filename=filename,system_name=system_name)
        MAX_INIT_TREE_DEPTH = get_space('MAX_INIT_TREE_DEPTH',filename=filename,system_name=system_name)
        MAX_TREE_DEPTH = get_space('MAX_TREE_DEPTH',filename=filename,system_name=system_name)
        POPULATION_SIZE = get_space('POPULATION_SIZE',filename=filename,system_name=system_name)

        # Others/Static parameters

        PROBLEM=NominalSpace([problem],'PROBLEM')
        EVAL_BUDGET = OrdinalSpace([max_eval_each,max_eval_each+1],'EVAL_BUDGET')

        #todo: By default, the following line should be 'if minimize_problem == True:', since the 'MAX_INIT_TREE_DEPTH' and 'MAX_TREE_DEPTH' can easily causes problem by generating too big search space.
        #But we found it also prodeces this problem for mux11 problem. so these two parameters are temporarily disbaled.
        if minimize_problem == False:
            search_space = PROBLEM + INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + TOURNAMENT_SIZE + ELITE_SIZE + CODON_SIZE + MAX_GENOME_LENGTH + MAX_INIT_TREE_DEPTH + MAX_TREE_DEPTH + POPULATION_SIZE + EVAL_BUDGET
        else:
            # for maximize problem, Max_init_tree_depth and Max_tree_depth is not going to be tuned.
            search_space = PROBLEM + INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + TOURNAMENT_SIZE + ELITE_SIZE + CODON_SIZE + MAX_GENOME_LENGTH + POPULATION_SIZE + EVAL_BUDGET

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
        f = open(r"../../logs/out_PonyGE2_"+problem+'_'+str(int(time.time()))+platform.uname()[1]+".txt", 'w+')
        print('parameters: {}'.format(search_space.name), file=f)
        print('xopt: {}'.format(xopt), file=f)
        print('fopt: {}'.format(fitness), file=f)
        print('stop criteria: {}'.format(stop_dict), file=f)
        f.close()




if __name__ == "__main__":
    np.random.seed(67)

    n_step = 100 # iteration number
    n_init_sample = 5 # number of sample point.
    eval_type = 'dict'  # control the type of parameters for evaluation: dict | list
    M = 21  # maximal length of grammar, to make the problem more linear
    max_eval_each=1000
    problem_set = ['regression', 'string_match', 'pymax','classification']

    # the problem you are going to test
    hyper_parameter_tuning_ponyge2(n_step, n_init_sample, eval_type, max_eval_each, problem_set)