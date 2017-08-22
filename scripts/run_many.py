import time
import os
import subprocess
import glob

PROC_QUEUE = []
PROC_RUNNING = []
UNIQUE_ID = 0
N_PROCS = 3
TARGET_SCRIPT = "run_sim.py"
TIME_0 = time.time()

def config_list():
    #return sorted(glob.glob(*.py"))
    prefix = "scripts/config/config_"
    config_list = [
        prefix+"end_length.py",
        prefix+"max_y_power.py",
        prefix+"tan_delta.py",
        #prefix+"da_scan.py",
    ]
    return config_list

def poll_process_queue():
    global UNIQUE_ID, PROC_RUNNING, PROC_QUEUE
    if is_scarf():
        temp_proc_queue = poll_scarf()
    else:
        temp_proc_queue = poll_laptop()
    while len(temp_proc_queue) < N_PROCS and len(PROC_QUEUE) > 0:
        subproc_args, logname = PROC_QUEUE.pop(0)
        UNIQUE_ID += 1
        job_log = "logs/"+logname+".log"
        if is_scarf():
            subproc_args = ['bsub',
                            '-q', 'scarf-ibis',
                            '-n', '1',
                            '-W', '72:00',
                            '-o', job_log]+subproc_args
            logfile = open("logs/"+logname+".bsub", "w")
        else:
            logfile = open(job_log, "w")
        temp_proc_queue.append(subprocess.Popen(subproc_args,
                               stdout=logfile, stderr=subprocess.STDOUT))
        print "Running", subproc_args, "with log", job_log,
        print "pid", temp_proc_queue[-1].pid, len(PROC_RUNNING)
    PROC_RUNNING = temp_proc_queue

def poll_laptop():
    temp_proc_queue = []
    for proc in PROC_RUNNING:
        if proc.poll() == None:
            temp_proc_queue.append(proc)
        else:
            print "PID", proc.pid, "finished with return code", proc.returncode
    print round(time.time()-TIME_0, 1), "...", "Running", len(PROC_RUNNING), "with", len(PROC_QUEUE), "queued"
    return temp_proc_queue

def poll_scarf():
    global TARGET_SCRIPT
    output = subprocess.check_output(['bjobs', '-w'])
    lines = output.split('\n')[1:]
    script_lines = []
    for line in lines:
        if TARGET_SCRIPT not in line:
            continue
        p_index = line.index('python')
        line = line[p_index:]
        line.split(' ')
        script_lines.append(line)
    return script_lines

def is_scarf():
    uname = subprocess.check_output(['uname', '-a'])
    return uname.find('scarf.rl.ac.uk') > -1

def main():
    if os.getenv("OPAL_EXE_PATH") == None:
        raise ValueError("No OPAL_EXE_PATH set")
    global N_PROCS, TARGET_SCRIPT, UNIQUE_ID
    if is_scarf():
        N_PROCS = 150
    for config in config_list():
        log_file = config.split("/")[-1]
        log_file = log_file[:-3]
        proc_tuple = (["python", "scripts/run_one.py", config], log_file)
        PROC_QUEUE.append(proc_tuple)
    print len(PROC_QUEUE), "jobs"
    while len(PROC_QUEUE) > 0 or len(PROC_RUNNING) > 0:
        poll_process_queue()
        time.sleep(10)

if __name__ == "__main__":
    main()
    



