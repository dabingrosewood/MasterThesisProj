# introdution
My thesis project is aim to compare different GE and GE-variant system.
The systems be compared includes: PonyGE2(python), SGE(to be continued). Most of codes are based on the the original code of these system and be modified. Detailed information can be found in modification_log files.


# Procedure to add new problem
(Fitness funntion)
1. Write your fitness function  `int evaluate_[problem_name](argv[])` or _#include_ your `problem.h` in `cython/fitness.h`.

2. Add the declaration of your evaluate function under `cdef extern from "fitness.h" :`
    
3. Add the interface function for python program, folling the shape of `eval_[problem](argv[])`
       

```diff
+ cdef extern from "fitness.h" :
+     double rmse(double *prediction_value, double *actual_value,int length);
    
+ def fitness_rmse(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None):
+     result = rmse(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
+     return result
```
