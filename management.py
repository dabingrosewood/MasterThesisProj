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
        # self.clear_log()
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

    def make_problem(self,problem_name):
        # used to copy necessary bnf, dataset in to target place.
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


    def make_problem(self,problem_name):

        # print('... MAKING PROBLEM')

        if os.path.exists('Benchmark/'+problem_name+'/Supervised/'):
            print(problem_name+"is being MAKED")

            f_datafile = open('GGES/datasets/'+problem_name+'.data','w+')
            f_soursefile_train = open('Benchmark/'+problem_name+'/Supervised/Train.txt','r')
            f_soursefile_test = open('Benchmark/'+problem_name+'/Supervised/Test.txt','r')

            count=0
            for line in f_soursefile_train.readlines():
                if not line.startswith('#'):
                    f_datafile.write(line)
                    count+=1
            sep_flag=count

            for line in f_soursefile_test.readlines():
                if not line.startswith('#'):
                    f_datafile.write(line)
                    count+=1

            with open('GGES/datasets/'+problem_name+'.folds','w+') as fold_file:
                line=''
                for number in range(sep_flag,count):

                    fold_file.write(str(number))
                    fold_file.write('\t')

            f_datafile.close()
            f_soursefile_train.close()
            f_soursefile_test.close()


        # print('... END OF MAKING PROBLEM')


    def give_problem(self,problem_set):
        self.problem_set=problem_set

        #todo:for supervised learning problem, remake the dataset(1,merge train/test file. 2,make .fold file.
        for problem in problem_set:
            self.make_problem(problem)


    def run_gges(self):
        print('\n')
        print("***"*20+"now testing GGES system"+"***"*20)

        hyper_para_tuning_GGES.hyper_parameter_tuning_GGES(self.n_step, self.n_init_sample, self.eval_type, self.max_eval_each, self.problem_set,
                                                      self.para_list)


class TesterManager:
    def __init__(self,test_systems,test_problems,n_step,n_init_sample,eval_type,max_eval_each,para_dict):
        self.test_systems = test_systems
        self.test_problems = test_problems

        self.n_step = n_step
        self.n_init_sample = n_init_sample
        self.eval_type = eval_type
        self.max_eval_each = max_eval_each

        self.para_dict = para_dict

    def run(self):

        base = os.getcwd()

        # clean previous test result
        global_log_cleaner()

        if 'PonyGE2' in self.test_systems:
            # ****Test PonyGE2*****
            tester = Tester_PONYGE2(n_step = n_step,
                                    n_init_sample = n_init_sample,
                                    eval_type=eval_type,
                                    max_eval_each=max_eval_each,
                                    para_list=self.para_dict+'/hyper_para_list_PonyGE2.json'
                                    )
            tester.give_problem(full_problem_set)
            tester.make_interface()
            # tester.refresh_interface()
            tester.run_PonyGE2()
            os.chdir(base)

        if 'SGE' in self.test_systems:
            # ****Test SGE*****
            tester2 = Tester_SGE(n_step=n_step,
                                 n_init_sample=n_init_sample,
                                 eval_type=eval_type,
                                 max_eval_each=max_eval_each,
                                 para_list=self.para_dict+'/hyper_para_list_SGE.json')
            tester2.give_problem(full_problem_set)
            tester2.make_interface()
            # tester2.refresh_interface()
            tester2.run_sge()
            os.chdir(base)

        if 'GGES' in self.test_systems:
            # *****Test GGES*****
            tester3 = Tester_GGES(n_step=n_step,
                                  n_init_sample=n_init_sample,
                                  eval_type=eval_type,
                                  max_eval_each=max_eval_each,
                                  para_list=self.para_dict+'/hyper_para_list_GGES.json')
            tester3.give_problem(full_problem_set)
            tester3.make_interface()
            tester3.refresh_interface()
            tester3.run_gges()
            os.chdir(base)

        print("All test finished, now quitting...")






if __name__ == "__main__":

    base=os.getcwd()

    # clean previous test result
    # global_log_cleaner()


    #here to define the problem for the comparison
    full_problem_set=['mux11','ant','string_match','vladislavleva4']
    full_problem_set=['vladislavleva4']

    #shared parameters
    n_step=100
    n_init_sample=5
    eval_type='dict'
    max_eval_each=50000
    test_sys=['PonyGE2','SGE']

    test=TesterManager(test_sys,full_problem_set,n_step,n_init_sample,eval_type,max_eval_each,'/util')
    test.run()


