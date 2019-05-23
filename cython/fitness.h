
#include <stdio.h>
#include <string.h>
#include "multiplexer.h"
#include "ant.c"
//#include <malloc.h>
#ifndef GESUITE_UTIL_H
#define GESUITE_UTIL_H


int average_value(int data1,int data2){

    return (data1+data2)/2;
}

double rmse(double *prediction_value, double *actual_value,int length){
    double fSum = 0;
    for (int i = 0; i < length; ++i)
    {
        fSum += (prediction_value[i] - actual_value[i]) *(prediction_value[i] - actual_value[i]);
    }
    return sqrt(fSum / length);
}


int min3(int a,int b,int c)
{
   if(a>b) a=b;
   if(a>c) a=c;
   return a;
}

int min2(int a,int b)
{
   if(a>b) return b;
   else  return a;
}

int editDistance(char* word1, char* word2) {

    int n1 = strlen(word1), n2=strlen(word2);
    int dp[n1 + 1][n2 + 1];
    for (int i = 0; i <= n1; ++i) dp[i][0] = i;
    for (int i = 0; i <= n2; ++i) dp[0][i] = i;
    for (int i = 1; i <= n1; ++i) {
        for (int j = 1; j <= n2; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = min2(dp[i - 1][j - 1], min2(dp[i - 1][j], dp[i][j - 1])) + 1;
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
    return f1;
}

#endif //GESUITE_UTIL_H
