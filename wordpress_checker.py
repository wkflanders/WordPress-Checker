import requests
from urllib.parse import urlparse, urlunparse
import argparse
import os
import csv
import time

def clean_url(url):
    # Parse the URL
    parsed = urlparse(url)
    # Reconstruct the URL, ensuring no double slashes in the path
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        '/' + parsed.path.lstrip('/'),
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return cleaned.rstrip('/')

def is_wordpress_site(url):
    try:
        indicators = 0

        # Define headers to mimic a typical browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }

        def check_url(endpoint):
            try:
                response = requests.get(f"{url}{endpoint}", headers=headers, timeout=10)
                print(f"Checking {url}{endpoint}: {response.status_code}")
                # Accept status codes that indicate the resource exists
                if response.status_code < 400 or response.status_code == 410:
                    return True
                if response.status_code == 403:
                    # Specifically handle the case where /wp-admin or /wp-login.php returns 403
                    if endpoint not in ["/wp-admin", "/wp-login.php"]:
                        return False
                    return True
            except requests.RequestException as e:
                print(f"Error checking {url}{endpoint}: {e}")
            return False

        # Check for /wp-admin
        if check_url("/wp-admin"):
            indicators += 1

        # Check for /wp-login.php
        if check_url("/wp-login.php"):
            indicators += 1

        # Check HTML source for WordPress-specific tags
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Checking {url} main page: {response.status_code}")
            if response.status_code < 400:
                content = response.text
                if 'wp-content' in content or 'wp-includes' in content:
                    indicators += 1
                if '<meta name="generator" content="WordPress' in content:
                    indicators += 1

                headers = response.headers
                # Check HTTP headers
                if 'x-powered-by' in headers and 'WordPress' in headers['x-powered-by']:
                    indicators += 1
                if 'server' in headers and 'WordPress' in headers['server']:
                    indicators += 1

                # Check for common WordPress cookies
                if 'set-cookie' in headers:
                    cookies = headers['set-cookie']
                    if 'wordpress_logged_in' in cookies or 'wp-settings' in cookies:
                        indicators += 1
        except requests.RequestException as e:
            print(f"Error checking {url} main page: {e}")

        print(f"Indicators for {url}: {indicators}")
        # Determine if it's a WordPress site based on multiple indicators
        return indicators >= 2

    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False


def check_sites(site_list):
    wordpress_sites = []
    for site in site_list:
        if is_wordpress_site(site):
            wordpress_sites.append(site)
    return wordpress_sites

def read_sites_from_csv(file_path, column_name):
    sites = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if column_name in row and row[column_name]:
                    url = row[column_name].strip()
                    if url:  # Check if URL is not empty
                        if not url.startswith(('http://', 'https://')):
                            url = 'https://' + url
                        url = clean_url(url)
                        sites.append(url)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except UnicodeDecodeError as e:
        print(f"Error decoding file {file_path}: {e}")
    
    print(f"Total sites found: {len(sites)}")
    if not sites:
        print("No valid URLs found in the CSV file.")
    return sites

def save_sites_to_csv(sites, output_file):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL'])
            for site in sites:
                writer.writerow([site])
        print(f"Verified sites saved to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check websites for WordPress installation.")
    parser.add_argument('--csv', help='Path to the CSV file', required=True)
    parser.add_argument('--column', help='Name of the column containing URLs', default='Company URL')
    parser.add_argument('--output', help='Path to the output CSV file', default='verified_sites.csv')
    args = parser.parse_args()

    verified_sites = []

    file_path = args.csv
    column_name = args.column
    output_file = args.output

    sites = read_sites_from_csv(file_path, column_name)

    if sites:
        start_time = time.time()
        wp_sites = check_sites(sites)
        elapsed_time = time.time() - start_time

        print("WordPress sites:")
        for wp_site in wp_sites:
            verified_sites.append(wp_site)
            print(wp_site)
        
        save_sites_to_csv(verified_sites, output_file)
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
    else:
        print("No sites to check.")   



