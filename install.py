import subprocess, sys

print("[-] Installing necessary dependencies...")

def python_dependencies():
    pip3_check = subprocess.run(["pip3 --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if pip3_check.returncode == 0:
        print("[+] Pip3 is installed")
    else :
        print("[!] Pip3 is NOT installed -- Installing now...")
        cloning = subprocess.run(["sudo apt-get install -y python3-pip"], stdout=subprocess.DEVNULL, shell=True)
        print("[+] Pip3 was successfully installed")

    print("[-] Installing required packages...")
    subprocess.run(["pip3 install argparse bs4"], shell=True)

def node_dependencies():
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

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def keystore():
    home_dir = get_home_dir()
    keystore_check = subprocess.run([f"ls {home_dir}/.keys"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    if keystore_check.returncode == 0:
        print("[+] Keys directory found.")
    else:
        print("[!] Keys directory NOT found!  Creating now...")
        subprocess.run([f"mkdir {home_dir}/.keys"], shell=True)
        keystore_check = subprocess.run([f"ls {home_dir}/.keys"], shell=True)
        if keystore_check.returncode == 0:
            print("[+] Keys directory created successfully!")
            slack_key = input("[*] Please enter your Slack Token (ENTER to leave black and add later):\n")
            hackerone_key = input("[*] Please enter your HackerOne API Key (Username:API_Key):\n")
            bugcrowd_key = input("[*] Please enter your BugCrowd API Key (Copy Full Key):\n")
            subprocess.run([f"""echo "{slack_key}" > {home_dir}/.keys/slack_web_hook && echo "{hackerone_key}" > {home_dir}/.keys/.hackerone && echo "{bugcrowd_key}" > {home_dir}/.keys/.bugcrowd"""], shell=True)

def main():
    keystore()
    python_dependencies()
    node_dependencies()
    print("[+] Installation complete!")

if __name__ == "__main__":
    main()