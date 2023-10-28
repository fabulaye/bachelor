import time 
def start_timer():
    start=time.time()
    return start

def runtime_test(start_time):
    stop=time.time()
    runtime=stop-start_time
    runtime_format=time.strftime("%H:%M:%S", time.gmtime(runtime))
    return runtime_format