//
// Created by rosewood on 2019/3/25.
//
#include <math.h>
#include <string>
#include <algorithm>

//#include "ant.h"
//#include "multiplexer.h"
#ifndef GESUITE_UTIL_H
#define GESUITE_UTIL_H

//for get the length of array
template <class T>
int getArrayLen(T& array)
{

    return (sizeof(array) / sizeof(array[0]));

}


//root mean square
double rmse(double *prediction_value, double *actual_value,int length){
    double fSum = 0;
    for (int i = 0; i < length; ++i)
    {
        fSum += (prediction_value[i] - actual_value[i]) *(prediction_value[i] - actual_value[i]);
    }
    return sqrt(fSum / length);
}

//mean square root
double msr(double* DataR,double *DataC,int Num)
{
    double fSum = 0;
    double meanValue = 0;
    for (int i = 0; i < Num; ++i)
    {
        meanValue += DataR[i];
    }
    meanValue = meanValue / Num;

    for (int i = 0; i < Num; ++i)
    {
        fSum += (DataC[i] - meanValue) *(DataC[i] - meanValue);
    }
    return sqrt(fSum / Num); //MSR
}

//root mean square
double rms(double* Data, int Num)
{
    double fSum = 0;
    for (int i = 0; i < Num; ++i)
    {
        fSum += Data[i] * Data[i];
    }
    return sqrt(fSum/Num);
}


//edit distance,aka 'Levenstein distance'
int editDistance(std::string word1, std::string word2) {
    int n1 = word1.size(), n2 = word2.size();
    int dp[n1 + 1][n2 + 1];
    for (int i = 0; i <= n1; ++i) dp[i][0] = i;
    for (int i = 0; i <= n2; ++i) dp[0][i] = i;
    for (int i = 1; i <= n1; ++i) {
        for (int j = 1; j <= n2; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = std::min(dp[i - 1][j - 1], std::min(dp[i - 1][j], dp[i][j - 1])) + 1;
            }
        }
    }
    return dp[n1][n2];
}

double  f1_score(double *data_pred, double *data_real,int length){
    double TP=0;
    double FN=0;
    double TN=0;
    double FP=0;

    for (int i = 0; i < length ; ++i) {
        if (data_pred[i] == 1 & data_real[i]==1){TP+=1;}
        else if(data_pred[i] == 0 & data_real[i]==0){TN+=1;}
        else if(data_pred[i] == 1 & data_real[i]==0){FP+=1;}
        else if(data_pred[i] == 0 & data_real[i]==1){FN+=1;}
    }

    double f1=2*TP/(2*TP+FN+FP);
    std::cout<<",TP="<<TP<<" ,TN="<<TN<<" ,FN="<<FN<<" ,FP="<<FP<<std::endl;
    return f1;
}




#endif //GESUITE_UTIL_H
