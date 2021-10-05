import subprocess as sp
import os
import sys


class Shell():
    def __init__(self):
        self._default_stdin = sys.stdin
        self._default_stdout = sys.stdout
        self.path_variables = os.environ['path'].split(';')
        self.python_scripts_folder = ".\\pythonscripts"
        self.original_directory = os.getcwd()
        self.cwd = self.original_directory
        self.username = os.environ['USERNAME']

        self.MSG_wrong_path = "Could Not Find Specified Path"
        self.MSG_permission_error = "Permission Denied"
        self.internal_functions = {
            "ls": self.ls,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "rmdir": self.rmdir
        }

    def runcli(self):
        req = ""
        while req != "exit":
            self.handle_operators(req)
            req = input(f"{self.username}~[{self.cwd}]$ ")
            print()
        print('====== Terminal Is Killed ======')

    def handle_operators(self, query):
        if not query:
            return

        print(f"request is: {query}")
        if '|' in query:
            req_list = query.split('|', 1)
            self.pipe(req_list[0].strip(), req_list[1].strip())
        elif '<' in query:
            req_list = query.split('<', 1)
            self.stdin(req_list[0].strip(), req_list[1].strip())
        elif '>' in query:
            req_list = query.split('>', 1)
            self.stdout(req_list[0].strip(), req_list[1].strip())
        else:
            self.run(query)

    def run(self, command):
        p = self.isInternal(command)
        if p:
            p()
        else:
            sp.Popen(self.get_command(command)).communicate()

    # region inops
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

    # endregion inops
    def pipe(self, p1, p2):
        p1 = self.isInternal(p1)
        if p1:
            self._iPipe(p1, p2)

    def stdin(self, p1, inputfile):
        p1 = self.isInternal(p1)
        if p1:
            self._iStdin(p1, inputfile)

    def stdout(self, p1, outputfile):
        p1 = self.isInternal(p1)
        if p1:
            self._iStdout(p1, outputfile)

    def isInternal(self, program):
        if program in self.internal_functions:
            return self.internal_functions[program]

        return None

    # external operators

    # region external
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
        err, path_ = self.find_python_func(c)
        if not err:
            print(f"Debug: {c} | Python Command")
            return ["python", path_]

        err, path_ = self.find_path_func(c)
        if not err:
            print(f"Debug: {c} | Path Command")
            return [path_]

        raise ValueError(self.MSG_wrong_path)

    def _xPipe(self, program, inputprogram):

        p1 = sp.Popen(self.get_command(program), stdout=sp.PIPE, shell=None)

        p2 = sp.Popen(self.get_command(inputprogram),
                      stdin=p1.stdout,
                      shell=None)
        p1.stdout.close()
        return p2.communicate()[0]

    def _xStdin(self, program, inputfilename):
        with open(inputfilename.strip(), 'rb') as f:
            p1 = sp.Popen(self.get_command(program), stdin=f, shell=None)
            return p1.communicate()[0]

    def _xStdout(self, program, outptfilename):
        with open(outptfilename.strip(), 'wb') as f:
            p1 = sp.Popen(self.get_command(program), stdout=f, shell=None)
            return p1.communicate()[0]

    # endregion external

    # region internal operators
    def _iPipe(self, program, inputprogram):
        pass  #not supported

    def _iStdin(self, program, inputfilename):
        with open(inputfilename) as newf:
            # save old stdin
            oldin = sys.stdin
            sys.stdin = newf
            program()
            sys.stdin = oldin

    def _iStdout(self, program, outptfilename):
        with open(outptfilename, 'w') as newf:
            # save old stdout
            oldout = sys.stdout
            sys.stdout = newf
            program()
            sys.stdout = oldout
            newf.close()

    # endregion internal operators

    def error_handler(self, e):
        # return handlers to default
        sys.stdout = self._default_stdout
        sys.stdin = self._default_stdin

        print(e)


def main():
    _shell = Shell()
    _shell.runcli()


if __name__ == "__main__":
    main()