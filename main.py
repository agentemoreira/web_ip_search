import argparse
from scanner import scan_network
from csv_writer import save_ip_csv

def main():
    parser = argparse.ArgumentParser(description="Discover web services in IP ranges")
    parser.add_argument('--range', required=True, help='IP range to scan (ex: 193.136.53.0/28)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        print(f"Starting scan for range: {args.range}")

    results = scan_network(args.range, verbose=args.verbose)

    for ip_data in results:
        if ip_data.get('responded', False):
            save_ip_csv(ip_data)
            if args.verbose:
                print(f"CSV file created for IP {ip_data['ip']}")

if __name__ == '__main__':
    main()
