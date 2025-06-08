import socket
import ipaddress
import threading
from queue import Queue
import requests

WEB_SERVICE_PORTS = [
    21, 22, 25, 80, 110, 143, 443, 465, 587, 993, 995, 8080, 8443, 8888, 3000, 5000, 7000, 9000
]

SERVICE_MAP = {
    21: 'FTP',
    22: 'SSH',
    25: 'SMTP',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    465: 'SMTP SSL',
    587: 'SMTP TLS',
    993: 'IMAP SSL',
    995: 'POP3 SSL',
    8080: 'HTTP-alt',
    8443: 'HTTPS-alt',
    8888: 'HTTP-alt',
    3000: 'Web App',
    5000: 'Web App',
    7000: 'Web App',
    9000: 'Web App',
}

def scan_port(ip, port, timeout=0.3):
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

def scan_ports(ip, ports=WEB_SERVICE_PORTS, threads=30):
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

def check_web_service(ip, port):
    # Apenas tenta http/https nos ports típicos HTTP
    if port not in [80, 8080, 443, 8443, 8888, 3000, 5000, 7000, 9000]:
        return False, ''

    protocols = []
    if port in [443, 8443]:
        protocols.append('https')
    else:
        protocols.append('http')

    for proto in protocols:
        url = f"{proto}://{ip}:{port}"
        try:
            resp = requests.get(url, timeout=2, verify=False)
            if resp.status_code == 200:
                start = resp.text.find('<title>')
                end = resp.text.find('</title>')
                title = resp.text[start+7:end].strip() if start != -1 and end != -1 else ''
                return True, title
        except:
            continue
    return False, ''

def scan_ip(ip, verbose=False):
    ip_str = str(ip)
    open_ports = scan_ports(ip_str)
    result = {
        'ip': ip_str,
        'responded': bool(open_ports),
        'ports': [],
        'web_service': 'Não',
        'title': ''
    }

    if not open_ports:
        if verbose:
            print(f"[✗] {ip_str} não respondeu nas portas testadas")
        return result

    for port in open_ports:
        service = SERVICE_MAP.get(port, '')
        result['ports'].append({'port': port, 'service': service})

    # Verifica webservice nas portas abertas
    for port_info in result['ports']:
        port = port_info['port']
        has_web, title = check_web_service(ip_str, port)
        if has_web:
            result['web_service'] = 'Sim'
            result['title'] = title
            break

    if verbose:
        ports_str = ', '.join(f"{p['port']}({p['service']})" for p in result['ports'])
        print(f"[✓] {ip_str} respondeu - Portas abertas: {ports_str}")

    return result

def scan_network(ip_range, verbose=False):
    net = ipaddress.ip_network(ip_range, strict=False)
    results = []
    for ip in net.hosts():
        results.append(scan_ip(ip, verbose))
    return results
