# import requests

# def is_wordpress_site(url):
#     try:
#         indicators = 0

#         # Check for /wp-admin
#         response = requests.get(f"{url}/wp-admin", timeout=5)
#         if response.status_code != 404:
#             indicators += 1
        
#         # Check for /wp-login.php
#         response = requests.get(f"{url}/wp-login.php", timeout=5)
#         if response.status_code != 404:
#             indicators += 1

#         # # Check for /wp-content
#         # response = requests.get(f"{url}/wp-content", timeout=5)
#         # if response.status_code != 404:
#         #     indicators += 1

#         # Check HTML source for WordPress-specific tags
#         response = requests.get(url, timeout=5)
#         if 'wp-content' in response.text or 'wp-includes' in response.text:
#             indicators += 1
#         if '<meta name="generator" content="WordPress' in response.text:
#             indicators += 1

#         # Check HTTP headers
#         if 'x-powered-by' in response.headers and 'WordPress' in response.headers['x-powered-by']:
#             indicators += 1
#         if 'server' in response.headers and 'WordPress' in response.headers['server']:
#             indicators += 1

#         # Check for common WordPress cookies
#         if 'set-cookie' in response.headers:
#             cookies = response.headers['set-cookie']
#             if 'wordpress_logged_in' in cookies or 'wp-settings' in cookies:
#                 indicators += 1

#         # Determine if it's a WordPress site based on multiple indicators
#         return indicators > 2
        
#     except requests.RequestException as e:
#         print(f"Error checking {url}: {e}")
#         return False
    

# def check_sites(site_list):
#     wordpress_sites = []
#     for site in site_list:
#         if is_wordpress_site(site):
#             wordpress_sites.append(site)
#     return wordpress_sites

# if __name__ == "__main__":
#     sites = [
#         "https://raffleleader.com",
#         "https://stackoverflow.com",
#         "https://twitter.com",
#         "https://seashoreflowerfarm.com",
#         "https://google.com",
#         "https://rafflepress.com",
#     ]

#     wp_sites = check_sites(sites)
#     print("WordPress sites:")
#     for wp_site in wp_sites:
#         print(wp_site)

import requests

def is_wordpress_site(url):
    try:
        indicators = 0

        # Check for /wp-admin
        response = requests.get(f"{url}/wp-admin", timeout=5)
        print(f"Checking {url}/wp-admin: {response.status_code}")
        if response.status_code == 200:
            indicators += 1

        # Check for /wp-login.php
        response = requests.get(f"{url}/wp-login.php", timeout=5)
        print(f"Checking {url}/wp-login.php: {response.status_code}")
        if response.status_code == 200:
            indicators += 1

        # Check HTML source for WordPress-specific tags
        response = requests.get(url, timeout=5)
        print(f"Checking {url} main page: {response.status_code}")
        if response.status_code == 200:
            if 'wp-content' in response.text or 'wp-includes' in response.text:
                indicators += 1
            if '<meta name="generator" content="WordPress' in response.text:
                indicators += 1

        # Check HTTP headers
        if 'x-powered-by' in response.headers and 'WordPress' in response.headers['x-powered-by']:
            indicators += 1
        if 'server' in response.headers and 'WordPress' in response.headers['server']:
            indicators += 1

        # Check for common WordPress cookies
        if 'set-cookie' in response.headers:
            cookies = response.headers['set-cookie']
            if 'wordpress_logged_in' in cookies or 'wp-settings' in cookies:
                indicators += 1

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

if __name__ == "__main__":
    sites = [
        "https://raffleleader.com",
        "https://stackoverflow.com",
        "https://twitter.com",
        "https://seashoreflowerfarm.com",
        "https://google.com",
        "https://rafflepress.com",
    ]

    wp_sites = check_sites(sites)
    print("WordPress sites:")
    for wp_site in wp_sites:
        print(wp_site)
