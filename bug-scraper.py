import requests
import subprocess
import base64
import argparse
import re
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HackerOne:
    def __init__(self, mrp=None):
        self.url = "https://hackerone.com/directory/programs"
        self.class_ = "daisy-link--major"
        self.platform = "HackerOne"
        self.mrp = mrp
        self.link = f"https://hackerone.com/{mrp}"

class BugCrowd:
    def __init__(self, mrp=None):
        self.url = "https://bugcrowd.com/programs"
        self.class_ = "cc-inline-clamp-2"
        self.platform = "BugCrowd"
        self.mrp = mrp
        self.link = f"https://bugcrowd.com/{mrp}"

class MostRecentPrograms:
    def __init__(self, hackerone, bugcrowd, intigriti):
        self.hackerone = hackerone
        self.bugcrowd = bugcrowd
        self.intigriti = intigriti

def get_most_recent_program_obj(program):
    try:
        get_content = subprocess.run([f'node bbdisco.js {program.url}'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        content = get_content.stdout
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.findAll('a', program.class_)
        return links[0]
    except Exception as e:
        print("[!] Something went wrong!  Skipping this round...")
        return False

def send_init_notification():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    message_json = {'text':':bulb::bulb:  Bug Bounty Program Monitoring Server Online!  :bulb::bulb:','username':'BB-Disco','icon_emoji':':bug:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)

def send_slack_notification(program):
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    message_json = {'text':f':fire::fire:  There is a new program on {program.platform}!  Title: *{program.mrp}*  |  Link: {program.link}  :fire::fire:','username':'HackerOne','icon_emoji':':bug:'}
    print(message_json)
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    print(f"[+] New Program Found!  Name: {program.mrp}")
    requests.post(f'https://hooks.slack.com/services/{token}', json=message_json)

def hackerone_check(mrps):
    program = HackerOne(mrps.hackerone)
    mrpo = get_most_recent_program_obj(program)
    if mrpo is False:
        return mrps
    mrp = mrpo.text
    if mrp != mrps.hackerone:
        print(f"[!] New HackerOne Program Found!  {mrp}")
        new_program = HackerOne(mrp)
        send_slack_notification(new_program)
        mrps.hackerone = mrp
        return mrps
    else:
        now = datetime.now()
        formatted_now = now.strftime("%m/%d/%Y, %H:%M:%S")
        print(f"[-] HackerOne -- Same -- {mrp} -- {formatted_now}")
        return mrps

def bugcrowd_check(mrps):
    program = BugCrowd(mrps.bugcrowd)
    mrpo = get_most_recent_program_obj(program)
    if mrpo is False:
        return mrps
    mrp = mrpo.text
    if mrp != mrps.bugcrowd:
        print(f"[!] New BugCrowd Program Found!  {mrp}")
        new_program = BugCrowd(mrp)
        send_slack_notification(new_program)
        mrps.bugcrowd = mrp
        return mrps
    else:
        now = datetime.now()
        formatted_now = now.strftime("%m/%d/%Y, %H:%M:%S")
        print(f"[-] BugCrowd -- Same -- {mrp} -- {formatted_now}")
        return mrps

def get_init_programs():
    hackerone = HackerOne()
    mrpo_hackerone = get_most_recent_program_obj(hackerone)
    mrp_hackerone = mrpo_hackerone.text
    print(f"[-] HackerOne -- Initial Program -- {mrp_hackerone}")
    bugcrowd = BugCrowd()
    mrpo_bugcrowd = get_most_recent_program_obj(bugcrowd)
    mrp_bugcrowd = mrpo_bugcrowd.text
    print(f"[-] BugCrowd -- Initial Program -- {mrp_bugcrowd}")
    send_init_notification()
    return MostRecentPrograms(mrp_hackerone, mrp_bugcrowd, "")

def monitor_mode():
    mrps = get_init_programs()
    while True:
        mrps = hackerone_check(mrps)
        mrps = bugcrowd_check(mrps)
        sleep(600)

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
            if scope_item == "*.*":
                continue
            if "," in scope_item:
                scope_item_list = scope_item.split(",")
                for item in scope_item_list:
                    if data_type == "domains" and item[2:] != "*.":
                        continue
                    clean_item = item.split("/")[0]
                    f.write(f"{clean_item}\n")
            else:
                clean_item = scope_item.split("/")[0]
                f.write(f"{clean_item}\n")

def append_output(data, data_type):
    with open(f'{data_type}.txt', 'a') as f:
        for scope_item in data:
            if " " in scope_item:
                continue
            if scope_item == "https://github.com" or scope_item == "https://play.google.com" or scope_item == "https://itunes.apple.com" :
                continue
            if "," in scope_item:
                scope_item_list = scope_item.split(",")
                for item in scope_item_list:
                    if data_type == "domains" and item[2:] != "*.":
                        continue
                    clean_item = item.replace("https://","").replace("http://","").split("/")[0]
                    f.write(f"{clean_item}\n")
            else:
                clean_item = scope_item.replace("https://","").replace("http://","").split("/")[0]
                f.write(f"{clean_item}\n")

def hackerone():
    init_url = "https://api.hackerone.com/v1/hackers/programs"
    programs = h1_api_call(init_url)
    program_list = []
    counter = 1
    while True:
        for program in programs['data']:
            program_list.append(program['attributes']['handle'])
        print(f"[-] Page {counter} Complete!")
        counter += 1
        try:
            programs = h1_api_call(programs['links']['next'])
        except Exception as e:
            # print(f"[!] Exception: {e}")
            break
    program_count = len(program_list)
    print(f"[+] Programs Discovered: {program_count}")
    url_list = []
    domain_list = []
    for program in program_list:
        print(f"[-] Checking {program} scope for URLs or Domains..")
        program_data = get_h1_domains(program)
        if program_data['relationships']['structured_scopes']:
            for scope_item in program_data['relationships']['structured_scopes']['data']:
                if scope_item['attributes']['asset_type'] == 'URL':
                    clean_url = scope_item['attributes']['asset_identifier'].replace("https://","").replace("http://","")
                    if clean_url[:2] == "*.":
                        domain_list.append(clean_url)
                        print("Domain: " + clean_url)
                    else:
                        url_list.append(clean_url)
                        print("URL: " + clean_url)
        else:
            print(f"[!] No structured scope key:\n{program_data['relationships']}")
    write_output(url_list, 'urls')
    write_output(domain_list, 'domains')

def get_bugcrowd_scope(program_link):
    get_content = subprocess.run([f'node bbdisco.js {program_link}'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    content = get_content.stdout
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.findAll("td", {"data-label": "Target"})
    url_list = []
    domain_list = []
    for link in links:
        scope_target = link.attrs['aria-label'].strip()
        if "*." in scope_target:
            print("Domain: " + scope_target)
            domain_list.append(scope_target)
            continue
        url_regex = r"(^(?:(http:\/\/|https:\/\/)?[a-zA-Z0-9_\-]{1,63}\.)+(?:[a-zA-Z]{1,}))"
        url_check = re.match(url_regex, scope_target)
        if url_check:
            url_tuple = re.findall(url_regex, scope_target)
            # if len(url_tuple) < 1:
            #     modified_url = "www." + scope_target
            #     url_tuple = re.findall(url_regex, modified_url)
            #     url = [x[0] for x in url_tuple]
            #     final_url = url[0].replace("www.","")
            #     print("URL: " + final_url)
            #     continue
            url = [x[0] for x in url_tuple]
            print("URL: " + url[0])
            url_list.append(url[0])
            continue
    append_output(url_list, 'urls')
    append_output(domain_list, 'domains')
        

def bugcrowd():
    ### Note From rs0n: The Bugcrowd API doesn't currently have a way to index all programs, only programs
    ### that the user has joined.  I've submitted a feature request, but until that's done I'm only crawling
    ### the Bugcrowd DOM with this module.
    ###
    # init_url = "https://api.bugcrowd.com/programs?fields%5Borganization%5D=name,programs,targets&fields%5Bprogram%5D=name,organization&fields%5Bprogram_brief%5D=description"
    # api_key = get_bc_api_key()
    # headers = {"Authorization":f"Token {api_key}","Bugcrowd-Version":"2021-10-28"}
    # proxies = {"https":"https://127.0.0.1:8080"}
    # res = requests.get(init_url, headers=headers, proxies=proxies, verify=False)
    # print(res.json())
    init_url = "https://www.bugcrowd.com/bug-bounty-list/"
    get_content = subprocess.run([f'node bbdisco.js {init_url}'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    content = get_content.stdout
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.findAll("th", {"class": "program-Name"})
    program_link_list = []
    for link in links:
        program_link = link.find('a', href=True).get('href')
        program_link_list.append(program_link)
    for program_link in program_link_list:
        if "bugcrowd" in program_link:
            program = program_link.replace("//","").split("/")[1]
            print(f"[-] Checking {program} scope for URLs or Domains..")
            get_bugcrowd_scope(program_link)
    return True

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--disco', help='Discover All URLs, TLDs, and Bug Bounty Program Names', required=False, action='store_true')
    parser.add_argument('--monitor', help='Be Notified of New Bug Bounty Programs', required=False, action='store_true')
    return parser.parse_args()

def main(args):
    if args.disco:
        hackerone()
        bugcrowd()
    if args.monitor:
        print("[-] Entering Monitor Mode...")
        monitor_mode()
    print("[+] Done!")

if __name__ == "__main__":
    args = arg_parse()
    main(args)