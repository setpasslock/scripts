import ftplib
import argparse
import socket

arg_parser = argparse.ArgumentParser(description="FTP Anonymous Login Checker")
arg_parser.add_argument("-f", "--file", required=True, help="ip file path")

args = vars(arg_parser.parse_args())
hosts = args["file"]

def check_anonymous_login(hostname, timeout=5):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hostname, timeout=timeout)
        ftp.login()  # try
        ftp.quit()
        return True  # Anonymous login successful
    except (ftplib.error_perm, socket.timeout):
        return False  #  Anonymous login failed or timeout
    except Exception as e:
        print(f"An error occured during check: {e}")
        return False

def main(hosts):
    try:
        with open(hosts, 'r') as file:
            hosts = file.readlines()
            for host in hosts:
                host = host.strip()
                if check_anonymous_login(host):
                    print(f"{host}: Anonymous login successful")
                else:
                    print(f"{host}:  Anonymous login failed")
    except FileNotFoundError:
        print("hosts.txt file not found")
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    main(hosts=hosts)
