#!/usr/bin/env python3
"""
Wordlist Generator CLI Tool
Generates password wordlists based on company names and common patterns.
"""

import argparse
import sys
import os
from pathlib import Path

# Base data
default_relnum = [123, 1]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
special_chars = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*",
    "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?",
    "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~",
]
seasons = ["Summer", "Winter", "Spring", "Autumn"]
default_year = 2025

leetspeak = {
    "A": ["4", "@", "^", "Λ"],
    "B": ["8", "|3", "13", "6"],
    "C": ["(", "{", "<"],
    "D": ["Ð"],
    "E": ["3", "€", "£", "&"],
    "F": ["ph"],
    "G": ["6", "9", "(&"],
    "H": ["#"],
    "I": ["1", "!", "|", "eye"],
    "J": [";", "]"],
    "K": ["X"],
    "L": ["1", "£", "7"],
    "M": ["^^", "(V)"],
    "N": ["И"],
    "O": ["0", "()", "*", "°"],
    "P": ["|*"],
    "Q": ["0_", "9"],
    "R": ["|2", "12"],
    "S": ["5", "$", "z"],
    "T": ["7"],
    "U": ["µ", "v"],
    "V": ["√"],
    "W": ["vv", "uu"],
    "X": ["><", "×"],
    "Y": ["¥", "`/", "j"],
    "Z": ["2"]
}

def binary_counter(num_digits):
    """Generate all binary combinations for given number of digits."""
    max_val = (1 << num_digits) - 1
    for num in range(max_val + 1):
        yield format(num, f'0{num_digits}b')

def active_assignment(word, binary):
    """Determine which characters should be replaced based on binary pattern."""
    activ = []
    activelet = []
    for i in range(len(str(binary))):
        if str(binary)[i] == '1':
            activ.append(i)
    for j in range(len(word)):
        if j in activ:
            activelet.append(word[j])
    return [activelet, activ]

def compilation(active_list):
    """Generate all combinations of leetspeak replacements."""
    if not active_list:
        return [[]]
    complist = [[]]
    for ch in active_list:
        if ch.upper() not in leetspeak:
            # If character has no leetspeak equivalent, keep original
            options = [ch]
        else:
            options = leetspeak[ch.upper()]
        new = []
        for base in complist:
            for opt in options:
                new.append(base + [opt])
        complist = new
    return complist

def combine(lis, pos, word):
    """Combine original word with leetspeak replacements."""
    for j in lis:
        comp = ""
        count = 0
        for i in range(len(word)):
            if i not in pos:
                comp += word[i]
            else:
                if count < len(j):  # Safety check
                    comp += j[count]
                    count += 1
                else:
                    comp += word[i]  # Fallback to original character
        yield comp

def leetspk(input_list):
    """Generate all leetspeak variations of input words."""
    for word in input_list:
        word_len = len(word)
        for binary in binary_counter(word_len):
            ls = active_assignment(word, binary)
            combinations = compilation(ls[0])
            for combo in combine(combinations, ls[1], word):
                yield combo

def generate_wordlist(companies, output_file, start_year=None, end_year=2015, include_months=False, include_seasons=True, include_specials=True, relnum=None, verbose=False):
    """Generate comprehensive wordlist based on company names and patterns."""
    if start_year is None:
        start_year = default_year
    if relnum is None:
        relnum = default_relnum
    
    base_words = []
    
    # Add company names
    base_words.extend(companies)
    
    # Add seasons if requested
    if include_seasons:
        base_words.extend(seasons)
    
    # Add months if requested
    if include_months:
        base_words.extend(months)
    
    print(f"Generating wordlist for: {', '.join(companies)}")
    print(f"Output file: {output_file}")
    print(f"Year range: {end_year}-{start_year}")
    
    if verbose:
        print(f"Base words to process: {base_words}")
        print(f"Relation numbers: {relnum}")
        print(f"Include months: {include_months}")
        print(f"Include seasons: {include_seasons}")
        print(f"Include special chars: {include_specials}")
        print(f"Total years to process: {start_year - end_year + 1}")
    
    word_variations = []
    total_words = 0
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # Generate base words with years and leetspeak
            if verbose:
                print("Generating base word variations with years...")
            
            for year in range(start_year, end_year - 1, -1):
                if verbose:
                    print(f"Processing year: {year}")
                
                year_count = 0
                for word in leetspk(base_words):
                    variations = [
                        word + str(year),        # word + full year
                        word,                    # word only
                        word + str(year)[2:]     # word + last two digits
                    ]
                    word_variations.extend(variations)
                    year_count += len(variations)
                
                if verbose:
                    print(f"  Generated {year_count} variations for {year}")
            
            if verbose:
                print(f"Total base variations: {len(word_variations)}")
            
            # Write base variations
            for variation in word_variations:
                f.write(variation + "\n")
                total_words += 1
            
            # Add special character combinations if requested
            if include_specials:
                if verbose:
                    print("Adding special character combinations...")
                
                special_count = 0
                for variation in word_variations:
                    for char in special_chars:
                        f.write(variation + char + "\n")  # word + special char
                        f.write(char + variation + "\n")  # special char + word
                        special_count += 2
                        total_words += 2
                
                if verbose:
                    print(f"Added {special_count} special character combinations")
                
                # Add special chars with relation numbers
                relnum_count = 0
                for num in relnum:
                    num_str = str(num)
                    for char in special_chars:
                        f.write(num_str + char + "\n")  # number + special char
                        f.write(char + num_str + "\n")  # special char + number
                        relnum_count += 2
                        total_words += 2
                
                if verbose:
                    print(f"Added {relnum_count} relation number + special char combinations")
        
        print(f"Wordlist generated successfully: {output_file}")
        if verbose:
            print(f"Total passwords generated: {total_words:,}")
        
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Generate password wordlists based on company names and common patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -c "Acme Corp" -o acme_wordlist.txt
  %(prog)s -c "TechCorp" "DataSys" -o combined_wordlist.txt
  %(prog)s -c "MyCompany" -y 2024 -e 2010 --months --no-specials
  %(prog)s -c "CompanyName" -r 456 789 101112 -o custom_wordlist.txt
        """
    )
    
    parser.add_argument(
        "-r", "--relnum",
        nargs="+",
        type=int,
        help="Relation numbers to include (default: 123, 1)"
    )
    
    parser.add_argument(
        "-c", "--company",
        nargs="+",
        required=True,
        help="Company name(s) to generate wordlist for"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="wordlist.txt",
        help="Output file name (default: wordlist.txt)"
    )
    
    parser.add_argument(
        "-y", "--year",
        type=int,
        default=default_year,
        help=f"Starting year for generation (default: {default_year})"
    )
    
    parser.add_argument(
        "-e", "--end-year",
        type=int,
        default=2015,
        help="Ending year for generation (default: 2015)"
    )
    
    parser.add_argument(
        "--months",
        action="store_true",
        help="Include month names in wordlist"
    )
    
    parser.add_argument(
        "--no-seasons",
        action="store_true",
        help="Exclude season names from wordlist"
    )
    
    parser.add_argument(
        "--no-specials",
        action="store_true",
        help="Exclude special character combinations"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.year < args.end_year:
        print(f"Error: Start year ({args.year}) must be greater than end year ({args.end_year})", file=sys.stderr)
        return 1
    
    # Check if output directory exists
    output_path = Path(args.output)
    if not output_path.parent.exists():
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error creating output directory: {e}", file=sys.stderr)
            return 1
    
    # Generate wordlist
    success = generate_wordlist(
        companies=args.company,
        output_file=args.output,
        start_year=args.year,
        end_year=args.end_year,
        include_months=args.months,
        include_seasons=not args.no_seasons,
        include_specials=not args.no_specials,
        relnum=args.relnum,
        verbose=args.verbose
    )
    
    if success:
        file_size = os.path.getsize(args.output)
        print(f"File size: {file_size:,} bytes")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
