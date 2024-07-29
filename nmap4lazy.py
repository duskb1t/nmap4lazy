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

def nmap_nse_scan(target, open_ports):
    command = f"/usr/bin/nmap {target} -sVC -p{','.join(open_ports)}"
    print(colored('\n[+]', 'yellow'), colored(f"Command being used:", 'blue'))
    print(colored(f"\n{command}", 'magenta'))
    result = subprocess.check_output(shlex.split(command))
    return result.decode()

def extract_ports(result):
    pattern = r'\d{1,5}\/tcp'
    open_ports = re.findall(pattern, result)
    return [port[:-4] for port in open_ports]

def nmap_all_ports(target, minrate):
    command = f"/usr/bin/nmap {target} -p- -sS -Pn -n --min-rate {minrate}"
    print(colored('\n[+]', 'yellow'), colored(f"Command being used:", 'blue'))
    print(colored(f"\n{command}", 'magenta'))
    process = subprocess.check_output(shlex.split(command))
    return process.decode()

def set_arguments():
    parser = argparse.ArgumentParser(
        description="nmap for lazy people",
        epilog="Example: sudo python3 nmap4lazy.py -t 192.168.45.123",
    )
    parser.add_argument('-t', '--target', dest='target', required=True)
    parser.add_argument('-m', '--min-rate', default=5000, dest='minrate')
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
        minrate = args.minrate

        # first scan
        print(colored('\n[+]', 'yellow'), colored("Scanning all TCP ports...", 'blue'))
        result = nmap_all_ports(target, minrate)
        open_ports = extract_ports(result)
        if not open_ports:
            print(colored("\n[!] Not open ports found. Terminatting scan!", 'yellow'))
            sys.exit(1)
        print(colored('\n[+]', 'yellow'), colored(f"Open ports: ", 'blue'))
        print(colored(f"\n{', '.join(open_ports)}", 'white'))

        # second scan
        print(colored('\n[+]', 'yellow'), colored("NSE Scan in process. This might take a while...", 'blue'))
        result = nmap_nse_scan(target, open_ports)
        print(colored(f"\n{result}", 'white'))
        
        print(colored('[+]', 'yellow'), colored("Script finished successfully", 'blue'))
        sys.exit(0)

    except KeyboardInterrupt:
        print(colored("\n[!] Keyboard interrumpt detected. Quitting!", 'yellow'))
        sys.exit(1)

    finally:
        show_cursor()   

main()
