#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: Yitan Lou
@email: dabing930714@gmail.com
        y.lou@liacs.leidenuniv.nl
"""

from pdb import set_trace

import numpy as np
import re,os,traceback
from datetime import datetime
from BayesOpt import BO
from BayesOpt.Surrogate import RandomForest
from BayesOpt.SearchSpace import ContinuousSpace, NominalSpace, OrdinalSpace
from multiprocessing import Pool




def runGE(cmd):
    try:
        p = os.popen(cmd)
        std_out = p.read()
        fitness = re.search(r'(\d+(\.\d+)?)([\n\s]*Phenotype)', std_out).group(1)
        print('current parameter has the fitness of ', fitness)
    except :
        fitness=np.nan
        print("error, fitness got value='NAN' ")

    return fitness

def build_cmd(x,parameter_name,cmd):
    if x.get(parameter_name):
        cmd=cmd+('  --'+parameter_name+' ').lower()+str(x[parameter_name])
    return cmd

def obj_func(x):

    # print("currently dealing with probelm ",problem,'\n')
    # print(str(x['CROSSOVER_PROBABILITY']))

    cmd = 'python3 ponyge.py --parameters '+problem+'.txt'

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

    tmp=0
    err=0
    result=[]

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
            tmp += float(fitness)

    pool.close()
    f=tmp/(5-err)


    file= open("summary_of_"+problem+".txt", 'a+')
    file.writelines("cmd inputed is ["+cmd+"]\n")
    file.writelines("fitness="+str(f)+'\n')
    file.writelines("==============spilt line================\n")
    file.close()

    return f



if __name__ == "__main__":
    np.random.seed(67)

    n_step = 1 # iteration number
    n_init_sample = 5
    eval_type = 'dict'  # control the type of parameters for evaluation: dict | list
    M = 21  # maximal length of grammar, to make the problem more linear
    # iteration = 0

    os.chdir("PonyGE2/src/")

    problem_set = ['classification', 'regression', 'string_match', 'pymax']
    # the problem you are going to test

    for problem in problem_set:
        minimize_problem = True
        # by default, it will be a minimize problem.
        if problem == 'classification' or 'pymax':
            minimize_problem = False

        # all shared hyper-parameters
        INITIALISATION = NominalSpace(['PI_grow', 'rhh', 'uniform_tree'], 'INITIALISATION')
        CROSSOVER = NominalSpace(['variable_onepoint', 'variable_twopoint', 'fixed_twopoint', 'fixed_onepoint'],
                                 'CROSSOVER')
        CROSSOVER_PROBABILITY = ContinuousSpace([0, 1], 'CROSSOVER_PROBABILITY')

        MUTATION = NominalSpace(['int_flip_per_codon', 'subtree', 'int_flip_per_ind'], 'MUTATION')
        MUTATION_PROBABILITY = ContinuousSpace([0, 1], 'MUTATION_PROBABILITY')
        MUTATION_EVENT_SUBTREE = OrdinalSpace([1, 5], 'MUTATION_EVENT_SUBSTREE')
        MUTATION_EVENT_FlIP = OrdinalSpace([1, 100], 'MUTATION_EVENT_FlIP')

        SELECTION_PROPORTION = ContinuousSpace([0, 1], 'SELECTION_PROPORTION')
        SELECTION = NominalSpace(['tournament', 'truncation'], 'SELECTION')

        CODON_SIZE = OrdinalSpace([10 * M, 100 * M], 'CODON_SIZE')
        MAX_GENOME_LENGTH = OrdinalSpace([100, 1000], 'MAX_GENOME_LENGTH')
        MAX_INIT_TREE_DEPTH = OrdinalSpace([5, 25], 'MAX_INIT_TREE_DEPTH')
        MAX_TREE_DEPTH = OrdinalSpace([20, 100], 'MAX_TREE_DEPTH')
        TOURNAMENT_SIZE = OrdinalSpace([1, 50], 'TOURNAMENT_SIZE')
        POPULATION_SIZE = OrdinalSpace([100, 500], 'POPULATION_SIZE')

        if minimize_problem == True:
            search_space = INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + CODON_SIZE + MAX_GENOME_LENGTH + MAX_INIT_TREE_DEPTH + MAX_TREE_DEPTH + TOURNAMENT_SIZE + POPULATION_SIZE
        else:
            # for maximize problem, Max_init_tree_depth and Max_tree_depth is not going to be tuned.
            search_space = INITIALISATION + CROSSOVER_PROBABILITY + CROSSOVER + MUTATION + MUTATION_PROBABILITY + MUTATION_EVENT_SUBTREE + MUTATION_EVENT_FlIP + SELECTION_PROPORTION + SELECTION + CODON_SIZE + MAX_GENOME_LENGTH + TOURNAMENT_SIZE + POPULATION_SIZE

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

        f = open("out.txt", 'w+')

        print('xopt: {}'.format(xopt), file=f)
        print('fopt: {}'.format(fitness), file=f)
        print('stop criteria: {}'.format(stop_dict), file=f)