import json
import os
from BayesOpt.SearchSpace import ContinuousSpace, NominalSpace, OrdinalSpace

def json2space(para_dict):
    if para_dict['type'] == 'NominalSpace':
        locals()[para_dict['name']]=NominalSpace(para_dict['options'], para_dict['name'])
    if para_dict['type'] == 'ContinuousSpace':
        locals()[para_dict['name']]=ContinuousSpace(para_dict['range'], para_dict['name'])
    if para_dict['type'] == 'OrdinalSpace':
        locals()[para_dict['name']]=OrdinalSpace(para_dict['range'], para_dict['name'])


def parameters_reader(root_dir=os.getcwd(),system_name=None):
    if system_name:
        filename = root_dir+"/hyper_para_list_" + system_name + '.json'
        with open(filename, 'r') as load_f:
            data = json.load(load_f)
            for parameters in data:
                # print(type(parameters['options']))

                json2space(parameters)
    else:
        print("No system name was givem")

def get_space(spacename,filename,system_name=None):
    if system_name:
        with open(filename, 'r') as load_f:
            data = json.load(load_f)
            for parameters in data:
                if parameters['name']==spacename:
                    if parameters['type'] == 'NominalSpace':
                        return NominalSpace(parameters['options'],parameters['name'])
                    if parameters['type'] == 'ContinuousSpace':
                        return ContinuousSpace(parameters['range'],parameters['name'])
                    if parameters['type'] == 'OrdinalSpace':
                        return OrdinalSpace(parameters['range'],parameters['name'])

    else:
        print("No system name was givem")
        return

if __name__ == "__main__":
    parameters_reader(system_name="PonyGE2")