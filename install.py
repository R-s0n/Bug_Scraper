import subprocess, sys

print("[-] Installing necessary dependencies...")

pip3_check = subprocess.run(["pip3 --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if pip3_check.returncode == 0:
    print("[+] Pip3 is installed")
else :
    print("[!] Pip3 is NOT installed -- Installing now...")
    cloning = subprocess.run(["sudo apt-get install -y python3-pip"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Pip3 was successfully installed")

print("[-] Installing required packages...")
subprocess.run(["pip3 install argparse bs4"], shell=True)

node_check = subprocess.run(["node --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if node_check.returncode == 0:
    print("[+] NodeJS is installed")
else :
    print("[!] NodeJS is NOT installed -- Installing now...")
    cloning = subprocess.run(["sudo apt-get install -y nodejs npm"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] NodeJS was successfully installed")
    node_check2 = subprocess.run(["node --version; npm --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if node_check2.returncode == 0:
        print("[+] NodeJS was successfully installed")
    else:
        print("[-] Something went wrong!  Check the stack trace, make any necessary adjustments, and try again.  Exiting...")
        sys.exit(2)

subprocess.run(["npm i puppeteer"], stdout=subprocess.DEVNULL, shell=True)
print("[+] Installation complete!")