import time
import psutil
import pandas as pd
from synchronize import test_proto2, close_zmq2
from commands import poll_zmq2
from utils import FieldReader, CSVReader
from constants import APSIM_DIR, SIMULATION_DIR, FIELDS_FILE, OUTPUT_CSV
from visualization import line_plot, bar_plot

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

it_values = csv_reader.get_columns_data('iteration')
weather_rain_values = csv_reader.get_columns_data('[Weather].Rain')
soil_water_values = csv_reader.get_columns_data(['[Soil].Water.PAW_0', 
                                             '[Soil].Water.PAW_1', 
                                             '[Soil].Water.PAW_2',
                                             '[Soil].Water.PAW_3',
                                             '[Soil].Water.PAW_4',
                                             '[Soil].Water.PAW_5',
                                             '[Soil].Water.PAW_6',])

line_plot(x=it_values, 
          y=list(soil_water_values.values()),
          labels=list(soil_water_values.keys()),
          title="Soil Water over Iterations", 
          xlabel="Iteration", 
          ylabel="Soil Water (mm)", 
          file_name="soil_water_over_iterations")

bar_plot(x=it_values,
         y=weather_rain_values,
         title="Rain over Iterations",
         xlabel="Iteration",
         ylabel="Rain Water (mm)",
         file_name="rain_water_over_iterations_bar",
        )

close_zmq2(apsim)