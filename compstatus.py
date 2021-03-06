""" A module for getting the status of the host computer (CPU, RAM, GPU, etc.) 
    Everything is presented in percent.
"""

import os
import psutil
from subprocess import Popen, PIPE

def cpu():
    return psutil.cpu_percent()
    
def ram():
    return psutil.virtual_memory().percent
    
def gpu():
    # Returns both GPU utilization and VRAM usage
    args = ["--query-gpu=utilization.gpu,memory.total,memory.used", "--format=csv,noheader,nounits"]
    devices = os.environ.get('CUDA_VISIBLE_DEVICES')
    if devices is not None:
        args.append('--id='+devices)

    p = Popen(["nvidia-smi"] + args, stdout=PIPE)
    output = p.stdout.read().decode('UTF-8')
    lines = output.split('\n')

    assert lines
    line = lines[0]

    util, tot, used = map(int, line.split(", "))
    return util, round(100*float(used)/tot,1)

def disk():
    p = Popen(['df','/data'], stdout=PIPE)
    output = p.stdout.read().decode('UTF-8')
    lines = output.split('\n')
    assert(len(lines)==3)
    line = lines[1].split(' ')
    
    return int(line[-2].strip('%'))

def status():
    gpu_util, gpu_mem = gpu()
    return cpu(), ram(), gpu_util, gpu_mem, disk()
    
if __name__ == '__main__':
    a = status()
    print(a)


