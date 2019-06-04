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
    # run PonyGE2 system
    try:
        p = os.popen(cmd)
        std_out = p.read()
        fitness = re.search(r'(\d+(\.\d+)?)([\n\s]*Phenotype)', std_out).group(1)
        print('current parameter has the fitness of ', fitness)
    except:
        fitness=np.nan
        print("error, fitness got value='NAN' ")

    # try:
    #     used_eval=re.search(r'Eval_count\s+=\s+(\d+)', std_out).group(1)
    #     print("used eval_num=",used_eval)
    # except:
    #     print("didnt get eval num, will used the estimation value to replace this.")
    #     used_eval = 50 * re.search(r'(--POPULATION_SIZE)\s*(\d+)',cmd).group(1)

        # 50 is the default number of iteration in Ponyge2 system.
        # in the case of the system cannot got the eval_num, this value will be set to the iteration_num*pop_size


    return fitness

def build_cmd(x,parameter_name,cmd):
    # used in obj_func()
    if x.get(parameter_name):
        cmd=cmd+('  --'+parameter_name+' ').lower()+str(x[parameter_name])
    return cmd

def obj_func(x):

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
    cmd = cmd + '  --POPULATION_SIZE  '.lower() + str(x['POPULATION_SIZE'])
    # cmd = cmd + '  --random_seed  '.lower() + str('666')
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

    # the problem you are going to test

    for problem in problem_set:
        minimize_problem = True
        # by default, it will be a minimize problem.

        if problem in ['classification', 'pymax']:
            minimize_problem = False



        #replacement
        filename = root_dir + para_list
        system_name='PonyGE2'

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

        CODON_SIZE = get_space('CODON_SIZE',filename=filename,system_name=system_name)
        MAX_GENOME_LENGTH = get_space('MAX_GENOME_LENGTH',filename=filename,system_name=system_name)
        MAX_INIT_TREE_DEPTH = get_space('MAX_INIT_TREE_DEPTH',filename=filename,system_name=system_name)
        MAX_TREE_DEPTH = get_space('MAX_TREE_DEPTH',filename=filename,system_name=system_name)
        POPULATION_SIZE = get_space('POPULATION_SIZE',filename=filename,system_name=system_name)

        # Others
        # GENERATIONS = OrdinalSpace([1, 100], 'GENERATIONS')

        PROBLEM=NominalSpace([problem],'PROBLEM')
        EVAL_BUDGET = OrdinalSpace([max_eval_each,max_eval_each+1],'EVAL_BUDGET')


        if minimize_problem == False:
            search_space = PROBLEM + EVAL_BUDGET +INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + TOURNAMENT_SIZE + CODON_SIZE + MAX_GENOME_LENGTH + MAX_INIT_TREE_DEPTH + MAX_TREE_DEPTH  + POPULATION_SIZE + EVAL_BUDGET
        else:
            # for maximize problem, Max_init_tree_depth and Max_tree_depth is not going to be tuned.
            search_space = PROBLEM + EVAL_BUDGET + INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + TOURNAMENT_SIZE + CODON_SIZE + MAX_GENOME_LENGTH + POPULATION_SIZE + EVAL_BUDGET

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
        f = open(r"../../log/out_ponyge2_"+problem+'_'+str(int(time.time()))+platform.uname()[1]+".txt", 'w+')
        print('parameters: {}'.format(search_space.name), file=f)
        print('xopt: {}'.format(xopt), file=f)
        print('fopt: {}'.format(fitness), file=f)
        print('stop criteria: {}'.format(stop_dict), file=f)
        f.close()




if __name__ == "__main__":
    np.random.seed(67)

    n_step = 100 # iteration number
    n_init_sample = 5
    eval_type = 'dict'  # control the type of parameters for evaluation: dict | list
    M = 21  # maximal length of grammar, to make the problem more linear
    max_eval_each=1000
    # os.chdir("PonyGE2/src/")
    problem_set = ['classification', 'regression', 'string_match', 'pymax']

    # the problem you are going to test
    hyper_parameter_tuning_ponyge2(n_step, n_init_sample, eval_type, max_eval_each, problem_set,M)