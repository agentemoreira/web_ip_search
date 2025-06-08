# discover_web

Scanner de rede para descobrir serviços e websites ativos em um range de IPs.

## Autor
agentemoreira

## Como usar

```bash
pip install -r requirements.txt
python3 main.py --range 192.168.1.0/28 --output both --verbose
```

## Saídas

- `output/results.json`
- `output/results.csv`
- Logs em `logs/scan.log`
