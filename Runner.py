import subprocess as sp
import os
import sys
# s


class Runner():
    def __init__(self, script_folder, pathvars, errmsg):
        self.path_variables = pathvars
        self.python_scripts_folder = script_folder
        self.MSG_wrong_path = errmsg

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

    def run(self, p):
        sp.Popen(p)


r = Runner("pythonscripts", os.environ['path'].split(';'), "Path Error")
r.run(r.get_command('calac'))
