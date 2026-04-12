#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import ssl
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SOURCE_URL = "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt"

OUTPUT_PATHS = {
    "qx": os.path.join("rules", "qx", "proxy.list"),
    "clash": os.path.join("rules", "clash", "proxy.yaml"),
}

POLICY_NAME = "PROXY"


def fetch_proxy_list():
    """Fetch the Clash proxy list from jsDelivr."""
    print("Fetching proxy list...")

    def download(context):
        with urlopen(SOURCE_URL, timeout=30, context=context) as response:
            return response.read().decode("utf-8")

    try:
        return download(ssl.create_default_context())
    except HTTPError as error:
        raise Exception(f"Failed to fetch proxy list, status code: {error.code}") from error
    except URLError as error:
        reason = getattr(error, "reason", error)
        if "CERTIFICATE_VERIFY_FAILED" in str(reason):
            print("Retrying without certificate verification...")
            try:
                return download(ssl._create_unverified_context())
            except HTTPError as retry_error:
                raise Exception(
                    f"Failed to fetch proxy list, status code: {retry_error.code}"
                ) from retry_error
            except URLError as retry_error:
                raise Exception(f"Failed to fetch proxy list: {retry_error.reason}") from retry_error

        raise Exception(f"Failed to fetch proxy list: {reason}") from error


def parse_proxy_domains(content):
    """Parse the Clash payload and extract domains."""
    print("Parsing proxy list...")
    domains = set()

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "payload:":
            continue

        if line.startswith("-"):
            line = line[1:].strip()

        line = line.strip("'\"")
        line = re.sub(r"^\+\.", "", line)
        line = re.sub(r"^\.", "", line)
        line = line.split("#", 1)[0].strip()

        if not line or "." not in line:
            continue

        domains.add(line.lower())

    return sorted(domains)


def convert_to_quantumultx(domains):
    """Convert domains to Quantumult X rule format."""
    print("Converting to Quantumult X format...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules = [
        "# Proxy List for Quantumult X",
        f"# Updated: {now}",
        f"# Total domains: {len(domains)}",
        "",
    ]

    for domain in domains:
        rules.append(f"HOST-SUFFIX,{domain},{POLICY_NAME}")

    return "\n".join(rules)


def convert_to_clash_yaml(domains):
    """Convert domains to a Clash rule-provider YAML file."""
    print("Converting to Clash rule-provider format...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rules = [
        "# Proxy List for Clash rule-provider",
        f"# Updated: {now}",
        f"# Total domains: {len(domains)}",
        "payload:",
    ]

    for domain in domains:
        rules.append(f"  - '{domain}'")

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
        proxy_content = fetch_proxy_list()
        domains = parse_proxy_domains(proxy_content)

        outputs = {
            OUTPUT_PATHS["qx"]: convert_to_quantumultx(domains),
            OUTPUT_PATHS["clash"]: convert_to_clash_yaml(domains),
        }

        for output_path, rules in outputs.items():
            save_rules(output_path, rules)

        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
