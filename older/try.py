import os
import subprocess
import sys

sys.stdin = sys.pipe
subprocess.Popen(["Python", "printtoscreen"],
                 stdout=subprocess.PIPE).communicate()

while 1:
    try:
        print(input())
    except:
        break
