import requests, subprocess
import base64
from bs4 import BeautifulSoup
from time import sleep
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

def get_h1_api_key():
    home_dir = get_home_dir()
    f = open(f'{home_dir}/.keys/.hackerone','r')
    api_key = f.read().strip()
    f.close()
    return api_key

def get_bc_api_key():
    home_dir = get_home_dir()
    f = open(f'{home_dir}/.keys/.bugcrowd','r')
    api_key = f.read().strip()
    f.close()
    return api_key

def h1_api_call(url):
    api_key = get_h1_api_key()
    auth_str = base64_encode(f"{api_key}")
    headers = {"Authorization":f"Basic {auth_str}","Accept":"application/json"}
    # proxies = {"https":"https://127.0.0.1:8080"}
    res = requests.get(url, headers=headers, verify=False)
    return res.json()

def get_h1_soup(program):
    res = requests.get(f'https://hackerone.com/{program}',verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup)

def get_h1_domains(program):
    program_url = f"https://api.hackerone.com/v1/hackers/programs/{program}"
    program_data = h1_api_call(program_url)
    return program_data

def write_output(data, data_type):
    subprocess.run([f"rm {data_type}.txt"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
    with open(f'{data_type}.txt', 'w', encoding='utf-8') as f:
        for scope_item in data:
            if "," in scope_item:
                scope_item_list = scope_item.split(",")
                for item in scope_item_list:
                    if data_type == "fqdns" and item[2:] != "*.":
                        continue
                    f.write(f"{item}\n")
            else:
                f.write(f"{scope_item}\n")

def hackerone():
    init_url = "https://api.hackerone.com/v1/hackers/programs"
    programs = h1_api_call(init_url)
    program_list = []
    program_name_list = []
    counter = 1
    while True:
        for program in programs['data']:
            program_list.append(program['attributes']['handle'])
            program_name_list.append(program['attributes']['name'])
        print(f"[-] Page {counter} Complete!")
        counter += 1
        try:
            programs = h1_api_call(programs['links']['next'])
        except Exception as e:
            # print(f"[!] Exception: {e}")
            break
    program_count = len(program_list)
    print(f"[+] Programs Discovered: {program_count}")
    write_output(program_name_list, "programs")
    url_list = []
    fqdn_list = []
    for program in program_list:
        print(f"[-] Checking {program} scope for URLs or Domains..")
        program_data = get_h1_domains(program)
        if program_data['relationships']['structured_scopes']:
            for scope_item in program_data['relationships']['structured_scopes']['data']:
                if scope_item['attributes']['asset_type'] == 'URL':
                    if scope_item['attributes']['asset_identifier'][0] == "*":
                        fqdn_list.append(scope_item['attributes']['asset_identifier'])
                        print("Domain: " + scope_item['attributes']['asset_identifier'])
                    else:
                        clean_url = scope_item['attributes']['asset_identifier'].replace("https://","").replace("http://","")
                        url_list.append(clean_url)
                        print("URL: " + clean_url)
        else:
            print(f"[!] No structured scope key:\n{program_data['relationships']}")
    write_output(url_list, 'urls')
    write_output(fqdn_list, 'fqdns')
    write_output(program_list, 'programs')

def bugcrowd():
    init_url = "https://api.bugcrowd.com/programs?fields%5Borganization%5D=name,programs,targets&fields%5Bprogram%5D=name,organization&fields%5Bprogram_brief%5D=description"
    api_key = get_bc_api_key()
    headers = {"Authorization":f"Token {api_key}","Bugcrowd-Version":"2021-10-28"}
    proxies = {"https":"https://127.0.0.1:8080"}
    res = requests.get(init_url, headers=headers, proxies=proxies, verify=False)
    print(res.json())

def main():
    hackerone()
    # bugcrowd()
    print("[+] Done!")

if __name__ == "__main__":
    main()