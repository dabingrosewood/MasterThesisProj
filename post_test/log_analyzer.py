import os,sys
import re
import plotly.plotly as py
import plotly.graph_objs as go
import csv
import pandas as pd
import matplotlib.pyplot as plt

lable=["PROBLEM","INITIALISATION","CROSSOVER_PROBABILITY","CROSSOVER","MUTATION","MUTATION_PROBABILITY","MUTATION_EVENT_SUBTREE","MUTATION_EVENT_FlIP","SELECTION_PROPORTION","SELECTION","CODON_SIZE","MAX_GENOME_LENGTH","MAX_INIT_TREE_DEPTH","MAX_TREE_DEPTH","TOURNAMENT_SIZE","POPULATION_SIZE"]
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
                        if len(para_list) == 16:
                            returne_value.append(para_list)
                        elif len(para_list) == 14:
                            para_list.insert(-3, 0)
                            para_list.insert(-4, 0)
                            returne_value.append(para_list)

                        else:
                            print("something wrong happens")

            f.close()
    return returne_value
if __name__=="__main__":
    if os.path.exists("result.csv"):
        print("file already exist, no further work on log_analyer.\n")
    else:
        log_analyzer()
    # drawer()
    # print(generator('classification'))
