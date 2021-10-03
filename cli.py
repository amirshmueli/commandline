import subprocess as sp
import os
import sys
from Runner import Runner
# Path 1: system path
# Path 2: internal functions
# Path 3: pythonscripts folder


class Shell():
    def __init__(self):
        self.path_variables = os.environ['path'].split(';')
        self.python_scripts_folder = ".\\pythonscripts"
        self.original_directory = os.getcwd()
        self.cwd = self.original_directory
        self.username = os.environ['USERNAME']
        self.MSG_wrong_path = "Could Not Find Specified Path"
        self.internal_functions = {"ls": self.ls, "cd": self.cd}
        self.runner = Runner(self.python_scripts_folder, self.path_variables,
                             self.MSG_wrong_path)

    def runcli(self):
        req = ""
        while req != "exit":
            self.handle_operators(req)
            req = input(f"{self.username}~[{self.cwd}]$ ")
            print()
        print('====== Terminal Is Killed ======')

    def cd(self, path):
        if os.path.exists(path):
            self.cwd = path
            return

        if (os.path.exists(self.cwd + '\\' + path)):
            self.cwd += '\\' + path
            return

        print(self.MSG_wrong_path)

    def ls(self):
        for e in os.listdir(self.cwd):
            print(e)

    def mkdir(path, name):
        os.mkdir(path + '\\' + name)

    def rmdir(path, name):
        os.remove(path + '\\' + name)

    # handles < | >
    def handle_operators(self, req, original=True):
        if not req:
            return

        req, args_ = req.split(' ', 1)
        req = self.cwd + '\\' + req

        print(f"request is: {req}")

        if '|' in req:
            req_list = req.split('|', 1)
            return self.pipe(req_list[0],
                             self.handle_operators(req_list[1], False))
        if '<' in req:
            req_list = req.split('<', 1)
            return self.stdin(req_list[0],
                              self.handle_operators(req_list[1], False))
        if '>' in req:
            req_list = req.split('>', 1)
            return self.stdout(req_list[0], req_list[1])

        if not original:
            return req

        p = sp.Popen(self.get_command(req), shell=None)
        return p.communicate()[0]

    def run_internal_command(self, funcname):
        pass

    def run(self, funcname):
        if funcname in self.internal_functions:
            pass


def main():
    _shell = Shell()
    _shell.runcli()


if __name__ == "__main__":

    main()