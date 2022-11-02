import requests, subprocess
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def base64_encode(data):
    data_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(data_bytes)
    base64_str = base64_bytes.decode('ascii')
    return base64_str

def get_api_key():
    home_dir = get_home_dir()
    f = open(f'{home_dir}/.keys/.hackerone','r')
    api_key = f.read().strip()
    f.close()
    return api_key

def get_programs(url):
    api_key = get_api_key()
    auth_str = base64_encode(f"r-s0n:{api_key}")
    headers = {"Authorization":f"Basic {auth_str}","Accept":"application/json"}
    # proxies = {"https":"https://127.0.0.1:8080"}
    res = requests.get(url, headers=headers, verify=False)
    return res.json()

def main():
    init_url = "https://api.hackerone.com/v1/hackers/programs"
    programs = get_programs(init_url)
    program_list = []
    counter = 1
    while True:
        for program in programs['data']:
            program_list.append(program['attributes']['name'])
        print(f"[-] Page {counter} Complete!")
        counter += 1
        try:
            programs = get_programs(programs['links']['next'])
        except Exception as e:
            # print(f"[!] Exception: {e}")
            break
    program_count = len(program_list)
    print(f"[+] Programs Discovered: {program_count}")
    print(program_list)
    print("[+] Done!")

if __name__ == "__main__":
    main()