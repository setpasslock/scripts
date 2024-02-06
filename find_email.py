import re
import argparse

arg_parser = argparse.ArgumentParser(description="Email finder")
arg_parser.add_argument("-f", "--file",required=True, help="file name")

args = vars(arg_parser.parse_args())
file_name = args["file"]

def find_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails

def main():
    with open(file_name, 'r') as file:
        text = file.read()
    emails = find_emails(text)
    if emails:
        for email in emails:
            print(email)
    else:
        pass

main()
