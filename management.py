import sys,os

from shutil import copytree, ignore_patterns,rmtree
import hyper_para_tuning
import numpy as np

def exec_cmd(cmd):
    output = os.popen(cmd)
    print(output.read()+'\n')

def cpy_interface():
    # build cython_implemented package for PonyGE2
    root_wd=os.getcwd()
    source_dir=root_wd+"/cython"
    target_dir=root_wd+"/PonyGE2/src/fitness/cython"

    if os.path.exists(target_dir):
        if os.path.exists(target_dir):
            print("原有文件夹将被删除")
            rmtree(target_dir)
        print("start copying")
        copytree(source_dir,target_dir,ignore_patterns("*.so","*.c","build/*"))
        print("copying is finished")

def clear_ponyge_result():
    result_dir=os.getcwd()+"/PonyGE2/results"
    if os.path.exists(result_dir):
        rmtree(result_dir)



# build_cmd="python3 setup.py build_ext --inplace"


# os.chdir("PonyGE2/src/")
# exec_cmd("python3 ponyge.py --parameter classification.txt")

if __name__ == "__main__":

    # clear previous Ponyge result
    clear_ponyge_result()


    # copy the interface into src/fitness
    # cpy_interface()


    build_cmd="python3 setup.py build_ext --inplace"
    exec_cmd(build_cmd)


    ########################################################################
    # test PonyGE2

    # parameter setting
    np.random.seed(67)
    n_step = 100  # iteration number
    n_init_sample = 5
    eval_type = 'dict'  # control the type of parameters for evaluation: dict | list
    M = 21  # maximal length of grammar, to make the problem more linear
    max_eval_each = 1000000
    problem_set = ['classification', 'regression', 'string_match', 'pymax']

    hyper_para_tuning.hyper_parameter_tuning(n_step, n_init_sample, eval_type, max_eval_each, problem_set, M)
    ##########################################################################