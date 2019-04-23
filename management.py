import sys,os

from shutil import copytree, ignore_patterns,rmtree


def exec_cmd(cmd):
    output = os.popen(cmd)
    print(output.read()+'\n')

def cpy_interface():
    # build cython_implemented package for PonyGE2
    root_wd=os.getcwd()
    source_dir=root_wd+"/cython"
    target_dir=root_wd+"/PonyGE2/src/fitness/cython"

    if os.path.exists(target_dir):
        if os.path.exists(target_dir):
            print("原有文件夹将被删除")
            rmtree(target_dir)
        print("start copying")
        copytree(source_dir,target_dir,ignore_patterns("*.so","*.c","build/*"))
        print("copying is finished")

def clear_ponyge_result():
    result_dir=os.getcwd()+"/PonyGE2/results"
    if os.path.exists(result_dir):
        rmtree(result_dir)



# build_cmd="python3 setup.py build_ext --inplace"


# os.chdir("PonyGE2/src/")
# exec_cmd("python3 ponyge.py --parameter classification.txt")

clear_ponyge_result()