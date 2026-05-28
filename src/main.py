import time
import psutil
import pandas as pd
from synchronize import test_proto2, close_zmq2
from commands import poll_zmq2
from utils import FieldReader, CSVReader
from constants import APSIM_DIR, SIMULATION_DIR, FIELDS_FILE, OUTPUT_CSV

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

csv_reader = CSVReader(OUTPUT_CSV)

print(f"\nSimulação concluída em {elapsed:.2f}s | Memória: {mem_mb:.1f} MB")
print(f"Resultados salvos em {OUTPUT_CSV}")
print(csv_reader.df)

close_zmq2(apsim)