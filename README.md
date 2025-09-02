# Ketchlist – Password Wordlist Generator CLI Tool

Ketchlist is a **command-line tool** for generating customized password wordlists. It’s designed for red teamers, penetration testers, and security researchers who need realistic and comprehensive wordlists based on company names, common patterns, leetspeak substitutions, and more.

---

## Features

- Generate passwords from **company names** or custom keywords.
- Supports **leet speak variations** for letters.
- Append or prepend **years, seasons, months**, and **special characters**.
- Include **relation numbers** and combined special character sequences.
- Fully **CLI-based** with verbose mode for detailed output.
- Output saved to a specified file, ready for use with tools like **Hydra**, **John the Ripper**, or **Hashcat**.

---

## Installation

Clone the repository:

git clone https://github.com/Isaam25/Ketchlist.git
cd Ketchlist

Make it executable:

chmod +x Ketchlist.py

## Usage
Basic example:
python3 Ketchlist.py -c "Acme Corp" -o acme_wordlist.txt

Multiple companies:
python3 Ketchlist.py -c "TechCorp" "DataSys" -o combined_wordlist.txt

Custom year range, include months, exclude special characters:
python3 Ketchlist.py -c "MyCompany" -y 2024 -e 2010 --months --no-specials

Include custom relation numbers:
python3 Ketchlist.py -c "CompanyName" -r 456 789 101112 -o custom_wordlist.txt

Enable verbose mode for detailed generation info:
python3 Ketchlist.py -c "ExampleCo" -v

Apply password policies:
python3 Ketchlist.py -c "SecureCorp" --min-length 8 --max-length 16 --require-upper --require-digit
python3 Ketchlist.py -c "TechFirm" --min-length 12 --require-upper --require-lower --require-digit --require-special

##CLI Options
| Flag                | Description                                             |
|--------------------|---------------------------------------------------------|
| `-c, --company`     | Company name(s) to generate wordlist for (**required**) |
| `-o, --output`      | Output file name (default: `wordlist.txt`)              |
| `-y, --year`        | Starting year for generation (default: 2025)            |
| `-e, --end-year`    | Ending year for generation (default: 2015)              |
| `--months`          | Include month names in wordlist                         |
| `--no-seasons`      | Exclude season names from wordlist                      |
| `--no-specials`     | Exclude special character combinations                  |
| `-r, --relnum`      | Relation numbers to include (default: 123, 1)           |
| `-v, --verbose`     | Enable verbose output                                   |
| `--min-length`      | Minimum password length                                 |
| `--max-length`      | Maximum password length                                 |
| `--require-upper`   | Require at least one uppercase letter                  |
| `--require-lower`   | Require at least one lowercase letter                  |
| `--require-digit`   | Require at least one digit                              |
| `--require-special` | Require at least one special character                 |
       |

## DISCLAIMER
This tool is intended for educational and authorized penetration testing purposes only. Do not use it for illegal activities.

