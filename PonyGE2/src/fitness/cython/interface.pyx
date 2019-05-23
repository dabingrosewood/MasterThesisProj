from __future__ import absolute_import, division, print_function, unicode_literals
# import sys
import numpy as np
cimport numpy as np

# from libcpp.string cimport string

np.import_array()

cdef extern from "fitness.h" :
    double rmse(double *prediction_value, double *actual_value,int length);
    # double msr(double* DataR,double *DataC,int Num);
    # double rms(double* Data, int Num);
    int editDistance(char* word1, char* word2);
    long  f1_score(double *data_pred, double *data_real,int length);

    int average_value(int data1,int data2);

    int evaluate_multiplexer(char *solution, int input_size);
    int evaluate_ant(char *cmd_line)

cdef bytes _bstring(s):
    # functino to convert string to bytes, which is only acceptabel for cython(py3).
    if type(s) is bytes:
        return <bytes>s
    elif isinstance(s, unicode):
        return s.encode('ascii')
    else:
        raise TypeError("expect a string, got %s" % str(type(s)))

def testf(data1,data2):
    print("i am doing the tesst fucnt for interface")
    return average_value(data1,data2)




def fitness_rmse(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None):
    result = rmse(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
    return result


def edit_dis(string1,string2):
    s1=_bstring(string1)
    s2=_bstring(string2)
    return editDistance(s1,s2)

def eval_f1_score(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None, np.ndarray[int,ndim=1,mode="c"] length not None):
    result=f1_score(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
    return result

def eval_multiplexer(phenotype,problem_size):
    return evaluate_multiplexer(_bstring(phenotype),problem_size)

def eval_ant(phenotype):
    return evaluate_ant(_bstring(phenotype))
