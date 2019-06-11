import pandas as pd
import numpy as np
import os,sys
import re


def line_praser_cmd(line):
    if re.findall(r'\[python.*?]',line):
        cmd=re.findall(r'\[python.*?]',line)[0]
        parameter_list=re.findall(r'--([A-Za-z0-9_\.]+)\s+([A-Za-z0-9_\.]+)',cmd)

        dict_constructer={}
        for element in parameter_list:
            dict_constructer[element[0]]=element[1]

        return (dict_constructer)

    else:
        return {}


def line_praser_fitness(line):
    if re.findall(r'fitness=([A-Za-z0-9\.]+)',line):
        fitness=re.findall(r'fitness=([A-Za-z0-9\.]+)',line)[0]
        return fitness
    else:
        return ""






wd_dir=os.getcwd()+'15-04'
files = os.listdir(path=wd_dir)

print("addd=",files)

tmp_dict={}
tmp_fit=""
data=[]
for file in files:
    if not os.path.isdir(file):
        f=open(wd_dir+'/'+file, encoding='utf8', errors='ignore')
        iter_f=iter(f)
        for line in iter_f:
            if line_praser_cmd(line)!={}:
                tmp_dict=line_praser_cmd(line)
            if line_praser_fitness(line)!="":
                tmp_fit=line_praser_fitness(line)
            if tmp_fit!=""  and tmp_dict!={}:
                tmp_dict['fitness']=tmp_fit
                data.append(tmp_dict)
                tmp_dict={}
                tmp_fit=""

print(len(data))
print(data)