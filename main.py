import argparse
from scanner import scan_network
from utils import save_results, setup_logging
import logging

def parse_args():
    parser = argparse.ArgumentParser(description="Scan a range of IPs and discover hosted websites.")
    parser.add_argument('--range', required=True, help='IP range in CIDR notation (e.g., 192.168.1.0/24)')
    parser.add_argument('--output', choices=['json', 'csv', 'both'], default='json', help='Output format')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logging.info(f"Scanning IP range: {args.range}")

    results = scan_network(args.range)
    save_results(results, args.output)

    logging.info("Scan completed.")

if __name__ == '__main__':
    main()
