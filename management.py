import sys,os
from shutil import copytree, ignore_patterns,rmtree
import hyper_para_tuning,hyper_para_tuning_sge
import numpy as np

from util.exec_cmd import exec_cmd



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
        os.system('mkdir '+target_dir)
    copytree(source_dir,target_dir,ignore_patterns('*.so',"*.c","build/*"))
    print("copying is finished")


class Tester_PONYGE2:
    def __init__(self,n_step,n_init_sample,eval_type,max_eval_each,para_list='/util/hyper_para_list_PonyGE2.json'):
        self.n_step = n_step
        self.n_init_sample = n_init_sample
        self.eval_type = eval_type
        self.max_eval_each = max_eval_each
        self.para_list = para_list


    def make_interface(self):
        # copy the interface into src/fitness
        if not os.path.exists(os.getcwd() + "/PonyGE2/src/fitness/cython"):
            cpy_interface()
            build_cmd = "python3 setup.py build_ext --inplace"
            cd_cmd = 'cd ' + os.getcwd() + "/PonyGE2/src/fitness/cython"
            exec_cmd(cd_cmd, build_cmd)
        else:
            print('interface alrady exist. Pass. IF NOT, delete the folder then retry or use refresh_interface.\n')


    def refresh_interface(self):
        rmtree(os.getcwd()+"/PonyGE2/src/fitness/cython")
        cpy_interface()
        build_cmd = "python3 setup.py build_ext --inplace"
        cd_cmd='cd '+os.getcwd()+"/PonyGE2/src/fitness/cython"
        exec_cmd(cd_cmd, build_cmd)


    def clear_log(self):
        # clear previous Ponyge result
        result_dir = os.getcwd() + "/PonyGE2/results"
        if os.path.exists(result_dir):
            rmtree(result_dir)
        os.makedirs(result_dir)


    def give_problem(self,problem_set):
        self.problem_set=problem_set


    def run_PonyGE2(self):

        print("***" * 20 + "now testing PonyGE2 system" + "***" * 20)
        hyper_para_tuning.hyper_parameter_tuning_ponyge2(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                         self.para_list)

    def make_problem(self):
        # used to add new problem from testsuite into PonyGE2
        # 1. bnf
        # 2. fitness
        # 3. parameter.txt

        pass



class Tester_SGE:
    def __init__(self,n_step,n_init_sample,eval_type,max_eval_each,para_list='/util/hyper_para_list_PonyGE2.json'):
        self.n_step = n_step
        self.n_init_sample = n_init_sample
        self.eval_type = eval_type
        self.max_eval_each = max_eval_each
        self.para_list = para_list

    def make_interface(self):
        if not os.path.exists(os.getcwd() + "/sge/src/util/interface"):
            cpy_interface()
            build_cmd = "python setup.py build_ext --inplace"
            cd_cmd = 'cd ' + os.getcwd() + "/sge/src/util/interface"
            exec_cmd(cd_cmd, build_cmd)
        else:
            print('interface alrady exist. Pass. IF NOT, delete the folder then retry or use refresh_interface.\n')

    def refresh_interface(self):
        rmtree(os.getcwd()+"/sge/src/util/interface")
        cpy_interface()
        build_cmd = "python setup.py build_ext --inplace"
        cd_cmd='cd '+os.getcwd()+"/sge/src/util/interface"
        exec_cmd(cd_cmd, build_cmd)

    def give_problem(self,problem_set):
        self.problem_set=problem_set

    def run_sge(self):
        print("***"*20+"now testing SGE system"+"***"*20)

        hyper_para_tuning_sge.hyper_parameter_tuning_sge(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                         self.para_list)

    def make_problem(self):
        pass




if __name__ == "__main__":

    # ****Test PonyGE2*****
    # tester=Tester_PONYGE2(n_step = 20,
    #                  n_init_sample = 5,
    #                  eval_type = 'dict',
    #                  max_eval_each=50000,
    #                  para_list='/util/hyper_para_list_PonyGE2.json'
    #                  )
    # tester.give_problem(['ant'])
    # # tester.give_problem(['ant','classification', 'regression', 'string_match', 'pymax'])
    # tester.clear_log()
    # # tester.make_interface()
    # # tester.refresh_interface()
    # tester.run_PonyGE2()


    # *****Test SGE*****
    tester2=Tester_SGE(n_step = 5,
                     n_init_sample = 5,
                     eval_type = 'dict',
                     max_eval_each=50000,
                       para_list='/util/hyper_para_list_sge.json')
    tester2.give_problem(['supervised_learning'])
    tester2.run_sge()





