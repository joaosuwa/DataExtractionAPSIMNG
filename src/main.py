import time
import psutil
import pandas as pd
from synchronize import test_proto2, close_zmq2
from commands import send_command, poll_zmq2

apsim_dir = "/home/joaosuwa/projetos/ApsimX"
simulation_dir = f'{apsim_dir}/Tests/Simulation/ZMQ-Sync/DataExtraction/wheat_sorriso_script.apsimx'
apsim = test_proto2(apsim_dir, simulation_dir)
rec = {"iter":[], "mem":[], "time":[]}

for i in range(10):
    start_time = time.time()
    poll_zmq2(apsim['apsim_socket'])
    proc = psutil.Process(apsim['process'].pid)
    mem_info = proc.memory_info().rss
    elapsed_time = time.time() - start_time
    rec["iter"].append(i + 1)
    rec["mem"].append(mem_info)
    rec["time"].append(elapsed_time)

close_zmq2(apsim)
print(pd.DataFrame(rec))