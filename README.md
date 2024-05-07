# nmap4lazy

**nmap4lazy** is a Python script that automates an Nmap discovery scan over all TCP ports. Essentially, it conducts a SYN scan across all TCP ports, extracts the open ports, and performs another version scan to ensure uncommon open ports aren't missed, as can happen with default settings.

# Usage

First, clone the repository and display the help menu.

```bash
git clone https://github.com/duskb1t/nmap4lazy
cd nmap4lazy

sudo python3 nmap4lazy.py --help
```

![Untitled](images/helpmenu.png)

All left is to run the scan

```bash
sudo python3 nmap4lazy.py -t 10.129.229.17
```

![Untitled](images/output1.png)

![Untitled](images/output2.png)