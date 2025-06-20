# Quantumult X GFW Rules

This repository automatically generates and updates Quantumult X rules based on the [GFW List](https://github.com/gfwlist/gfwlist).

## What is this?

This project fetches the GFW List (a list of domains blocked by the Great Firewall of China) and converts it to a format that can be used by Quantumult X, a powerful network tool for iOS.

## How it works

1. A GitHub Actions workflow runs daily to fetch the latest GFW List
2. The Python script decodes and parses the GFW List
3. The script converts each domain to Quantumult X rule format
4. The generated rules are saved to the `rules/gfwlist.conf` file
5. Any changes are automatically committed and pushed to this repository

## How to use

### In Quantumult X

1. Open Quantumult X
2. Go to Settings > Filter
3. Add a new filter with the following URL:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/quantumult-x-rules/main/rules/gfwlist.conf
   ```
   (Replace `YOUR_USERNAME` with your GitHub username)
4. Set the policy to your preferred proxy policy
5. Save and enjoy!

### Manual update

If you want to update the rules manually:

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install requests
   ```
3. Run the script:
   ```
   python scripts/gfwlist_to_quantumultx.py
   ```
4. The updated rules will be saved to `rules/gfwlist.conf`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* [GFW List](https://github.com/gfwlist/gfwlist) for providing the list of blocked domains
* [Quantumult X](https://quantumult.app/) for the excellent network tool