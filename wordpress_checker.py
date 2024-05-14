import requests

def is_wordpress(url):
    try:
        response = requests.get(f"{url}/wp-admin", timeout=5)
        if response.status_code != 404:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False
    

def check_sites(site_list):
    wordpress_sites = []
    for site in site_list:
        if is_wordpress(site):
            wordpress_sites.append(site)
    return wordpress_sites

if __name__ == "__main__":
    sites = [
        "https://raffleleader.com",
        "https://stackoverflow.com",
    ]

    wp_sites = check_sites(sites)
    print("WordPress sites:")
    for wp_site in wp_sites:
        print(wp_site)