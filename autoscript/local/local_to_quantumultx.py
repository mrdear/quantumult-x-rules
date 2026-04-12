#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import ssl
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SOURCE_URL = "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt"

OUTPUT_PATHS = {
    "qx": os.path.join("rules", "qx", "local.list"),
    "clash": os.path.join("rules", "clash", "local.yaml"),
}

POLICY_NAME = "DIRECT"


def fetch_local_cidrs():
    """Fetch the Clash LAN CIDR list from jsDelivr."""
    print("Fetching local CIDR list...")

    def download(context):
        with urlopen(SOURCE_URL, timeout=30, context=context) as response:
            return response.read().decode("utf-8")

    try:
        return download(ssl.create_default_context())
    except HTTPError as error:
        raise Exception(f"Failed to fetch local CIDR list, status code: {error.code}") from error
    except URLError as error:
        reason = getattr(error, "reason", error)
        if "CERTIFICATE_VERIFY_FAILED" in str(reason):
            print("Retrying without certificate verification...")
            try:
                return download(ssl._create_unverified_context())
            except HTTPError as retry_error:
                raise Exception(
                    f"Failed to fetch local CIDR list, status code: {retry_error.code}"
                ) from retry_error
            except URLError as retry_error:
                raise Exception(f"Failed to fetch local CIDR list: {retry_error.reason}") from retry_error

        raise Exception(f"Failed to fetch local CIDR list: {reason}") from error


def parse_local_cidrs(content):
    """Parse the Clash payload and extract CIDR rules."""
    print("Parsing local CIDR list...")
    cidrs = set()

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "payload:":
            continue

        if line.startswith("-"):
            line = line[1:].strip()

        line = line.strip("'\"")
        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$", line) or ":" in line:
            cidrs.add(line)

    return sorted(cidrs)


def convert_to_quantumultx(cidrs):
    """Convert CIDRs to Quantumult X rule format."""
    print("Converting to Quantumult X format...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules = [
        "# Local CIDR List for Quantumult X",
        f"# Updated: {now}",
        f"# Total cidrs: {len(cidrs)}",
        "",
    ]

    for cidr in cidrs:
        rule_type = "IP-CIDR6" if ":" in cidr else "IP-CIDR"
        rules.append(f"{rule_type},{cidr},{POLICY_NAME},no-resolve")

    return "\n".join(rules)


def convert_to_clash_yaml(cidrs):
    """Convert CIDRs to a Clash rule-provider YAML file."""
    print("Converting to Clash rule-provider format...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules = [
        "# Local CIDR List for Clash rule-provider",
        f"# Updated: {now}",
        f"# Total cidrs: {len(cidrs)}",
        "payload:",
    ]

    for cidr in cidrs:
        rules.append(f"  - '{cidr}'")

    return "\n".join(rules)


def save_rules(output_path, content):
    """Save the rules to a file."""
    print("Saving rules...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Rules saved to {output_path}")


def main():
    """Main function."""
    try:
        local_content = fetch_local_cidrs()
        cidrs = parse_local_cidrs(local_content)

        outputs = {
            OUTPUT_PATHS["qx"]: convert_to_quantumultx(cidrs),
            OUTPUT_PATHS["clash"]: convert_to_clash_yaml(cidrs),
        }

        for output_path, rules in outputs.items():
            save_rules(output_path, rules)

        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
