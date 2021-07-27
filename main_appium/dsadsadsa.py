import os,signal

out=os.popen("ps aux | grep xx.py").read()

for line in out.splitlines():
    print(line)
    if 'BcexServices.py' in line:
        pid = int(line.split()[1])
        print(pid)
        os.kill(pid,signal.SIGKILL)

def kill(pid):
    try:
        a = os.kill(pid, signal.SIGKILL)
        print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))

    except OSError:
        print('没有如此进程!!!')