# Thesis Project/ Benchmark for Grammatical Evolution(GE) system
This project is the thesis project for my master degrees at Leiden University, which is supervised by Prof. Dr. Thomas bäck and Dr. H. Wang @Leiden University. 

The general aim of this project is to provide a pipeline which can customize problems to build a benchmark to compare different GE and GE-variant systems. 
Every GE system asks for several 'hyper-parameter' to manage the evolving process in the GE system. In order to compare the peak performance for different GE systems, here we use MIP-EGO method to do the hyper-parameter tuning. This module will find the best-suited hyper-parameter setting for each GE system.

Until now, several GE systems has been included, covers PonyGE2(py3) ,SGE(py2) and GGES(c). 
Most codes of these systems are forked from the master branch of these systems on github, and they are modified according to need of this project.


On the other side, this project is still in construction, some parts may not synchronized with the latest version on my personal computer. Please contact me directly if you got any problem or comments.



## Structure
![image](http://assets.processon.com/chart_image/5d2c90f9e4b065dc42a56c41.png)
In this project, Every tested system will be seen as a independent module. Their hyper-parameter(such like evolutionary settings) are managed  by `management.py` and tuned by calling `MIP-EGO` module. All tuned hyper-parameters are automatically feed into testing systems.
On the other side, all fitness functions for every problem in this test is calling C-implemented Test Suite, with their corresponded interface to different coding languagess. Until now, interfaces of py3 to C and py2 to c are provided.

## Usage
To run the test on your own computer/server, please use `git clone https://github.com/dabingrosewood/MasterThesisProj.git`.

The main program of this project is `management.py` in the root directory. So please `cd MasterThesisProj\`, and run it with `python3 management.py` with default settings.

Several variables in `management.py` are best to know before your test:

+ `full_problem_set` : represents what problem you are going to test with.
+ `n_step` : The iteration number of hyper-parameter tuning process.
+ `n_init_sample` : The number of sample point in initialization of hyper-parameter tuning.
+ `max_eval_each` : The maximum number of evaluation function calling for each iteration.

## Prerequisite(python)
```
    numpy
    scikit-learn
    pathos
    cython
    (to be continued...)

```



##How to add new problem and run the test
### 1. write your own fitness function and interface
I. Write your fitness function  `int evaluate_[problem_name](argv[])` or _#include_ your `problem.c` in `cython/fitness.h`.

II. Add the declaration of your evaluate function under `cdef extern from "fitness.h" :` in interface.pyc.

III. Add the interface function for your test system language,  following the scheme of `eval_[problem](argv[])`

example(cython for python2 and python3):
```diff
+ cdef extern from "fitness.h" :
+     double rmse(double *prediction_value, double *actual_value,int length);

+ def fitness_rmse(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None):
+     result = rmse(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
+     return result
```


### 2. add new problem to test system
#### for PonyGE2 system:
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

#### For SGE system:
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
    experience_name = "WHATEVER/"
    grammar = grammar.Grammar("../grammars/BNF_NAME", 5)
    evaluation_function = PROBLEM_NAME()
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)
```
In the case of you are adding a supervised_learning problem, please refer to 


#### For GGES system:
For the test in GGES system, you need to write a test program for your selected problem (in `/demo`),copy your bnf into `/bnf` directory and assign your fitness function's return value  to eval function respectively.
For the reference of these work, please mimic the `/demo/template.c` file.

 After finishing this part, you need to modify the `Makefile` by adding some info of your problem
 ```diff
 BIN:
++  $(BINDIR)/YOUR_PROBLEM
 
 
++  $(BINDIR)/YOUR_PROBLEM: $(DEMO_OBJS) $(OBJDIR)/YOUR_PROBLEM.o $(LIB)
++	@echo linking $@ from $^
++	@$(CC) $(CFLAGS) $^ -o $@ $(LFLAGS)
``` 

*Since the GGES system has some problem to pass its standard output to python3, this part is not used in the thesis project.*


##CAUTION:
For some supervised learning prblem(especially those problem use `eval` function), please confirm that all component in the individual can be recognized by your system.
For instance, when we are using `eval(math_funtion)` to calculate a prediction value, every mathematical characters must be specified in your problem or in system(e.g sin(),cos(),tanh()...).

##Cite us
If you wants to use this project as your own purpose, please also cite these original works and refer to their original address.


https://github.com/PonyGE/PonyGE2

https://github.com/nunolourenco/sge

https://github.com/grantdick/libgges#libgges-grammar-guided-evolutionary-search

