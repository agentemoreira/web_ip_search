import json
import csv
import os
import logging

def setup_logging(verbose=False):
    log_level = logging.DEBUG if verbose else logging.INFO
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/scan.log"),
            logging.StreamHandler()
        ]
    )

def save_results(results, format):
    os.makedirs("output", exist_ok=True)
    if format in ('json', 'both'):
        with open("output/results.json", "w") as f:
            json.dump(results, f, indent=2)

    if format in ('csv', 'both'):
        with open("output/results.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "ip", "port", "service", "url", "title"])
            for item in results:
                for port in item['open_ports']:
                    writer.writerow([
                        item['timestamp'], item['ip'], port['port'], port['service'], '', ''
                    ])
                for site in item['websites']:
                    writer.writerow([
                        item['timestamp'], item['ip'], '', '', site['url'], site['title']
                    ])
