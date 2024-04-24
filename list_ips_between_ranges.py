import argparse

arg_parser = argparse.ArgumentParser(description="list the other ip's between two ip ranges.")
arg_parser.add_argument("-s", "--start",required=True, help="start ip")
arg_parser.add_argument("-e", "--end",required=True, help="end ip")

args = vars(arg_parser.parse_args())
start_ip = args["start"]
end_ip = args["end"]


def list_ips_between_ranges(start_ip: str, end_ip: str):
    def ip_to_int(ip):
        return sum(int(x) << (8 * i) for i, x in enumerate(reversed(ip.split('.'))))

    def int_to_ip(num):
        return '.'.join(str((num >> i) & 0xFF) for i in (24, 16, 8, 0))

    if not all(part.isdigit() and 0 <= int(part) < 256 for part in start_ip.split('.')) or not all(part.isdigit() and 0 <= int(part) < 256 for part in end_ip.split('.')):
        raise ValueError("Invalid IP address format.")

    start_int = ip_to_int(start_ip)
    end_int = ip_to_int(end_ip)

    if start_int > end_int:
        raise ValueError("Start IP should be less than or equal to the end IP.")

    ip_list = [int_to_ip(i) for i in range(start_int, end_int + 1)]

    return ip_list


ips_between_range = list_ips_between_ranges(start_ip, end_ip)

for ip in ips_between_range:
    print(ip)
