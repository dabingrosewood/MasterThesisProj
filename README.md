# Benchmark for Grammatical Evolution(GE) system

## Introdution
This project is the thesis project for my master degrees at Leiden University, which is supervised by Prof. Dr. Thomas bäck and Dr. H. Wang.
The main aim of this project is to compare the performance over different GE and GE-variant system.
Until now, systems include PonyGE2(py3) and SGE(py2). Most of the codes are based on the original code of these systems, and they are modified according to need of this program. For the detail of modifications, please refer to modification.log.  

Every GE system asks for several 'hyper-parameter' to manage the evolving process in the GE system. In order to compare the peak performance for different GE systems, here we use MIP-EGO method to do the hyper-parameter tuning. This module will find the best-suited hyper-parameter setting for each GE system.

## Structure
![image](http://assets.processon.com/chart_image/5c9b935be4b0630a45dc0ca5.png)
In this project, Every tested system will be seen as a independent module. Their hyper-parameter(such like evolutionary settings) are managed  by `management.py` and tuned by calling `MIP-EGO` module. All tuned hyper-parameters are automatically feed into testing systems.
On the other side, all fitness functions for every problem in this test is calling C-implemented Test Suite, with their corresponded interface to different coding languagess. Until now, interfaces of py3 to C and py2 to c are provided.

## Usage
The main program of this project is `management.py` in the root directory. Run with `python3 management.py`
The variable `full_problem_set` represents what problem you are going to test with.

## prerequisite
```
    numpy
    sklearn
    pathos
    cython
    (to be continued...)

```



##How to add new problem and run the test
### 1. write your own fitness function
I. Write your fitness function  `int evaluate_[problem_name](argv[])` or _#include_ your `problem.c` in `cython/fitness.h`.

II. Add the declaration of your evaluate function under `cdef extern from "fitness.h" :`

III. Add the interface function for python program, following the shape of `eval_[problem](argv[])`

example:
```diff
+ cdef extern from "fitness.h" :
+     double rmse(double *prediction_value, double *actual_value,int length);

+ def fitness_rmse(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None):
+     result = rmse(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
+     return result
```


### 2. add new problem for PonyGE2 sys
To run your own problem in PonyGE2 system, you still need to
1. add a fitness class under `PonyGE2/src/fitness`, following the schema of 
```python
from fitness.base_ff_classes.base_ff import base_ff
from fitness.cython.interface import your_fitness_function
class problem_name(base_ff):

    def __init__(self):
        super().__init__()

    @eval_counter
    def evaluate(self, ind, **kwargs):
        return your_fitness_function(**kwargs)
```
2. add a parameter text file under `PonyGE2/src/parameters`
3. copy the BNF file of your problem into `PonyGE2/src/grammars`


### 3. add new problemfor SGE system
To run your own problem in SGE system,you need to write a scirpt python file for each problem you are going to test.
Following code is a good template to start with.
```python
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from util.cython.interface import your_fitness_function

class PROBLEM_NAME:
    def evaluate(self, individual):
        error=your_fitness_function(**kwargs)
        return (error, {})


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    experience_name = "Mux11/"
    grammar = grammar.Grammar("../grammars/BNF_NAME", 5)
    evaluation_function = PROBLEM_NAME()
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)
```
In the case of you are adding a supervised_learning problem, please refer to 

##Appelndix. (TODO)

1.定义测试类,management.py

    def init()                          初始化类属性，测试环境，将Cython内容覆盖到系统测fitness文件夹，并build
    def prepare(problem_set)            读取参数List
    def run()                           calling 针对不同系统的hyper_parameter_tuning, record 参数表和best_fitness
    def analyze()                       数据分析


2. log's information
    under the `log/` directory, there are 2 kinds of different log files

    The first type is like `summary_of_SYSTEM_PROBLEM_MACHINENAME.log`, which includes all tested command and corresponeding  average fitness value and std_dev.

    The second type is like `out_SYSTEM_PROBLEM_UNIXTIME_MACHINE.txt`, every file follows this shape is the best_founded hyperparameter setting for one hyper-parameter tuning test.
