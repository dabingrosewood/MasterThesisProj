import os,sys

def exec_cmd(*args):
    cmd=""
    for element in args:
        cmd = cmd + element
        cmd=cmd+ " && "

    cmd=cmd.rstrip(" && ")
    output = os.popen(cmd)
    print(output.read()+'\n')