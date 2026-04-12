#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import re
import os
import ssl
from datetime import datetime
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

# GFW list URL
GFWLIST_URL = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
# Output paths
OUTPUT_PATHS = {
    "qx": os.path.join("rules", "qx", "gfwlist.list"),
    "clash": os.path.join("rules", "clash", "gfwlist.yaml"),
}

# Policy name used by both rule sets
POLICY_NAME = "GFWLIST"

def is_ip_address(domain):
    """Check if a domain is actually an IP address (with or without port)"""
    # Remove port if present
    if ':' in domain:
        domain = domain.split(':')[0]

    # Check if it's an IPv4 address
    try:
        socket.inet_pton(socket.AF_INET, domain)
        return True
    except socket.error:
        pass

    # Check if it's an IPv6 address
    try:
        socket.inet_pton(socket.AF_INET6, domain)
        return True
    except socket.error:
        pass

    return False

def fetch_gfwlist():
    """Fetch the GFW list from GitHub"""
    print("Fetching GFW list...")

    def download(context):
        with urlopen(GFWLIST_URL, timeout=30, context=context) as response:
            return response.read().decode("utf-8")

    try:
        return download(ssl.create_default_context())
    except HTTPError as error:
        raise Exception(f"Failed to fetch GFW list, status code: {error.code}") from error
    except URLError as error:
        reason = getattr(error, "reason", error)
        if "CERTIFICATE_VERIFY_FAILED" in str(reason):
            print("Retrying without certificate verification...")
            try:
                return download(ssl._create_unverified_context())
            except HTTPError as retry_error:
                raise Exception(
                    f"Failed to fetch GFW list, status code: {retry_error.code}"
                ) from retry_error
            except URLError as retry_error:
                raise Exception(f"Failed to fetch GFW list: {retry_error.reason}") from retry_error

        raise Exception(f"Failed to fetch GFW list: {reason}") from error

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
            # Remove leading dot
            domain = re.sub(r'^\.', '', domain)
            if domain and not is_ip_address(domain):
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
            # Remove leading dot
            domain = re.sub(r'^\.', '', domain)
            if domain and '.' in domain and not is_ip_address(domain):
                domains.add(domain)

    return sorted(list(domains))

def convert_to_rule_format(domains, rule_prefix, title):
    """Convert domains to a rule format."""
    print(f"Converting to {title} format...")
    rules = []

    # Add header with metadata
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules.append(f"# GFW List for {title}")
    rules.append(f"# Updated: {now}")
    rules.append(f"# Total domains: {len(domains)}")
    rules.append("")

    for domain in domains:
        rules.append(f"{rule_prefix},{domain},{POLICY_NAME}")

    return "\n".join(rules)

def convert_to_clash_rule_provider(domains):
    """Convert domains to a Clash rule-provider YAML file."""
    print("Converting to Clash rule-provider format...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules = [
        "# GFW List for Clash rule-provider",
        f"# Updated: {now}",
        f"# Total domains: {len(domains)}",
        "payload:",
    ]

    for domain in domains:
        # Clash domain providers use wildcard-style suffix matching.
        rules.append(f"  - '+.{domain}'")

    return "\n".join(rules)

def save_rules(output_path, content):
    """Save the rules to a file"""
    print("Saving rules...")
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the rules to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Rules saved to {output_path}")

def main():
    """Main function"""
    try:
        # Fetch the GFW list
        gfwlist_content = fetch_gfwlist()

        # Decode the GFW list
        decoded_content = decode_gfwlist(gfwlist_content)

        # Parse the GFW list
        domains = parse_gfwlist(decoded_content)

        outputs = {
            OUTPUT_PATHS["qx"]: convert_to_rule_format(domains, "HOST-SUFFIX", "Quantumult X"),
            OUTPUT_PATHS["clash"]: convert_to_clash_rule_provider(domains),
        }

        for output_path, rules in outputs.items():
            save_rules(output_path, rules)

        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
