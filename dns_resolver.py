import argparse
import dns.resolver
import time
from prettytable import PrettyTable
import ipaddress
import requests

last_dict = {}

# CLOUDFLARE_IP_RANGES = [
#     "173.245.48.0/20",
#     "103.21.244.0/22",
#     "103.22.200.0/22",
#     "103.31.4.0/22",
#     "141.101.64.0/18",
#     "108.162.192.0/18",
#     "190.93.240.0/20",
#     "188.114.96.0/20",
#     "197.234.240.0/22",
#     "198.41.128.0/17",
#     "162.158.0.0/15",
#     "104.16.0.0/13",
#     "104.24.0.0/14",
#     "172.64.0.0/13",
#     "131.0.72.0/22"
# ]



def get_cloudflare_ip_ranges():
    print("Fetching CF IP ranges, be patient...")
    url = "https://www.cloudflare.com/ips-v4/"
    response = requests.get(url)
    if response.status_code == 200:
        print("okey, let's go!")
        return response.text.splitlines()
    else:
        print("Error fetching Cloudflare IP ranges")
        return []
    
CLOUDFLARE_IP_RANGES = get_cloudflare_ip_ranges()

def is_cloudflare_ip(ip):
    for ip_range in CLOUDFLARE_IP_RANGES:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range):
            return True
    return False

def add_to_dict(key, value):
    if key not in last_dict:
        last_dict[key] = []

    if value not in last_dict[key]:
        last_dict[key].append(value)

def print_dict(dictionary):
    for key, values in dictionary.items():
        values_str = ", ".join(map(str, values)) 
        print(f"{key} : {values_str}")

def read_domains_from_file(file_path):
    domains = []
    with open(file_path, 'r') as file:
        for line in file:
            domain = line.strip()
            domains.append(domain)
    return domains

def send_rdns_queries(domains, dns_servers, use_table=False):
    table = PrettyTable(["Domain", "DNS Server", "Result", "Cloudflare"])
    for domain in domains:
        for dns_server in dns_servers:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]
            resolver.timeout = 10  # 10 ideal
            resolver.lifetime = 20 # 20 ideal
            try:
                time.sleep(0.1)
                answer = resolver.resolve(domain, 'A')
                for ip in answer:
                    iscf = is_cloudflare_ip(ip=ip)
                    if iscf == True:
                        iscf = "Yes"
                    else:
                        iscf = "No"

                    result = f"{domain} | {dns_server} | {ip}"
                    if use_table:
                        table.add_row([domain, dns_server, ip, iscf])
                    else:
                        print(result)
                    add_to_dict(key=domain, value=ip)
            except dns.resolver.NXDOMAIN:
                iscf = "Unknown"
                result = f"{domain} | {dns_server} | \033[91mNo such domain\033[0m "
                
                if use_table:
                    table.add_row([domain, dns_server, " \033[91mNo such domain\033[0m ", iscf])
                else:
                    print(result)
            except dns.resolver.NoAnswer:
                iscf = "Unknown"
                result = f"{domain} | {dns_server} | \033[91mNo DNS record found\033[0m"
                

                if use_table:
                    table.add_row([domain, dns_server, " \033[91mNo DNS record found\033[0m ", iscf])
                else:
                    print(result)
            except dns.resolver.LifetimeTimeout:
                iscf = "Unknown"
                result = f"{domain} | {dns_server} | \033[91mThe DNS operation timed out\033[0m"
                
                if use_table: 
                    table.add_row([domain, dns_server, " \033[91mThe DNS operation timed out\033[0m ", iscf])
                else:
                    print(result)
            except dns.exception.Timeout:
                iscf = "Unknown"
                result = f"{domain} | {dns_server} | \033[91mDNS query timed out\033[0m"
                
                if use_table:
                    table.add_row([domain, dns_server, " \033[91mDNS query timed out\033[0m ", iscf])
                else:
                    print(result)
            except dns.resolver.NoNameservers:
                iscf = "Unknown"
                result = f"{domain} | {dns_server} | \033[91mNo Name Servers\033[0m"
                
                if use_table:
                    table.add_row([domain, dns_server, " \033[91mNo Name Servers\033[0m ", iscf])
                else:
                    print(result)
    
    if use_table:
        print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send rDNS queries to domains using specified DNS servers.")
    parser.add_argument("file", help="Path to the file containing subdomains/domains.")
    parser.add_argument("--table", action="store_true", help="Display results in a table format.")
    args = parser.parse_args()

    dns_servers_list = ['1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4', '76.76.2.0', '76.76.10.0', '9.9.9.9', '149.112.112.112', '208.67.222.222', '208.67.220.220', '94.140.14.14', '94.140.15.15', '185.228.168.9', '185.228.169.9', '76.76.19.19', '76.223.122.150']
    domains_list = read_domains_from_file(args.file)
    
    if domains_list:
        send_rdns_queries(domains_list, dns_servers_list, use_table=args.table)
        print("========================================================")
        print_dict(dictionary=last_dict)
    else:
        print("Please specify DNS servers using the --dns_servers argument.")
