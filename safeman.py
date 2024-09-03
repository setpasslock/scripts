# A pacman script to make safer updates against newly released but potentially corrupted updates.

import subprocess
from datetime import datetime
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
import os
import re
import argparse




pack_list = []


console = Console()
cmd = """pacman -Qu | cut -d ' ' -f 1 | xargs pacman -Si | awk \
        '/^Repository/ {repo=$0} /^Name/ {name=$0} /^Version/ {version=$0} /^Build Date/ {printf "%s | %s | %s | %s\\n", repo, name, version, $0}' | sort -u"""



def clean_line(line):
    cleaned_line = re.sub(r'\s*\|\s*', ' | ', line.strip())
    cleaned_line = re.sub(r'\s*:\s*', ' : ', cleaned_line)
    return cleaned_line




def parse_lines(cleaned_lines):

    for line in cleaned_lines:

        parts = line.split("|")
        repo_part = parts[0]
        ix_d = repo_part.find(":")

        repoName = repo_part[ix_d+2:-1]
        
        name_part = parts[1]
        ix_d = name_part.find(":")
        pName = name_part[ix_d+2:-1]


        version_part = parts[2]
        ix_d = version_part.find(":")
        version = version_part[ix_d+2:-1]
        version = version.replace(" : ", ":")

        buildate_part = parts[3]
        ix_d = buildate_part.find(":")
        buildDate = buildate_part[ix_d+2:-1]
        buildDate = buildDate.replace(" : ", ":")

        pck_list = [repoName, pName, version, buildDate]

        pack_list.append(pck_list)

        



date_format = "%a %d %b %Y %I:%M:%S %p %z"

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        date_str = date_str.rsplit(' ', 1)[0]
        return datetime.strptime(date_str, "%a %d %b %Y %I:%M:%S %p")


def print_table():
    today = datetime.now()

    sorted_list = sorted(pack_list, key=lambda x: parse_date(x[3]))

    table = Table(title="Package List Sorted by Date", style="purple  ")

    table.add_column("ID", style="cyan")
    table.add_column("Repository", style="red")
    table.add_column("Package", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Build Date", style="cyan")
    table.add_column("Days Ago")

    for idx, item in enumerate(sorted_list, start=1):
        # date differance
        item_date = parse_date(item[3])
        days_diff = (today - item_date).days
        
        table.add_row(str(idx), item[0], item[1], item[2], item[3], f"{days_diff} days ago")


    
    console.print(table)

    return sorted_list

def get_user_selection(sorted_list):
    user_input = input("Select IDs (e.g., 1,2,5 or 1-5): ").strip()
    
    selected_packages = []

    try:

        if ',' in user_input:
            indices = [int(x.strip()) for x in user_input.split(',')]
            selected_packages = [sorted_list[i-1][1] for i in indices if 1 <= i <= len(sorted_list)]
        elif '-' in user_input:
            start, end = map(int, user_input.split('-'))
            selected_packages = [sorted_list[i-1][1] for i in range(start, end+1) if 1 <= i <= len(sorted_list)]
        else:
            idx = int(user_input)
            if 1 <= idx <= len(sorted_list):
                selected_packages = [sorted_list[idx-1][1]]

        return selected_packages
    except ValueError:
        print("Invalid char. Operation aborted.")


def approve(pkgs):
    print("")
    console.print("Selected Packages:", style="bold green")
    print("")
    console.print(f"        {pkgs}", style="cyan")
    print("")
    inpp = Prompt.ask("[purple]Do you confirm your choice?[/purple] [Y/n]", default="Y")
    if inpp.lower() == "y":
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description="Script for pacman")
    parser.add_argument("--nosync", action="store_true", help="You pass the synchronization phase (-Syu) but you cannot upgrade. Only to see the packages.")
    args = parser.parse_args()

    if args.nosync:
        noSync = True
    else:
        noSync = False
        os.system("yes no | sudo pacman -Syu")

        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        cleaned_lines = [clean_line(line) for line in output.strip().split("\n")]
        parse_lines(cleaned_lines=cleaned_lines)


    sorted_list = print_table()

    if noSync:
        exit(0)
    else:
        selected_packages = get_user_selection(sorted_list)

        if selected_packages:
            pkgs = ""
            for pkg in selected_packages:
                pkgs += pkg + " "
            
            appr = approve(pkgs=pkgs)

            if appr:
                command = f"sudo pacman -S --needed {pkgs}"
                os.system(command)
            else:
                print("Operation aborted.")
            
        else:
            print("No valid selections were made.")

main()
