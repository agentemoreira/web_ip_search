import socket
import ipaddress
import threading
from queue import Queue

def scan_port(ip, port, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def worker(ip, port_queue, results):
    while not port_queue.empty():
        port = port_queue.get()
        if scan_port(ip, port):
            results.append(port)
        port_queue.task_done()

def scan_ports(ip, ports=range(1, 1025), threads=100):
    port_queue = Queue()
    for port in ports:
        port_queue.put(port)

    results = []
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(ip, port_queue, results))
        t.daemon = True
        t.start()
        thread_list.append(t)

    port_queue.join()
    return sorted(results)

def scan_ip(ip, verbose=False):
    ip_str = str(ip)
    open_ports = scan_ports(ip_str)
    if verbose:
        print(f"[✓] {ip_str} Portas abertas: {open_ports}")
    return {
        'ip': ip_str,
        'responded': bool(open_ports),
        'ports': open_ports,
    }

def scan_network(ip_range, verbose=False):
    net = ipaddress.ip_network(ip_range, strict=False)
    results = []
    for ip in net.hosts():
        results.append(scan_ip(ip, verbose))
    return results

