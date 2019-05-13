import os,sys
import re
import plotly.offline as py
py.init_notebook_mode(connected=False)
import plotly.graph_objs as go
import csv
import pandas as pd
import matplotlib.pyplot as plt

from pyecharts import options as opts
from pyecharts.charts import Page, Parallel

import numpy as np


lable=["PROBLEM","EVAL_BUDGET","INITIALISATION","CROSSOVER_PROBABILITY","CROSSOVER","MUTATION","MUTATION_PROBABILITY","MUTATION_EVENT_SUBTREE","MUTATION_EVENT_FlIP","SELECTION_PROPORTION","SELECTION","CODON_SIZE","MAX_GENOME_LENGTH","MAX_INIT_TREE_DEPTH","MAX_TREE_DEPTH","TOURNAMENT_SIZE","POPULATION_SIZE"]
result_classification = []
result_pymax = []
result_string_match = []
result_regression = []

def log_analyzer():
    current_dir = os.getcwd()
    log_dir = current_dir + "/../result/"
    files = os.listdir(log_dir)

    with open("result.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(lable)
        for file in files:
            if file.endswith(".txt"):
                # print("dealing with file ",file,type(file))
                f = open(os.path.join(log_dir, file))
                while 1:
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("xopt"):
                        tmp = line.strip("xopt: [").replace(']\n', '\n').replace("'", "").replace(" ", "")
                        para_list = tmp.split(",")
                        if para_list[-1].endswith("\n"):
                            para_list[-1] = para_list[-1].replace("\n", "").replace("\r", "")


                        print("para_list=", para_list)

                        print("len=", len(para_list), '\n')
                        if len(para_list)==16:
                            writer.writerow(para_list)
                        elif len(para_list)==14:
                            para_list.insert(-2, 0)
                            para_list.insert(-2 , 0)
                            writer.writerow(para_list)
                        else:
                            print("something wrong happens")

                f.close()



def drawer():
    df = pd.read_csv("result.csv")
    from pandas.plotting import parallel_coordinates


    a=plt.figure()
    a.add_subplot(parallel_coordinates(df,'PROBLEM'))
    a.set_size_inches(18.5, 10.5)
    a.show()





def generator(problem):
    # for https://ecomfe.github.io/echarts-examples/public/editor.html?c=parallel-aqi&theme=light
    returne_value=[]
    current_dir = os.getcwd()
    log_dir = current_dir + "/../result/"
    files = os.listdir(log_dir)

    for file in files:
        if file.endswith(".txt"):
            f = open(os.path.join(log_dir, file))
            while 1:
                line = f.readline()
                if not line:
                    break
                if line.startswith("xopt"):
                    tmp = line.strip("xopt: [").replace(']\n', '\n').replace("'", "").replace(" ", "")
                    para_list = tmp.split(",")
                    if para_list[-1].endswith("\n"):
                        para_list[-1] = para_list[-1].replace("\n", "").replace("\r", "")

                    # print("para_list=", para_list)

                    if para_list[0]==problem:
                        if len(para_list) == 17:
                            returne_value.append(para_list)
                        elif len(para_list) == 15:
                            para_list.insert(-3, 0)
                            para_list.insert(-4, 0)
                            returne_value.append(para_list)

                        else:
                            print("something wrong happens")

            f.close()
    return returne_value

"INITIALISATION"

def parallel_constructor():
    def convernter(df2,list):
        # col = 'body_style'
        for col in list:
            strs = df2[col].value_counts()
            value_map = dict((v, i) for i, v in enumerate(strs.index))
            df2[col] = df2.replace({col: value_map})[col]
        return df2


    string_index=["PROBLEM","INITIALISATION","CROSSOVER","MUTATION","SELECTION"]

    df = pd.read_csv("result.csv",header=0)

    df = convernter(df,string_index)

    data = [
        go.Parcoords(
            line=dict(color = df['PROBLEM'],
                   colorscale = 'Jet',
                   showscale = True,
                   reversescale = True,
                   cmin = 0,
                   cmax = 3),
            dimensions=list([
                dict(range=[0, 3],
                     label='PROBLEM', values=df['PROBLEM']),
                dict(range=[0, 2],
                     label='INITIALISATION', values=df['INITIALISATION']),
                dict(range=[0, 3],
                     label='CROSSOVER', values=df['CROSSOVER']),
                dict(range=[0, 1],
                     label='CROSSOVER_PROBABILITY', values=df['CROSSOVER_PROBABILITY']),
                dict(range=[0, 3],
                     label='MUTATION', values=df['MUTATION']),
                dict(range=[0, 1],
                     label='MUTATION_PROBABILITY', values=df['MUTATION_PROBABILITY']),
                dict(range=[0, 5],
                     label='MUTATION_EVENT_SUBTREE', values=df['MUTATION_EVENT_SUBTREE']),
                dict(range=[0, 100],
                     label='MUTATION_EVENT_FlIP', values=df['MUTATION_EVENT_FlIP']),
                dict(range=[0, 1],
                     label='SELECTION', values=df['SELECTION']),
                dict(range=[0, 1],
                     label='SELECTION_PROPORTION', values=df['SELECTION_PROPORTION']),
                dict(range=[0, 50],
                     label='TOURNAMENT_SIZE', values=df['TOURNAMENT_SIZE']),
                dict(range=[210, 2100],
                     label='CODON_SIZE', values=df['CODON_SIZE']),
                dict(range=[100, 1000],
                     label='MAX_GENOME_LENGTH', values=df['MAX_GENOME_LENGTH']),
                dict(range=[0, 25],
                     label='MAX_INIT_TREE_DEPTH', values=df['MAX_INIT_TREE_DEPTH']),
                dict(range=[0, 100],
                     label='MAX_TREE_DEPTH', values=df['MAX_TREE_DEPTH']),
                dict(range=[100, 500],
                     label='POPULATION_SIZE', values=df['POPULATION_SIZE'])
            ])
        )
    ]

    layout = go.Layout(
        plot_bgcolor='#E5E5E5',
        paper_bgcolor='#E5E5E5'
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='parcoords-basic')
    import plotly.io as pio
    pio.write_image(fig, 'fig1.png')



if __name__=="__main__":
    if os.path.exists("result.csv"):
        print("file already exist, no further work on log_analyer.\n")
    else:
        log_analyzer()

    # drawer()
    # print(generator('classification'))
    parallel_constructor()
