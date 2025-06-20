#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import requests
import re
import os
from datetime import datetime

# GFW list URL
GFWLIST_URL = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
# Output directory
OUTPUT_DIR = "rules"
# Output file name
OUTPUT_FILE = "gfwlist.list"

def fetch_gfwlist():
    """Fetch the GFW list from GitHub"""
    print("Fetching GFW list...")
    response = requests.get(GFWLIST_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch GFW list, status code: {response.status_code}")
    return response.text

def decode_gfwlist(content):
    """Decode the base64 encoded GFW list"""
    print("Decoding GFW list...")
    return base64.b64decode(content).decode('utf-8')

def parse_gfwlist(content):
    """Parse the GFW list and extract domains"""
    print("Parsing GFW list...")
    domains = set()

    # Split the content by lines
    lines = content.splitlines()

    for line in lines:
        # Skip comments, empty lines, and invalid rules
        if line.startswith('!') or line.startswith('[') or line.startswith('@') or not line.strip():
            continue

        # Handle regular domain rules
        if '||' in line:
            domain = line.split('||')[1].split('/')[0]
            # Remove any trailing characters like ^ or $
            domain = re.sub(r'[\^\\].*$', '', domain)
            # Remove wildcard prefix (*.domain)
            domain = re.sub(r'^\*\.', '', domain)
            if domain:
                domains.add(domain)
        # Handle domain keyword rules
        elif '.' in line and not line.startswith('/'):
            # Remove any protocol prefix
            domain = re.sub(r'^(http|https)://', '', line)
            # Extract the domain part
            domain = domain.split('/')[0]
            # Remove any trailing characters
            domain = re.sub(r'[\^\\].*$', '', domain)
            # Remove wildcard prefix (*.domain)
            domain = re.sub(r'^\*\.', '', domain)
            if domain and '.' in domain:
                domains.add(domain)

    return sorted(list(domains))

def convert_to_quantumultx(domains):
    """Convert domains to Quantumult X rule format"""
    print("Converting to Quantumult X format...")
    rules = []

    # Add header with metadata
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules.append(f"# GFW List for Quantumult X")
    rules.append(f"# Updated: {now}")
    rules.append(f"# Total domains: {len(domains)}")
    rules.append("")

    for domain in domains:
        # Use HOST-SUFFIX for domain rules
        rules.append(f"HOST-SUFFIX,{domain},GFWLIST")

    return "\n".join(rules)

def save_rules(content):
    """Save the rules to a file"""
    print("Saving rules...")
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Write the rules to the output file
    with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), 'w') as f:
        f.write(content)

    print(f"Rules saved to {os.path.join(OUTPUT_DIR, OUTPUT_FILE)}")

def main():
    """Main function"""
    try:
        # Fetch the GFW list
        gfwlist_content = fetch_gfwlist()

        # Decode the GFW list
        decoded_content = decode_gfwlist(gfwlist_content)

        # Parse the GFW list
        domains = parse_gfwlist(decoded_content)

        # Convert to Quantumult X format
        rules = convert_to_quantumultx(domains)

        # Save the rules
        save_rules(rules)

        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
