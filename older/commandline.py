import subprocess as sp
import os
import path
import sys

path_variables = os.environ['path']
original_cwd = os.getcwd()
cwd = original_cwd
username = os.environ['USERNAME']
internal_command = True


# region custom functions
def cd(dir):
    global cwd

    if path.exists(cwd + dir):
        cwd = dir
        return True, "directory changed"

    if ':' in dir and path.exists(dir):
        cwd = dir
        return True, "directory changed"

    return False, "could not find such directory"


def hello():
    return "hello " + username


internal_functions = {"cd": cd, "hello": hello}

# endregion custom functions


def handle_request(req):
    handle_operators(req)


def handle_operators(req, original=True):
    if not req:
        return

    req = cwd + '\\' + req
    print(f"request is: {req}")
    if '|' in req:
        req_list = req.split('|', 1)
        return pipe(req_list[0], handle_operators(req_list[1], False))
    if '<' in req:
        req_list = req.split('<', 1)
        return stdin(req_list[0], handle_operators(req_list[1], False))
    if '>' in req:
        req_list = req.split('>', 1)
        return stdout(req_list[0], req_list[1])

    if not original:
        return req

    #@todo run
    return


def pipe(program, inputprogram):

    p1 = sp.Popen(["python", program], stdout=sp.PIPE, shell=None)
    p2 = sp.Popen(["python", inputprogram], stdin=p1.stdout, shell=None)
    p1.stdout.close()
    return p2.communicate()[0]


def stdin(program, inputfilename):
    with open(inputfilename, 'rb') as f:
        p1 = sp.Popen(["python", program], stdin=f, shell=None)
        return p1.communicate()[0]


def stdout(program, outptfilename):
    with open(outptfilename, 'wb') as f:
        p1 = sp.Popen(["python", program], stdout=f, shell=None)
        p1.communicate()[0]


def main():
    req = ""
    while req != "exit":
        handle_request(req)
        req = input(f"{username}~[{cwd}]$ ")

    print('====== Terminal Is Killed ======')


if __name__ == "__main__":
    main()