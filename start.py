import subprocess
import threading
import time
import socket


def monitor_subprocess(process, command):
    while not exit_event.is_set():
        if process.poll() is not None:
            print(f"Process for {command} has stopped. Restarting...")
            process = subprocess.Popen(command)
        time.sleep(1)

def user_input_handler():
    user_input = input("Type 'q' to quit: ")
    if user_input.lower() == 'q':
        exit_event.set()

def send_shutdown_message():
    shutdown_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    port = 9999
    shutdown_message = "shutdown"
    shutdown_socket.sendto(shutdown_message.encode('utf-8'), (host, port))
    shutdown_socket.close()

exit_event = threading.Event()

blossom_process = subprocess.Popen(["python", "./blossom/start_with_hgr.py"])
hgr_process = subprocess.Popen(["python", "./HGR/HGR_Stub.py"])

blossom_monitor_thread = threading.Thread(target=monitor_subprocess, args=(blossom_process, ['python', './Blossom/start_with_hgr.py']), daemon=True)
hgr_monitor_thread = threading.Thread(target=monitor_subprocess, args=(hgr_process, ['python', './HGR/HGR_Stub.py']), daemon=True)

blossom_monitor_thread.start()
hgr_monitor_thread.start()

input_thread = threading.Thread(target=user_input_handler, daemon=True)
input_thread.start()

exit_event.wait()

send_shutdown_message()

time.sleep(1)

if blossom_process.poll() is None:
    blossom_process.terminate()

if hgr_process.poll() is None:
    hgr_process.terminate()

blossom_process.wait()
hgr_process.wait()

print("All subprocesses have been terminated. Exiting...")
