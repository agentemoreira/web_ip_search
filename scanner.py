import socket
import ipaddress
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import COMMON_PORTS, TIMEOUT

def scan_ip(ip):
    ip = str(ip)
    open_ports = []
    websites = []

    for port, service in COMMON_PORTS.items():
        try:
            with socket.create_connection((ip, port), timeout=TIMEOUT):
                open_ports.append({'port': port, 'service': service})
        except:
            continue

    if any(p['port'] in [80, 443] for p in open_ports):
        for proto in ['http', 'https']:
            try:
                url = f"{proto}://{ip}"
                response = requests.get(url, timeout=2, verify=False)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else 'No title'
                websites.append({'url': url, 'title': title})
            except:
                continue

    return {
        'timestamp': datetime.utcnow().isoformat(),
        'ip': ip,
        'open_ports': open_ports,
        'websites': websites
    }

def scan_network(ip_range):
    network = ipaddress.ip_network(ip_range, strict=False)
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_ip, ip) for ip in network.hosts()]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res['open_ports']:
                results.append(res)

    return results
