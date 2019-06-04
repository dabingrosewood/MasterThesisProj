from __future__ import absolute_import, division, print_function, unicode_literals
# import sys
import numpy as np
import warnings
from sklearn.metrics.classification import f1_score as sklearn_f1_score
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

# def eval_f1_score(np.ndarray[double, ndim=1, mode="c"] y not None, np.ndarray[double, ndim=1, mode="c"] yhat not None):
#     print("in cython",y,yhat,"there is")
#     result=f1_score(<double*> np.PyArray_DATA(y),<double*> np.PyArray_DATA(yhat),y.shape[0])
#     return result

def eval_multiplexer(phenotype,problem_size):
    return evaluate_multiplexer(_bstring(phenotype),problem_size)

def eval_ant(phenotype):
    return evaluate_ant(_bstring(phenotype))

def eval_f1_score(y, yhat):
    #this is for temporary usage of f1-score, on which previous one got some problem.

    # if phen is a constant, eg 0.001 (doesn't refer to x), then yhat
    # will be a constant. that will break f1_score. so convert to a
    # constant array.
    if not isinstance(yhat, np.ndarray) or len(yhat.shape) < 1:
        yhat = np.ones_like(y) * yhat

    # convert real values to boolean with a zero threshold
    yhat = (yhat > 0)
    with warnings.catch_warnings():
        # if we predict the same value for all samples (trivial
        # individuals will do so as described above) then f-score is
        # undefined, and sklearn will give a runtime warning and
        # return 0. We can ignore that warning and happily return 0.
        warnings.simplefilter("ignore")
        return sklearn_f1_score(y, yhat, average="weighted")