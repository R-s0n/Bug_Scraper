# Bug Scraper

The Bug Scraper is designed to help Bug Bounty Researchers find valid targets for both [Wide-Band and Narrow-Band Testing](https://www.linkedin.com/posts/harrison-richardson-cissp-oswe-msc-7a55bb158_bugbounty-webapplicationsecurity-cybersecurity-activity-6849314055283466240-ppxn?utm_source=share&utm_medium=member_desktop). 

At this time, this tool contains two modules:

### Discovery Module

The Discovery Module uses a combination of API Calls and DOM Scraping to build a list of all valid URLs and Domains listed in public programs on HackerOne and BugCrowd.  Running this module will output two TXT files, `domains.txt` and `urls.txt`, with these wordlists. 

### Monitor Module

The Monitor Module periodically (30 min. intervals) checks HackerOne and BugCrowd for new public programs.  When a new program is discovered, Bug Scraper will send a Slack message to a web hook alerting you of the new program.

******************************************************************************************************
    I AM NOT RESPONSABLE FOR HOW YOU USE THIS TOOL.  DON'T BE A DICK!                     
******************************************************************************************************

### Install

The install script included in this repo is designed to work on the latest version of [Kali Linux](https://www.kali.org/get-kali/).  To run Bug Scraper on Windows/Mac, please make sure you have the following dependencies installed:

- Python3 (and pip3)
- Python Modules:
    - argparse
    - bs4
- NodeJS (and npm)
- NPM Packages:
    - puppeteer

You will also need to manually create the `.keys` folder in your home directory and add the following files:

```
.keys
|    slack_web_hook
|    .hackerone
|    .bugcrowd
```

These files should contain your API Keys for each service.  Below are examples of the correct formatting.

Slack Web Hook - [RAW_TOKEN]

`T01EJL4T8RZ/B02CQAWLY2F/Y513AokrRCZXj60lf46OoQge`

HackerOne API Key - [USERNAME]:[API_KEY]

`rs0n:uyFIUtMeajuBFPYxKQ9LZaQFP+2KPqMc45Jg64Som4k=`

BugCrowd API Key - [RAW_TOKEN]

`sdfwnpiwjf:_L5soTaruwfdviJyoxquAmjq_E874_uLm7ePTcKTRJj7EnDK8E9LgdIbdPXv2LnHjaliefjz`

For Kali Linux users, simply run the install script included in this repo:

    python3 install.py
    
### Usage

    python3 bug-scraper.py [--disco] [--monitor]

-----------------------------------------------------------------------------------------------------------------
|   Module    |    Flag     |  Required  |                               Notes                                  |
|-------------|-------------|------------|----------------------------------------------------------------------|
|   Discover  |  --disco    |     no     | Builds a list of Domains and URLs listed as valid Bug Bounty Targets |
|   Monitor   |  --monitor  |     no     | Monitors BugCrowd and HackerOne for new public programs              |
-----------------------------------------------------------------------------------------------------------------