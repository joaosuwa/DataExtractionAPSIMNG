import subprocess
import psutil
import time
import zmq

# Set up a listening server on a random port
def test_proto2(apsim_dir, simulation_file=None):
    apsim = {}
    
    # The simulation will connect back to this port:
    context = zmq.Context()
    apsim['apsim_socket'] = context.socket(zmq.REP)
    apsim['apsim_socket'].bind("tcp://0.0.0.0:0")
    apsim['random_port'] = apsim['apsim_socket'].getsockopt(zmq.LAST_ENDPOINT).decode().split(":")[-1]
	
    print("Listening on", apsim['apsim_socket'].getsockopt(zmq.LAST_ENDPOINT))

    apsim_simulation_dir = simulation_file if simulation_file else f"{apsim_dir}/Tests/Simulation/ZMQ-Sync/ZMQ-sync.apsimx"
    
    apsim['process'] = subprocess.Popen([
        "/usr/bin/dotnet",
        f"{apsim_dir}/bin/Debug/net8.0/ApsimZMQServer.dll",
        "-p", apsim['random_port'],
        "-P", "interactive",
        "-f", f"{apsim_simulation_dir}"
    ])
    
    print("Started Apsim process id", apsim['process'].pid)
    
    return apsim

def close_zmq2(apsim):
    apsim['apsim_socket'].close()
    apsim['process'].terminate()
    # process = psutil.Process(apsim['process'].pid)
    # for proc in process.children(recursive=True):
    #     proc.kill()
    # process.kill()