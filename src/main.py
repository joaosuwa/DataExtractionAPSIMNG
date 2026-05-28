import time
import psutil
import pandas as pd
from synchronize import test_proto2, close_zmq2
from commands import poll_zmq2
from utils import FieldReader

APSIM_DIR = "/home/joaosuwa/projetos/ApsimX"
SIMULATION_DIR = (
    f"{APSIM_DIR}/Tests/Simulation/ZMQ-Sync/DataExtraction/wheat_sorriso_script.apsimx"
)
FIELDS_FILE  = "data/fields.txt"
OUTPUT_CSV   = "output/summary.csv"

field_reader = FieldReader(FIELDS_FILE)
print(field_reader)
print("Variáveis:", field_reader.variables)

apsim = test_proto2(APSIM_DIR, SIMULATION_DIR)
proc  = psutil.Process(apsim["process"].pid)

start_time = time.time()

poll_zmq2(
    socket=apsim["apsim_socket"],
    field_reader=field_reader,
    output_path=OUTPUT_CSV,
)

elapsed = time.time() - start_time
mem_mb  = proc.memory_info().rss / 1024**2

print(f"\nSimulação concluída em {elapsed:.2f}s | Memória: {mem_mb:.1f} MB")
print(f"Resultados salvos em {OUTPUT_CSV}")
print(pd.read_csv(OUTPUT_CSV))

close_zmq2(apsim)