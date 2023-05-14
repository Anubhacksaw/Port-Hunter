import socket
import threading
import argparse
import time
print("""
 .S_sSSs      sSSs_sSSs     .S_sSSs    sdSS_SSSSSSbs         .S    S.    .S       S.    .S_sSSs    sdSS_SSSSSSbs  
.SS~YS%%b    d%%SP~YS%%b   .SS~YS%%b   YSSS~S%SSSSSP        .SS    SS.  .SS       SS.  .SS~YS%%b   YSSS~S%SSSSSP  
S%S   `S%b  d%S'     `S%b  S%S   `S%b       S%S             S%S    S%S  S%S       S%S  S%S   `S%b       S%S       
S%S    S%S  S%S       S%S  S%S    S%S       S%S             S%S    S%S  S%S       S%S  S%S    S%S       S%S       
S%S    d*S  S&S       S&S  S%S    d*S       S&S             S%S SSSS%S  S&S       S&S  S%S    S&S       S&S       
S&S   .S*S  S&S       S&S  S&S   .S*S       S&S             S&S  SSS&S  S&S       S&S  S&S    S&S       S&S       
S&S_sdSSS   S&S       S&S  S&S_sdSSS        S&S             S&S    S&S  S&S       S&S  S&S    S&S       S&S       
S&S~YSSY    S&S       S&S  S&S~YSY%b        S&S             S&S    S&S  S&S       S&S  S&S    S&S       S&S       
S*S         S*b       d*S  S*S   `S%b       S*S             S*S    S*S  S*b       d*S  S*S    S*S       S*S       
S*S         S*S.     .S*S  S*S    S%S       S*S             S*S    S*S  S*S.     .S*S  S*S    S*S       S*S       
S*S          SSSbs_sdSSS   S*S    S&S       S*S             S*S    S*S   SSSbs_sdSSS   S*S    S*S       S*S       
S*S           YSSP~YSSY    S*S    SSS       S*S             SSS    S*S    YSSP~YSSY    S*S    SSS       S*S       
SP                         SP               SP                     SP                  SP               SP        
Y                          Y                Y                      Y                   Y                Y         
                                                                                                                  
    """)
print("\033[5;31;40mPort Hunt v1.0\033[0m")
# Global variables
open_ports = []
lock = threading.Lock()

def scan_ports(host, start_port, end_port):
    global open_ports
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust timeout as needed
        
        result = sock.connect_ex((host, port))
        if result == 0:
            with lock:
                open_ports.append(port)
            
        sock.close()

def get_service_version(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust timeout as needed
        
        sock.connect((host, port))
        sock.send(b'GET / HTTP/1.0\r\n\r\n')
        response = sock.recv(1024)
        sock.close()
        
        return response.decode().split('\r\n')[0]
    except:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port Scanner')
    parser.add_argument('-t', '--target', help='IP address or domain name of the target')
    parser.add_argument('-pf', '--startport',default=0, type=int, help='Starting port')
    parser.add_argument('-pl', '--endport',default=65535, type=int, help='Ending port')
    args = parser.parse_args()
    
    host = args.target
    start_port = args.startport
    end_port = args.endport
    print(f"\033[94mStarted scan on {host}\033[0m")

    # Determine the number of threads to use based on the number of ports
    num_threads = min(100, end_port - start_port + 1)
    ports_per_thread = (end_port - start_port + 1) // num_threads

    # Create and start the threads
    threads = []
    for i in range(num_threads):
        thread_start_port = start_port + i * ports_per_thread
        thread_end_port = thread_start_port + ports_per_thread - 1

        if i == num_threads - 1:
            thread_end_port = end_port  # Adjust the end port for the last thread

        thread = threading.Thread(target=scan_ports, args=(host, thread_start_port, thread_end_port))
        thread.start()
        threads.append(thread)

    start_time = time.time()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()

    execution_time = end_time - start_time
    total_ports = end_port - start_port + 1
    scanned_ports = len(open_ports)
    

    print(f"Open ports on {host}:")
    for port in open_ports:
        service_version = get_service_version(host, port)
        if service_version:
            print(f"Port {port}: {service_version}")
        else:
            print(f"Port {port}: Unknown service")

    print(f"\nScanned {scanned_ports} ports out of {total_ports} total ports.")
    print(f"Execution time: {execution_time:.2f} seconds")
    print("\033[5;31;40mby Anubhab Mukherjee\033[0m")
