import argparse
from scanner import scan_network
import os
import csv

def save_ip_csv(ip_data, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    ip = ip_data['ip']
    filename = os.path.join(output_dir, f"{ip}.csv")

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Porta', 'Serviço', 'Web Service', 'Título'])
        for port_info in ip_data.get('ports', []):
            porta = port_info.get('port')
            servico = port_info.get('service', '')
            webservice = ip_data.get('web_service', 'Não')
            titulo = ip_data.get('title', '')
            writer.writerow([porta, servico, webservice, titulo])

def main():
    parser = argparse.ArgumentParser(description="Scanner de IPs e serviços")
    parser.add_argument('--range', required=True, help='Range de IPs para escanear, ex: 193.136.53.0/24')
    parser.add_argument('--output', choices=['csv', 'both'], default='csv', help='Formato de saída')
    parser.add_argument('--verbose', action='store_true', help='Modo verboso')

    args = parser.parse_args()

    if args.verbose:
        print(f"Começando scan para o range: {args.range}")

    results = scan_network(args.range, verbose=args.verbose)

    if args.output in ('csv', 'both'):
        for ip_data in results:
            if ip_data.get('responded', False):
                save_ip_csv(ip_data)
                if args.verbose:
                    print(f"Arquivo CSV criado para IP {ip_data['ip']}")

if __name__ == '__main__':
    main()
