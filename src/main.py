import time
import psutil
import pandas as pd
from synchronize import test_proto2, close_zmq2
from commands import poll_zmq2
from summary import SummaryCollector

apsim_dir = "/home/joaosuwa/projetos/ApsimX"
simulation_dir = (
    f"{apsim_dir}/Tests/Simulation/ZMQ-Sync/DataExtraction/wheat_sorriso_script.apsimx"
)

apsim = test_proto2(apsim_dir, simulation_dir)
proc = psutil.Process(apsim["process"].pid)

# ── define quais colunas serão salvas (além de "iteration") ──────────────────
FIELDS = ["day", "paw_0", "paw_1", "paw_2", "paw_3", "paw_4", "paw_5", "paw_6"]

start_time = time.time()

with SummaryCollector(output_path="output/summary.csv", fields=FIELDS) as collector:
    poll_zmq2(apsim["apsim_socket"], collector=collector)

elapsed_time = time.time() - start_time
mem_info = proc.memory_info().rss

print(f"\nSimulação concluída em {elapsed_time:.2f}s | Memória: {mem_info / 1024**2:.1f} MB")
print(f"Resultados salvos em output/summary.csv")
print(pd.read_csv("output/summary.csv"))

close_zmq2(apsim)