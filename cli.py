import subprocess as sp
import os
import sys

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

        pass

    def mkdir(path):
        pass

    def rmdir(path):
        pass

    # finds exe files in path
    def find_path_func(self, cmd):
        if '.exe' not in cmd:
            cmd += '.exe'

        for _dir in self.path_variables:
            full_path = _dir + '\\' + cmd
            if os.path.exists(full_path):
                return False, full_path

        return True, self.MSG_wrong_path

    # finds py files in pythonscripts
    def find_python_func(self, cmd):
        if '.py' not in cmd:
            cmd += '.py'

        full_path = self.python_scripts_folder + '\\' + cmd
        if os.path.exists(full_path):
            return False, full_path

        return True, self.MSG_wrong_path

    def get_command(self, c):

        if c in self.internal_functions:
            print(f"Debug: {c} | Internal Command")
            return self.internal_functions[c]

        err, path_ = self.find_python_func(c)
        if not err:
            print(f"Debug: {c} | Python Command")
            return ["python", path_]

        err, path_ = self.find_path_func(c)
        if not err:
            print(f"Debug: {c} | Path Command")
            return [path_]

        return self.MSG_wrong_path

    def pipe(self, program, inputprogram):

        p1 = sp.Popen(self.get_command(program), stdout=sp.PIPE, shell=None)

        p2 = sp.Popen(self.get_command(inputprogram),
                      stdin=p1.stdout,
                      shell=None)
        p1.stdout.close()
        return p2.communicate()[0]

    def stdin(self, program, inputfilename):
        with open(inputfilename.strip(), 'rb') as f:
            p1 = sp.Popen(self.get_command(program), stdin=f, shell=None)
            return p1.communicate()[0]

    def stdout(self, program, outptfilename):
        with open(outptfilename.strip(), 'wb') as f:
            p1 = sp.Popen(self.get_command(program), stdout=f, shell=None)
            return p1.communicate()[0]

    def run_internal_command(self, command, i_=sys.stdin, o_=sys.stdout):
        i, o = sys.stdin, sys.stdout
        sys.stdin = i_
        sys.stdout = o_
        command()
        sys.stdin = i
        sys.stdout = o

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


class ShellCommand():
    pass


'''
class PythonShellOps():
    @staticmethod
    def pipe(program, inputprogram):
        p1 = sp.Popen(["python", program.strip()], stdout=sp.PIPE, shell=None)
        p2 = sp.Popen(["python", inputprogram.strip()],
                      stdin=p1.stdout,
                      shell=None)
        p1.stdout.close()
        return p2.communicate()[0]

    @staticmethod
    def stdin(program, inputfilename):
        with open(inputfilename.strip(), 'rb') as f:
            p1 = sp.Popen(["python", program.strip()], stdin=f, shell=None)
            return p1.communicate()[0]

    @staticmethod
    def stdout(program, outptfilename):
        with open(outptfilename.strip(), 'wb') as f:
            p1 = sp.Popen(["python", program.strip()], stdout=f, shell=None)
            p1.communicate()[0]
'''


def main():
    _shell = Shell()
    _shell.runcli()


if __name__ == "__main__":

    main()