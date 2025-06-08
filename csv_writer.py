import csv
import os

def save_ip_csv(ip_data, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    ip = ip_data['ip']
    filename = os.path.join(output_dir, f"{ip.replace('.', '_')}.csv")

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Porta', 'Serviço', 'Web Service', 'Título'])
        for port_info in ip_data.get('ports', []):
            porta = port_info.get('port')
            servico = port_info.get('service', '')
            webservice = ip_data.get('web_service', 'Não')
            titulo = ip_data.get('title', '')
            writer.writerow([porta, servico, webservice, titulo])
