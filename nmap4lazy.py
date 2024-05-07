#!/usr/bin/env python3

# Author: duskb1t

import argparse
import os
import re
import shlex
import subprocess
import sys
from termcolor import colored

def show_cursor():
    bin_path = "/usr/bin/tput"
    if os.path.exists(bin_path):
        subprocess.run(["/usr/bin/tput", "cnorm"])

def hide_cursor():
    bin_path = "/usr/bin/tput"
    if os.path.exists(bin_path):
        subprocess.run(["/usr/bin/tput", "civis"])

def is_root():
    return os.getuid() == 0

def simple_address_validation(address):
    pattern = r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'
    if re.match(pattern, address):
        return True
    return False

def nmap_nse_scan(target, open_ports):
    command = f"/usr/bin/nmap {target} -sVC -p{','.join(open_ports)}"
    print(colored(f"\n[+] Command being used:", 'magenta'))
    print(f"\n{command}")
    result = subprocess.check_output(shlex.split(command))
    return result.decode()

def extract_ports(result):
    pattern = r'\d{1,5}\/tcp'
    open_ports = re.findall(pattern, result)
    return [port[:-4] for port in open_ports]

def nmap_all_ports(target):
    command = f"/usr/bin/nmap {target} -p- -sS -Pn -n --min-rate 5000"
    print(colored(f"\n[+] Command being used:", 'magenta'))
    print(f"\n{command}")
    process = subprocess.check_output(shlex.split(command))
    return process.decode()

def set_arguments():
    parser = argparse.ArgumentParser(
        description="nmap for lazy people",
        epilog="Example: sudo python3 nmap4lazy.py -t 192.168.45.123",
    )
    parser.add_argument('-t', '--target', dest='target', required=True)
    args = parser.parse_args()
    return args

def main():
    hide_cursor()
    try:
        if not is_root():
            print(colored("\n[!] This script must be run as root", 'yellow'))
            sys.exit(1)

        args = set_arguments()
        target = args.target

        if not simple_address_validation(target):
            print(colored(f"\n[!] {target} is not a valid ip address", 'yellow'))
            sys.exit(1)

        # first scan
        print(colored("\n[+] Scanning all TCP ports...", 'magenta'))
        result = nmap_all_ports(target)
        open_ports = extract_ports(result)
        if not open_ports:
            print("\n[!] Not open ports found. Terminatting scan!")
            sys.exit(1)
        print(colored(f"\n[+] Open ports: ", 'magenta'))
        print(f"\n{', '.join(open_ports)}")

        # second scan
        print(colored("\n[+] NSE Scan in process. This might take a while...", 'magenta'))
        result = nmap_nse_scan(target, open_ports)
        print(colored("\n[+] NSE Scan results: ", 'magenta'))
        print(f"\n{result}")
        
        print(colored("[+] Script finished successfully", 'magenta'))
        sys.exit(0)

    except KeyboardInterrupt:
        print(colored("\n[!] Keyboard interrumpt detected. Quitting!", 'yellow'))
        sys.exit(1)

    finally:
        show_cursor()   

main()