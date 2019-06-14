import sys,os
from shutil import copytree, ignore_patterns,rmtree
import hyper_para_tuning,hyper_para_tuning_sge,hyper_para_tuning_GGES
import numpy as np
from util.exec_cmd import exec_cmd



def cpy_interface(target_dir_relative='/PonyGE2/src/fitness/cython'):
    # build cython_implemented package for PonyGE2
    root_wd=os.getcwd()
    source_dir=root_wd+"/cython"

    target_dir=root_wd+target_dir_relative

    if os.path.exists(target_dir):
        if os.path.exists(target_dir):
            print("original dir will be removed.")
            rmtree(target_dir)
        print("start copying")
        os.system('mkdir '+target_dir)
    copytree(source_dir,target_dir,ignore_patterns('*.so',"build/*",".idea/*"))
    print("copying is finished")

def global_log_cleaner(log_dir='log/'):
    try:
        rmtree(log_dir)
    except (FileNotFoundError,NotADirectoryError):
        print("no log need to be cleaned")
    if not os.path.exists('log/'):
        os.mkdir('log/')

class Tester_PONYGE2:
    '''

    '''
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
        print('\n')
        print("***" * 20 + "now testing PonyGE2 system" + "***" * 20)
        hyper_para_tuning.hyper_parameter_tuning_ponyge2(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                         self.para_list)

    def make_problem(self):
        pass


class Tester_SGE:
    def __init__(self,n_step,n_init_sample,eval_type,max_eval_each,para_list='/util/hyper_para_list_SGE.json'):
        self.n_step = n_step
        self.n_init_sample = n_init_sample
        self.eval_type = eval_type
        self.max_eval_each = max_eval_each
        self.para_list = para_list

    def make_interface(self):
        #problem here  and add __init__.py
        if not os.path.exists(os.getcwd() + "/SGE/src/util/cython"):
            cpy_interface('/SGE/src/util/cython')
            build_cmd = "python setup.py build_ext --inplace"
            cd_cmd = 'cd ' + os.getcwd() + "/SGE/src/util/cython"
            exec_cmd(cd_cmd, build_cmd,)
            open(os.getcwd() + "/SGE/src/util/cython/" + "__init__.py", 'a').close()
        else:
            print('interface alrady exist. Pass. IF NOT, delete the folder then retry or use refresh_interface.\n')

    def refresh_interface(self):
        rmtree(os.getcwd()+"/SGE/src/util/cython")
        cpy_interface('/SGE/src/util/cython')
        build_cmd = "python setup.py build_ext --inplace"
        cd_cmd='cd '+os.getcwd()+"/SGE/src/util/cython"
        exec_cmd(cd_cmd, build_cmd)
        open(os.getcwd() + "/SGE/src/util/cython/" + "__init__.py",'a').close()


    def give_problem(self,problem_set):
        self.problem_set=problem_set

    def run_sge(self):
        print('\n')
        print("***"*20+"now testing SGE system"+"***"*20)

        hyper_para_tuning_sge.hyper_parameter_tuning_sge(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                         self.para_list)

    def make_problem(self):
        pass

class Tester_GGES:
    def __init__(self,n_step,n_init_sample,eval_type,max_eval_each,para_list='/util/hyper_para_list_GGES.json'):
        self.n_step = n_step
        self.n_init_sample = n_init_sample
        self.eval_type = eval_type
        self.max_eval_each = max_eval_each
        self.para_list = para_list

    def make_interface(self):
        if not os.path.exists(os.getcwd() + "/GGES/src/interface"):
            cpy_interface('/GGES/src/interface')
        else:
            print('interface alrady exist. Pass. IF NOT, delete the folder then retry or use refresh_interface.\n')

    def refresh_interface(self):
        rmtree(os.getcwd()+'/GGES/src/interface')
        cpy_interface('/GGES/src/interface')

    def give_problem(self,problem_set):
        self.problem_set=problem_set

    def run_gges(self):
        print('\n')
        print("***"*20+"now testing GGES system"+"***"*20)

        hyper_para_tuning_GGES.hyper_parameter_tuning_GGES(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                      self.para_list)

    def make_problem(self):
        pass


if __name__ == "__main__":

    base=os.getcwd()

    # clean previous test result
    global_log_cleaner()


    #here to define the problem for the comparison
    full_problem_set=['mux11','ant','string_match','Vladislavleva4']
    full_problem_set=['ant','string_match','mux11']

    #shared parameter
    n_step=100
    n_init_sample=5
    eval_type='dict'
    max_eval_each=50000

    # ****Test PonyGE2*****
    tester=Tester_PONYGE2(n_step = n_step,
                     n_init_sample = n_init_sample,
                     eval_type = eval_type,
                     max_eval_each=max_eval_each,
                     para_list='/util/hyper_para_list_PonyGE2.json'
                     )
    tester.give_problem(full_problem_set)
    # tester.clear_log()
    # tester.make_interface()
    # tester.refresh_interface()
    # tester.run_PonyGE2()


    os.chdir(base)

    # *****Test SGE*****
    tester2=Tester_SGE(n_step = n_step,
                     n_init_sample = n_init_sample,
                     eval_type = eval_type,
                     max_eval_each=max_eval_each,
                     para_list='/util/hyper_para_list_SGE.json')
    tester2.give_problem(full_problem_set)
    # tester2.make_interface()
    # tester2.refresh_interface()
    # tester2.run_sge()

    os.chdir(base)
    # *****Test GGES*****
    tester3=Tester_GGES(n_step = n_step,
                     n_init_sample = n_init_sample,
                     eval_type = eval_type,
                     max_eval_each=max_eval_each,
                     para_list='/util/hyper_para_list_GGES.json')
    tester3.give_problem(full_problem_set)
    tester3.make_interface()
    # tester3.refresh_interface()
    tester3.run_gges()