import re, requests, time, sys, os, random
from os import path
from concurrent.futures import ThreadPoolExecutor, as_completed
from user_agent import generate_user_agent

# --------------------------
# DEFINE COLOR CODES
# --------------------------
RED = '\033[1;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[2;32m'
CYAN = '\033[2;36m'
LIGHT_BLUE = '\033[1;34m'
P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = "\033[1;31m"   
X = '\033[1;33m'
F = '\033[2;32m'
L = "\033[1;95m"
C = '\033[2;35m'
A = '\033[2;39m'
P = "\x1b[38;5;231m"
J = "\x1b[38;5;208m"
J1 = '\x1b[38;5;202m'
J2 = '\x1b[38;5;203m'
J21 = '\x1b[38;5;204m'
J22 = '\x1b[38;5;209m'
F1 = '\x1b[38;5;76m'
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
P2 = '\x1b[38;5;190m'
# Expected success response from a report
expected_response = '"status_code":0,"status_msg":"Thanks for your feedback"'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --------------------------
# PROXY HELPER FUNCTIONS
# --------------------------
def format_proxy(proxy):
    """
    Ensure proxy string starts with a proper protocol.
    Supports socks5, socks4, and http.
    If missing, assumes http://.
    """
    proxy = proxy.strip()
    if not (proxy.startswith("http://") or proxy.startswith("https://") or 
            proxy.startswith("socks5://") or proxy.startswith("socks4://")):
        return "http://" + proxy
    return proxy

TEST_URL = "https://httpbin.org/ip"
PROXY_TIMEOUT = 1
MAX_THREADS = 400

def check_proxy(proxy_url):
    """Test a single proxy by trying to fetch TEST_URL."""
    formatted = format_proxy(proxy_url)
    proxies = {"http": formatted, "https": formatted}
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=PROXY_TIMEOUT)
        if response.status_code == 200:
            return proxy_url, True
    except Exception:
        pass
    return proxy_url, False

def check_proxies_concurrently(proxy_list):
    """Concurrently test all proxies and return the list of working ones."""
    working = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(check_proxy, p): p for p in proxy_list}
        for future in as_completed(future_to_proxy):
            proxy, status = future.result()
            if status:
                working.append(format_proxy(proxy))
    return working

# --------------------------
# MAIN MENU
# --------------------------
clear_screen()
print(YELLOW + '''
 
░█████╗░██╗░░██╗██╗░░░██╗░█████╗░
██╔══██╗██║░░██║╚██╗░██╔╝██╔══██╗
██║░░╚═╝███████║░╚████╔╝░██║░░██║
██║░░██╗██╔══██║░░╚██╔╝░░██║░░██║
╚█████╔╝██║░░██║░░░██║░░░╚█████╔╝
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░  TikTok
- By CHYO
- Instagram: @ix.chyo
- Telegram: t.me/chyoo1
💀💀💀💀💀💀💀💀 
1-[Report Content]
2-[Spam or Harassment]
3-[Under 13]
4-[Fake Information - Alias]
5-[Hate Speech]
6-[Pornographic]
7-[Terrorism Organizations]
8-[Self Harm]
9-[Harassment or Bullying - Someone I Know]
10-[Violence]
12-[Random Reports]
13-[Random Reports with Proxies]
14-[Frauds And Scams]
15-[Dangerous and challenges acts]
16-[Report Spam]
💀💀💀💀💀💀💀💀
------------------------------------------
''')

try:
    option = int(input(CYAN + "[?] Choose report type: "))
except ValueError:
    print(RED + "Please enter a valid number")
    sys.exit(0)

# Valid options are now: 1-10, 12, 13, 14, 15 and 16.
if option not in [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16]:
    print(RED + f"No such option: {option}")
    sys.exit("Instagram: @chyoo1")

# --------------------------
# DETERMINE REPORT MODE
# --------------------------
if option == 12:
    random_mode = True
    proxy_mode = False
    report_type = None  # Randomly select per request.
elif option == 13:
    random_mode = True
    proxy_mode = True
    report_type = None
else:
    random_mode = False
    proxy_mode = False
    report_type = option

clear_screen()

# --------------------------
# LOAD SESSION IDS
# --------------------------
use_file = input(CYAN + "[?] Do you want to load session IDs from a file? (Y/N): ").strip().lower()
sessions = []
if use_file == 'y':
    fixed_file = "sessions.txt"
    if not path.isfile(fixed_file):
        print(RED + f"Fixed session file '{fixed_file}' not found!")
        sys.exit(0)
    with open(fixed_file, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s:
                sessions.append(s)
else:
    try:
        num = int(input(CYAN + "[?] How many session IDs do you want to use? : "))
    except ValueError:
        print(RED + "Please enter a valid number")
        sys.exit(0)
    for i in range(num):
        s = input(CYAN + f'Enter session ID number {i+1}: ')
        sessions.append(s.strip())

# --------------------------
# IF PROXY MODE, LOAD AND CHECK PROXIES
# --------------------------
working_proxies = []
if proxy_mode:
    proxy_file = input(CYAN + "[?] Enter proxy file path: ").strip()
    if not path.isfile(proxy_file):
        print(RED + f"Proxy file '{proxy_file}' not found!")
        sys.exit(0)
    proxy_list = []
    with open(proxy_file, 'r', encoding='utf-8') as pf:
        for line in pf:
            p = line.strip()
            if p:
                proxy_list.append(p)
    if not proxy_list:
        print(RED + "No proxies loaded from file!")
        sys.exit(0)
    print(GREEN + f"[*] Checking {len(proxy_list)} proxies. Please wait...")
    working_proxies = check_proxies_concurrently(proxy_list)
    if not working_proxies:
        print(RED + "No working proxies found!")
        sys.exit(0)
    else:
        print(GREEN + f"[✔] {len(working_proxies)} working proxies found.\n")

# --------------------------
# GET TARGET USERNAME & SLEEP TIME
# --------------------------
username = input(CYAN + '[?] Enter target username:\n').strip()
try:
    sleep_time = int(input(CYAN + '[?] Enter sleep time (e.g., 5 or 10): \n'))
except ValueError:
    print(RED + "Please enter a valid number for sleep time")
    sys.exit(0)

# --------------------------
# SESSION VALIDITY CHECK & SAVE VALID SESSIONS
# --------------------------
check_url = ('https://api16-normal-c-alisg.tiktokv.com/passport/account/info/v2/'
             '?scene=normal&multi_login=1&account_sdk_source=app&passport-sdk-version=19&'
             'os_api=25&device_type=A5010&ssmix=a&manifest_version_code=2018093009&dpi=191&'
             'carrier_region=JO&uoo=1&region=US&app_name=musical_ly&version_name=7.1.2&'
             'timezone_offset=28800&ts=1628767214&ab_version=7.1.2&residence=SA&'
             'cpu_support64=false&current_region=JO&ac2=wifi&ac=wifi&app_type=normal&'
             'host_abi=armeabi-v7a&channel=googleplay&update_version_code=2018093009&'
             '_rticket=1628767221573&device_platform=android&iid=7396386396296286392&'
             'build_number=7.1.2&locale=en&op_region=SA&version_code=200705&'
             'timezone_name=Asia%2FShanghai&cdid=f61ca549-c9ee-450b-90da-8854423b74e7&'
             'openudid=3e5afbd3f6dde322&sys_region=US&device_id=7296396296396396393&'
             'app_language=en&resolution=576*1024&device_brand=OnePlus&language=en&'
             'os_version=7.1.2&aid=1233&mcc_mnc=2947')
base_headers = {
    'Host': 'api16-normal-c-alisg.tiktokv.com',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': generate_user_agent()
}

valid_sessions_file = "valid_sessions.txt"
valid_session_count = 0
expired_session_count = 0
checked_valid_sessions = []

print(GREEN + "\n[*] Checking session validity...")
for s in sessions:
    h = base_headers.copy()
    h['Cookie'] = 'sessionid=' + s
    try:
        resp = requests.get(check_url, headers=h, timeout=1)
    except Exception as e:
        print(RED + f"Error checking session {s}: {e}")
        continue
    if '"session expired, please sign in again"' in resp.text:
        expired_session_count += 1
        print(RED + "Session expired: " + s)
    elif 'user_id' in resp.text:
        valid_session_count += 1
        checked_valid_sessions.append(s)
        print(GREEN + "Session valid")
if not checked_valid_sessions:
    print(RED + "No valid sessions found!")
    sys.exit(0)
sessions = checked_valid_sessions

print(YELLOW + f"\nValid sessions count: {valid_session_count}")
print(YELLOW + f"Expired sessions count: {expired_session_count}\n")
with open(valid_sessions_file, 'w', encoding='utf-8') as f:
    for sess in sessions:
        f.write(sess + "\n")
print(GREEN + f"[✔] Valid sessions saved to {valid_sessions_file}\n")
clear_screen()
# --------------------------
# GET TARGET USER ID FROM USERNAME
# --------------------------
head = {
    'Host': 'www.tiktok.com',
    'User-Agent': generate_user_agent(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Te': 'trailers',
    'Connection': 'close',
}
req = requests.get(f'https://www.tiktok.com/@{username}?lang=en', headers=head)
try:
    target_ID = re.findall(r'"user":{"id":"(.*?)"', req.text)[0]
except:
    print(RED + "User not found or banned!")
    sys.exit(0)
clear_screen()
print(GREEN + '''███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████''')

# --------------------------
# ASK REPORT MODE: CONTINUOUS OR ONE ROUND
# --------------------------
mode = input(CYAN + "[?] Do you want to send reports continuously? (Y/N): ").strip().lower()
continuous = True if mode == 'y' else False

clear_screen()

# --------------------------
# REPORT COUNTERS & FUNCTIONS
# --------------------------
successful_reports = 0
failed_reports = 0

def send_report(session, report_url, headers, data, proxies=None):
    global successful_reports, failed_reports
    try:
        rep = requests.post(report_url, headers=headers, data=data, proxies=proxies, timeout=5)
        # When the expected response is found, count it as a failure.
        if expected_response in rep.text:
            failed_reports += 1
        else:
            successful_reports += 1
    except Exception as e:
        failed_reports += 1

def get_report_params(r_type, target_ID, session):
    base_url = 'https://www.tiktok.com/aweme/v1/aweme/feedback/'
    common = ("?aid=1233&app_name=tiktok_web&device_platform=web_mobile"
              "&region=SA&priority_region=SA&os=ios&"
              "cookie_enabled=true&screen_width=375&screen_height=667&"
              "browser_language=en-US&browser_platform=iPhone&"
              "browser_name=Mozilla&browser_version=5.0+(iPhone;+CPU+iPhone+OS+15_1+like+Mac+OS+X)+"
              "AppleWebKit/605.1.15+(KHTML,+like+Gecko)+InspectBrowser&"
              "browser_online=true&app_language=ar&timezone_name=Asia%2FRiyadh&"
              "is_page_visible=true&focus_state=true&is_fullscreen=false")
    params = {
        1: {"reason": "399", "reporter_id": "7024230440182809606", "device_id": "7008218736944907778"},
        2: {"reason": "310", "reporter_id": "27568146", "device_id": "7008218736944907778"},
        3: {"reason": "317", "reporter_id": "27568146", "device_id": "7008218736944907778"},
        4: {"reason": "3142", "reporter_id": "6955107540677968897", "device_id": "7034110346035136001"},
        5: {"reason": "306", "reporter_id": "6955107540677968897", "device_id": "7034110346035136001"},
        6: {"reason": "308", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        7: {"reason": "3011", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        8: {"reason": "3052", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        9: {"reason": "3072", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        10: {"reason": "303", "reporter_id": "310430566162530304", "device_id": "7034110346035136001"},
        14: {"reason": "9004", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"},
        15: {"reason": "90064", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"},
        16: {"reason": "9010", "reporter_id": "7242379992225940485", "device_id": "7449373206865561094"}
    }
    p = params.get(r_type)
    url = (f"{base_url}{common}&history_len=14&reason={p['reason']}&report_type=user"
           f"&object_id={target_ID}&owner_id={target_ID}&target={target_ID}"
           f"&reporter_id={p['reporter_id']}&current_region=SA")
    rep_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=' + session,
        'Host': 'www.tiktok.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': generate_user_agent()
    }
    data = {
        "object_id": target_ID,
        "owner_id": target_ID,
        "report_type": "user",
        "target": target_ID
    }
    return url, rep_headers, data

def get_random_report_type():
    # Include options 1-10, 14, 15 and 16 in random mode.
    return random.choice([1,2,3,4,5,6,7,8,9,10,14,15,16])

# --------------------------
# DYNAMIC STATUS UPDATE FUNCTION
# --------------------------
def update_status():
    # Pick a random color for the dynamic output
    color_dynamic = random.choice([F, J, Z, C, B, L, J1, J2, J21, J22, F1, C1, P1])
    total = successful_reports + failed_reports
    clear_screen() 
    print('''▬▬▬▬▬CHYØ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
░█████╗░██╗░░██╗██╗░░░██╗░█████╗░
██╔══██╗██║░░██║╚██╗░██╔╝██╔══██╗
██║░░╚═╝███████║░╚████╔╝░██║░░██║
██║░░██╗██╔══██║░░╚██╔╝░░██║░░██║
╚█████╔╝██║░░██║░░░██║░░░╚█████╔╝
░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░   \x1b[38;5;226m¸.•´¯`•.¸¸ \x1b[1;32mReport By CHYO\x1b[38;5;226m ¸.•´¯`•.¸¸
\x1b[1;32mDEVLOPER↪: @chyoo1''')
         
    status_line = f"\rReports🏴‍☠️: True✅: {GREEN}[{successful_reports}]{color_dynamic} | False❌: {RED}[{failed_reports}]{color_dynamic} | Total: {total}"
    sys.stdout.write(status_line)
    sys.stdout.flush()
print('''▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ CHYØ▬▬▬▬▬▬▬▬''')
# --------------------------
# SEND REPORTS (CONTINUOUS OR ONE ROUND) with dynamic status update
# --------------------------
if continuous:
    # Remove any initial "sending" message and update the status inline
    while True:
        for s in sessions:
            time.sleep(sleep_time)
            current_r_type = get_random_report_type() if random_mode else report_type
            url_report, headers_rep, data_rep = get_report_params(current_r_type, target_ID, s)
            if proxy_mode:
                proxy_addr = random.choice(working_proxies)
                proxies = {"http": proxy_addr, "https": proxy_addr}
            else:
                proxies = None
            send_report(s, url_report, headers_rep, data_rep, proxies=proxies)
            update_status()
else:
    for s in sessions:
        time.sleep(sleep_time)
        current_r_type = get_random_report_type() if random_mode else report_type
        url_report, headers_rep, data_rep = get_report_params(current_r_type, target_ID, s)
        if proxy_mode:
            proxy_addr = random.choice(working_proxies)
            proxies = {"http": proxy_addr, "https": proxy_addr}
        else:
            proxies = None
        send_report(s, url_report, headers_rep, data_rep, proxies=proxies)
        update_status()
    print()  # Ensure a final newline after processing