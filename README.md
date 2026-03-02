# spyder-osint
Spyder OSINT GUI — Graphical open-source intelligence research tool for phone number lookup, IP geolocation, social media reconnaissance, email validation, domain WHOIS, username search, with multi-module architecture and Tkinter-based interface for digital forensics
# Spyder OSINT — GUI Version

Graphical interface for the Spyder OSINT multi-module intelligence research framework.

## Features

- **Phone number lookup** — carrier identification, region detection
- **IP geolocation** — geographic and ISP data from multiple APIs
- **Social media recon** — username search across 100+ platforms
- **Email validation** — deliverability and breach checks
- **Domain WHOIS** — registrant data and DNS records
- **License plate lookup** — vehicle registration queries
- **Username search** — cross-platform profile discovery

## Requirements

- Python 3.9+
- Tkinter (usually bundled with Python)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
2_GUI/
  main.py            Entry point (GUI launcher)
  gui/               Tkinter interface modules
  core/              Core lookup engines
  detection/         Signature analysis and classification
  reports/           Output reports
```

## License

MIT
