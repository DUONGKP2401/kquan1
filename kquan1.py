import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import json
from collections import deque, defaultdict, Counter
import random
import hashlib
import platform
import subprocess
import string
import urllib.parse
import uuid

# Check và cài đặt các thư viện cần thiết
try:
    from colorama import init
    init(autoreset=True)
    import pytz
    from faker import Faker
    from pystyle import Colors, Colorate
    # Thư viện Rich cho giao diện
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align
except ImportError:
    print('__Đang cài đặt thư viện nâng cấp, vui lòng chờ...__')
    os.system("pip install requests colorama pytz faker pystyle bs4 rich")
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool__')
    sys.exit()

# =====================================================================================
# PHẦN 1: LOGIC XÁC THỰC KEY
# =====================================================================================

# CONFIGURATION FOR VIP KEY
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/KEY-VIP.txt/main/KEY-VIP.txt"
VIP_CACHE_FILE = 'vip_cache.json'

# Encrypt and decrypt data using base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Colors for display
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

# Banner xác thực
def authentication_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = f"""
{luc}████████╗ ██████╗░░ ██╗░░██╗░
{luc}╚══██╔══╝ ██╔══██╗░ ██║██╔╝░░
{luc}░░░██║░░░ ██║░░██║░ █████╔╝░░
{luc}░░░██║░░░ ██║░░██║░ ██╔═██╗░░
{luc}░░░██║░░░ ██║░░██║░ ██║░╚██╗░
{luc}░░░╚═╝░░░ ╚█████╔╝░ ╚═╝░░╚═╝░
{trang}══════════════════════════

{vang}Tool NUÔI FB
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

# DEVICE ID AND IP ADDRESS FUNCTIONS
def get_device_id():
    """Generates a stable device ID based on CPU information."""
    system = platform.system()
    try:
        if system == "Windows":
            cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, text=True, stderr=subprocess.DEVNULL)
            cpu_info = ''.join(line.strip() for line in cpu_info.splitlines() if line.strip() and "ProcessorId" not in line)
        else:
            try:
                cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            except:
                cpu_info = platform.processor()
        if not cpu_info:
            cpu_info = platform.processor()
    except Exception:
        cpu_info = "Unknown"

    hash_hex = hashlib.sha256(cpu_info.encode()).hexdigest()
    only_digits = re.sub(r'\D', '', hash_hex)
    if len(only_digits) < 16:
        only_digits = (only_digits * 3)[:16]

    return f"DEVICE-{only_digits[:16]}"

def get_ip_address():
    """Gets the user's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    """Displays the banner, IP address, and Device ID."""
    authentication_banner()
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")

    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")


# FREE KEY HANDLING FUNCTIONS
def luu_thong_tin_ip(ip, key, expiration_date):
    """Saves free key information to a json file."""
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    """Loads free key information from the json file."""
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def kiem_tra_ip(ip):
    """Checks for a saved free key for the current IP."""
    data = tai_thong_tin_ip()
    if data and ip in data:
        try:
            expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
            if expiration_date > datetime.now():
                return data[ip]['key']
        except (ValueError, KeyError):
            return None
    return None

def generate_key_and_url(ip_address):
    """Creates a free key and a URL to bypass the link."""
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'TDK{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://tdkkeyfree.blogspot.com/2025/09/t1.html?m={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    """Shortens the link to get the free key."""
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def process_free_key(ip_address):
    """Handles the entire process of obtaining a free key."""
    url, key, expiration_date = generate_key_and_url(ip_address)

    with ThreadPoolExecutor(max_workers=1) as executor:
        yeumoney_future = executor.submit(get_shortened_link_phu, url)
        yeumoney_data = yeumoney_future.result()

    if yeumoney_data and yeumoney_data.get('status') == "error":
        print(yeumoney_data.get('message'))
        return False

    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_yeumoney}{trang}')

    while True:
        keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}')
        if keynhap == key:
            print(f'{luc}Key Đúng! Mời Bạn Dùng Tool{trang}')
            sleep(2)
            luu_thong_tin_ip(ip_address, keynhap, expiration_date)
            return True
        else:
            print(f'{trang}[{do}<>{trang}] {hong}Key Sai! Vui Lòng Vượt Lại Link {xnhac}: {link_key_yeumoney}{trang}')


# VIP KEY HANDLING FUNCTIONS
def save_vip_key_info(device_id, key, expiration_date_str):
    """Saves VIP key information to a local cache file."""
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    """Loads VIP key information from the local cache file."""
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    """Calculates and displays the remaining time for a VIP key."""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()

        if expiry_date > now:
            delta = expiry_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
    """Checks the VIP key from the URL on GitHub."""
    print(f"{vang}Đang kiểm tra Key VIP...{trang}")
    try:
        response = requests.get(VIP_KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{do}Lỗi: Không thể tải danh sách key (Status code: {response.status_code}).{trang}")
            return 'error', None

        key_list = response.text.strip().split('\n')
        for line in key_list:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                key_ma_may, key_value, _, key_ngay_het_han = parts

                if key_ma_may == machine_id and key_value == user_key:
                    try:
                        expiry_date = datetime.strptime(key_ngay_het_han, '%d/%m/%Y')
                        if expiry_date.date() >= datetime.now().date():
                            return 'valid', key_ngay_het_han
                        else:
                            return 'expired', None
                    except ValueError:
                        continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None

# MAIN AUTHENTICATION FLOW
def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)
    key_info = {}

    if not ip_address or not device_id:
        print(f"{do}Không thể lấy thông tin thiết bị cần thiết. Vui lòng kiểm tra kết nối mạng.{trang}")
        return False, None, None

    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                key_info = {'type': 'VIP', 'key': cached_vip_info['key'], 'expiry': cached_vip_info['expiration_date']}
                sleep(3)
                return True, device_id, key_info
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng lấy hoặc nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key. Vui lòng nhập lại key.{trang}")

    if kiem_tra_ip(ip_address):
        print(f"{trang}[{do}<>{trang}] {hong}Key free hôm nay vẫn còn hạn. Mời bạn dùng tool...{trang}")
        key_info = {'type': 'Free', 'key': 'Free Daily', 'expiry': datetime.now().strftime('%d/%m/%Y')}
        time.sleep(2)
        return True, device_id, key_info

    while True:
        print(f"{trang}========== {vang}MENU LỰA CHỌN{trang} ==========")
        print(f"{trang}[{luc}1{trang}] {xduong}Nhập Key VIP{trang}")
        print(f"{trang}[{luc}2{trang}] {xduong}Lấy Key Free (Dùng trong ngày){trang}")
        print(f"{trang}======================================")

        try:
            choice = input(f"{trang}[{do}<>{trang}] {xduong}Nhập lựa chọn của bạn: {trang}")
            print(f"{trang}═══════════════════════════════════")

            if choice == '1':
                vip_key_input = input(f'{trang}[{do}<>{trang}] {vang}Vui lòng nhập Key VIP: {luc}')
                status, expiry_date_str = check_vip_key(device_id, vip_key_input)

                if status == 'valid':
                    print(f"{luc}Xác thực Key VIP thành công!{trang}")
                    save_vip_key_info(device_id, vip_key_input, expiry_date_str)
                    display_remaining_time(expiry_date_str)
                    key_info = {'type': 'VIP', 'key': vip_key_input, 'expiry': expiry_date_str}
                    sleep(3)
                    return True, device_id, key_info
                elif status == 'expired':
                    print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
                elif status == 'not_found':
                    print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
                else:
                    print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
                sleep(2)

            elif choice == '2':
                if process_free_key(ip_address):
                    key_info = {'type': 'Free', 'key': 'Free Daily', 'expiry': datetime.now().strftime('%d/%m/%Y')}
                    return True, device_id, key_info
                else:
                    return False, None, None

            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2.{trang}")

        except (KeyboardInterrupt):
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

# =====================================================================================
# PHẦN 2: LOGIC TOOL FACEBOOK
# =====================================================================================

# --- Cải thiện mã màu và giao diện ---
tim = "\033[1;35m" # Màu hồng đậm cho banner
xanh = "\033[1;36m"
# Giao diện prompt mới, đẹp hơn
thanh = f'{xanh}[{vang}TDK{xanh}] {trang}➢ '
listCookie = []
nhiem_vu_da_bat = {}

def Server():
    try:
        response = requests.get('https://dhphuoc.click/api_key/server.php').json()
        if response['status'] == 'success': return 'LIVE'
        else: return 'OFFLINE'
    except:
        return 'OFFLINE'

def thanhngang(so):
    print(xanh + '—' * so)

# --- Banner và giao diện mới theo yêu cầu ---
def banner():
    os.system('cls' if os.name=='nt' else 'clear')
    banner_art = f'''
        '''
    print(Colorate.Vertical(Colors.blue_to_cyan, banner_art))
    print(f'''{thanh}{luc}Admin{trang}: {vang}DUONG PHUNG 👨‍💻
{thanh}{luc}Nhóm Zalo{trang}: {do}https://zalo.me/g/ddxsyp497
{thanh}{luc}Đang Sử Dụng Tool{trang}: {vang}Nuôi Tài Khoản Facebook''')
    thanhngang(65)

# --- Hàm Delay được làm lại, chạy đúng 1 dòng ---
def Delay(value):
    try:
        value = int(value)
        for i in range(value, 0, -1):
            sys.stdout.write(f'\r{trang}[{xanh}DELAY{trang}] {vang}Vui lòng chờ trong {luc}{i:02d}{vang} giây...{" " * 25}')
            sys.stdout.flush()
            sleep(1)
        sys.stdout.write('\r' + ' ' * 60 + '\r') # Xóa dòng delay sau khi chạy xong
        sys.stdout.flush()
    except (ValueError, TypeError):
        pass

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

class Facebook:
    def __init__(self, cookie: str):
        try:
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.session = requests.Session()
            self.id = self.cookie.split('c_user=')[1].split(';')[0]
            self.headers = {'authority': 'www.facebook.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'vi', 'sec-ch-prefers-color-scheme': 'light', 'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'viewport-width': '1366', 'Cookie': self.cookie}
            url = self.session.get(f'https://www.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            data_split = response.text.split('"CurrentUserInitialData",[],{')
            json_data = '{' + data_split[1].split('},')[0] + '}'
            parsed_data = json.loads(json_data)
            id = parsed_data.get('USER_ID', '0')
            name = parsed_data.get('NAME', '')
            if id == '0' and name == '': return 'cookieout'
            elif '828281030927956' in response.text: return '956'
            elif '1501092823525282' in response.text: return '282'
            elif '601051028565049' in response.text: return 'spam'
            else: id, name = parsed_data.get('USER_ID'), parsed_data.get('NAME')
            return {'success': 200, 'id': id, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def timban(self, text):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'SearchCometResultsInitialResultsQuery',
                'variables': '{"count":5,"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"23bd9138-cec6-4e71-aaeb-225fc8964e5b","tsid":"0.10477759801522946"},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"GLOBAL_SEARCH"},"filters":[],"text":"'+text+'"},"cursor":null,"feedbackSource":23,"fetch_filters":true,"renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '9545374252239656'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data).json()
            profile = response["data"]["serpResponse"]["results"]["edges"][0]['rendering_strategy']['result_rendering_strategies'][0]['view_model']['profile']
            name = profile.get('name')
            uid = profile.get('id')
            return {'status': 'success', 'id': uid, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def ketban(self, idkb):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'FriendingCometFriendRequestSendMutation',
                'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1748257667487,475021,190055527696468,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1748257603766,498383,391724414624676,,","click_proof_validation_result":null,"friend_requestee_ids":["'+idkb+'"],"friending_channel":"PROFILE_BUTTON","warn_ack_for_ids":[],"actor_id":"'+self.id+'","client_mutation_id":"6"},"scale":1}',
                'server_timestamps': 'true',
                'doc_id': '8805328442902902'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data).json()
            trangthai = response["data"]["friend_request_send"]["friend_requestees"]
            if trangthai and trangthai[0].get('friendship_status') == 'OUTGOING_REQUEST':
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def getidpost(self):
        try:
            variables = {"RELAY_INCREMENTAL_DELIVERY": True, "clientQueryId": str(uuid.uuid4()), "count": 5, "cursor": None, "feedLocation": "NEWSFEED", "feedStyle": "DEFAULT", "orderby": ["TOP_STORIES"], "renderLocation": "homepage_stream", "scale": 1, "useDefaultActor": False}
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometNewsFeedPaginationQuery',
                'variables': json.dumps(variables),
                'server_timestamps': 'true',
                'doc_id': '29492828377027602'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data).text
            if '"post_id":"' in response:
                id = response.split('\"post_id\":\"')[1].split('\",')[0]
                return {'status': 'success', 'idpost': id}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def getidgr(self, noidung):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'SearchCometResultsInitialResultsQuery',
                'variables': '{"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"' + str(uuid.uuid4()) + '","tsid":"' + str(random.random()) + '"},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"GROUPS_TAB"},"filters":[],"text":"'+noidung+'"},"count":5,"cursor":null,"feedLocation":"SEARCH","feedbackSource":23,"fetch_filters":true,"focusCommentID":null,"locale":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true}',
                'server_timestamps': 'true',
                'doc_id': '24016506881293628'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data).json()
            thongtin = response['data']["serpResponse"]["results"]['edges'][0]['rendering_strategy']['view_model']['profile']
            name = thongtin.get('name')
            uid = thongtin.get('id')
            return {'status': 'success', 'id': uid, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def reaction(self, id, type):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            idreac = reac.get(type)
            variables = {
                "input": {
                    "attribution_id_v2": f"CometHomeRoot.react,comet.home,tap_tabbar,{int(datetime.now().timestamp() * 1000)},322693,4748854339,,",
                    "feedback_id": encode_to_base64(f"feedback:{id}"),
                    "feedback_reaction_id": idreac,
                    "feedback_source": "NEWS_FEED",
                    "is_tracking_encrypted": True,
                    "tracking": [],
                    "session_id": str(uuid.uuid4()),
                    "actor_id": self.id,
                    "client_mutation_id": str(random.randint(1, 10))
                },
                "useDefaultActor": False,
                "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False
            }
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': json.dumps(variables),'server_timestamps': 'true','doc_id': '7047198228715224',}
            _get = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
            if '{"data":{"feedback_react":{"feedback":{"id":' in _get.text:
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def comment(self, id, msg):
        try:
            variables = {
                "feedLocation": "DEDICATED_COMMENTING_SURFACE",
                "feedbackSource": 110,
                "groupID": None,
                "input": {
                    "client_mutation_id": str(random.randint(1, 10)),
                    "actor_id": self.id,
                    "attachments": None,
                    "feedback_id": encode_to_base64(f"feedback:{id}"),
                    "formatting_style": None,
                    "message": {
                        "ranges": [],
                        "text": msg
                    },
                    "attribution_id_v2": f"CometHomeRoot.react,comet.home,via_cold_start,{int(datetime.now().timestamp() * 1000)},194880,4748854339,,",
                    "vod_video_timestamp": None,
                    "feedback_referrer": "/",
                    "is_tracking_encrypted": True,
                    "tracking": [json.dumps({
                        "assistant_caller": "comet_above_composer",
                        "conversation_guide_session_id": str(uuid.uuid4()),
                        "conversation_guide_shown": None
                    })],
                    "idempotence_token": f"client:{uuid.uuid4()}",
                    "session_id": str(uuid.uuid4())
                },
                "inviteShortLinkKey": None,
                "renderLocation": None,
                "scale": 1,
                "useDefaultActor": False,
                "focusCommentID": None
            }
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'useCometUFICreateCommentMutation','variables': json.dumps(variables),'server_timestamps': 'true','doc_id': '7994085080671282',}
            cmt = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            if '"feedback_submitted":true' in str(cmt) or 'create_comment' in str(cmt):
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def follow(self, id):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUserFollowMutation','variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1719765181042,489343,250100865708545,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,unexpected,1719765155735,648442,391724414624676,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1719765153341,865155,391724414624676,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"5"},"scale":1}','server_timestamps': 'true','doc_id': '25581663504782089',}
            response = self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers)
            if '"subscribe_status":"IS_SUBSCRIBED"' in response.text:
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def group(self, id):
        try:
            data = {'av':self.id,'fb_dtsg':self.fb_dtsg,'jazoest':self.jazoest,'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'GroupCometJoinForumMutation','variables':'{"feedType":"DISCUSSION","groupID":"'+id+'","imageMediaType":"image/x-auto","input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,via_cold_start,1673041528761,114928,2361831622,","group_id":"'+id+'","group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":false},"actor_id":"'+self.id+'","client_mutation_id":"1"},"inviteShortLinkKey":null,"isChainingRecommendationUnit":false,"isEntityMenu":true,"scale":2,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometEntityMenuEmbeddedrelayprovider":true,"__relay_internal__pv__GlobalPanelEnabledrelayprovider":false}','server_timestamps':'true','doc_id':'5853134681430324','fb_api_analytics_tags':'["qpl_active_flow_ids=431626709"]',}
            response = self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
            if id in response.text:
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

def addcookie():
    i = 0
    while True:
        i += 1
        cookie = input(f'{thanh}{luc}Nhập Cookie Facebook số{vang} {i}{trang}: {vang}')
        if cookie == '' and i > 1:
            break
        if cookie == '':
            i -= 1
            continue
        fb = Facebook(cookie)
        info = fb.info()
        if info and 'success' in info:
            name = info['name']
            print(f'{thanh}{luc}Tên Facebook: {vang}{name} {luc}➤ {trang}Thêm thành công!')
            listCookie.append(cookie)
        else:
            print(f'{thanh}{do}Cookie Facebook không hợp lệ hoặc đã hết hạn!')
            i -= 1
    thanhngang(65)

# =====================================================================================
# PHẦN 3: LUỒNG CHẠY CHÍNH
# =====================================================================================

if __name__ == "__main__":
    is_authenticated, device_id, key_info = main_authentication()

    if is_authenticated:
        # Bắt đầu chạy logic của tool FB7 sau khi xác thực thành công
        server = Server()
        if server != 'LIVE':
            banner()
            print(f'{thanh}{luc}Trạng thái Server{trang}: {trang}[{do}{server}{trang}]')
            os.remove(sys.argv[0])
            sys.exit()
        else:
            banner()
            if not os.path.exists('cookiefb-add.json'):
                addcookie()
                with open('cookiefb-add.json','w') as f:
                    json.dump(listCookie, f, indent=4)
            else:
                print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Sử dụng Cookie Facebook đã lưu')
                print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Cookie Facebook mới')
                thanhngang(65)
                chon = input(f'{thanh}{luc}Nhập lựa chọn của bạn{trang}: {vang}')
                thanhngang(65)
                while True:
                    if chon == '1':
                        print(f'{thanh}{luc}Đang tải dữ liệu đã lưu... ')
                        sleep(1)
                        listCookie = json.loads(open('cookiefb-add.json', 'r').read())
                        break
                    elif chon == '2':
                        addcookie()
                        with open('cookiefb-add.json','w') as f:
                            json.dump(listCookie, f, indent=4)
                        break
                    else:
                        chon = input(f'{thanh}{do}Lựa chọn không hợp lệ, vui lòng nhập lại: {vang}')

            banner()
            comment = input(f"{thanh}{luc}Bật comment dạo {do}({vang}y/n{do}){luc}: {vang}").lower() == 'y'
            group = input(f"{thanh}{luc}Bật tham gia nhóm dạo {do}({vang}y/n{do}){luc}: {vang}").lower() == 'y'
            reaction = input(f"{thanh}{luc}Bật thả cảm xúc dạo {do}({vang}y/n{do}){luc}: {vang}").lower() == 'y'
            follow = input(f"{thanh}{luc}Bật follow dạo {do}({vang}y/n{do}){luc}: {vang}").lower() == 'y'
            add_friend = input(f"{thanh}{luc}Bật gửi lời mời kết bạn dạo {do}({vang}y/n{do}){luc}: {vang}").lower() == 'y'
            thanhngang(65)

            comments = []
            if comment:
                nhiem_vu_da_bat['comment'] = True
                i = 1
                while True:
                    cmt = input(f"{thanh}{luc}Nhập nội dung comment số {vang}{i}{trang} (để trống và enter để kết thúc): {vang}").strip()
                    if cmt == "":
                        if len(comments) > 0:
                            break
                        else:
                            print(f"{thanh}{do}Bạn phải nhập ít nhất một nội dung comment!")
                    else:
                        comments.append(cmt)
                        i += 1
                thanhngang(65)

            if reaction:
                nhiem_vu_da_bat['reaction'] = True
                print(f'{xanh}╔═══════════════════════════════════╗')
                print(f'{xanh}║    {vang}CHỌN LOẠI CẢM XÚC TƯƠNG TÁC   {xanh}║')
                print(f'{xanh}╠═══════════════════════════════════╣')
                print(f'{xanh}║ {do}[{vang}1{do}] {luc}LIKE      {do}[{vang}2{do}] {luc}LOVE      {do}[{vang}3{do}] {luc}CARE  {xanh}║')
                print(f'{xanh}║ {do}[{vang}4{do}] {luc}HAHA      {do}[{vang}5{do}] {luc}WOW       {do}[{vang}6{do}] {luc}SAD   {xanh}║')
                print(f'{xanh}║ {do}[{vang}7{do}] {luc}ANGRY                             {xanh}║')
                print(f'{xanh}╚═══════════════════════════════════╝')
                print(f'{thanh}{luc}Có thể chọn nhiều nhiệm vụ {do}({vang}VD: 1245...{do})')
                chon = input(f'{thanh}{luc}Nhập số để chọn nhiệm vụ{trang}: {vang}').strip()
                ds_camxuc = {"1": "LIKE", "2": "LOVE", "3": "CARE", "4": "HAHA", "5": "WOW", "6": "SAD", "7": "ANGRY"}
                camxucchon = [ds_camxuc[c] for c in chon if c in ds_camxuc]
                thanhngang(65)

            if group: nhiem_vu_da_bat['group'] = True
            if follow: nhiem_vu_da_bat['follow'] = True
            if add_friend: nhiem_vu_da_bat['add_friend'] = True

            while(True):
                try:
                    delay = int(input(f'{thanh}{luc}Nhập delay giữa các nhiệm vụ (giây){trang}: {vang}'))
                    break
                except:
                    print(f'{thanh}{do}Vui lòng chỉ nhập số!')
            while(True):
                try:
                    JobbBlock = int(input(f'{thanh}{luc}Sau bao nhiêu nhiệm vụ thì nghỉ chống block{trang}: {vang}'))
                    if JobbBlock <= 1:
                        print(f'{thanh}{do}Vui lòng nhập số lớn hơn 1')
                        continue
                    break
                except:
                    print(f'{thanh}{do}Vui lòng chỉ nhập số!')
            while(True):
                try:
                    DelayBlock = int(input(f'{thanh}{luc}Thời gian nghỉ chống block (giây){trang}: {vang}'))
                    break
                except:
                    print(f'{thanh}{do}Vui lòng chỉ nhập số!')
            while(True):
                try:
                    JobBreak = int(input(f'{thanh}{luc}Sau bao nhiêu nhiệm vụ thì chuyển tài khoản{trang}: {vang}'))
                    if JobBreak <= 1:
                        print(f'{thanh}{do}Vui lòng nhập số lớn hơn 1')
                        continue
                    break
                except:
                    print(f'{thanh}{do}Vui lòng chỉ nhập số!')
            runidfb = input(f'{thanh}{luc}Bạn có muốn ẩn ID Facebook không? {do}({vang}y/n{do}){luc}: {vang}')
            thanhngang(65)
            stt = 0
            while True:
                if len(listCookie) == 0:
                    print(f'{thanh}{do}Đã hết cookie trong danh sách, vui lòng nhập lại!')
                    addcookie()
                    with open('cookiefb-add.json','w') as f:
                        json.dump(listCookie, f, indent=4)

                for cookie in listCookie:
                    chuyen = False
                    nextDelay = False
                    JobFail, JobSuccess = 0, 0
                    fb = Facebook(cookie)
                    info = fb.info()

                    if info and 'success' in info:
                        namefb = info['name']
                        idfb = str(info['id'])
                        idrun = idfb[0:3] + "#" * (len(idfb) - 3) if runidfb.lower() == 'y' else idfb
                    else:
                        print(f'{thanh}{do}Cookie die hoặc hết hạn, đã tự động xóa khỏi danh sách!')
                        listCookie.remove(cookie)
                        with open('cookiefb-add.json', 'w') as f:
                            json.dump(listCookie, f, indent=4)
                        break

                    print(f'{luc}Đang chạy tài khoản{trang}: {vang}{namefb} {do}| {luc}ID{trang}: {vang}{idrun}')
                    thanhngang(65)

                    while True:
                        if not nhiem_vu_da_bat:
                            print(f'{thanh}{do}Bạn chưa bật bất kỳ nhiệm vụ nào. Vui lòng khởi động lại tool.')
                            sys.exit()

                        try:
                            nhiemvu = random.choice(list(nhiem_vu_da_bat.keys()))
                            timejob = datetime.now().strftime('%H:%M:%S')

                            if nhiemvu == "comment":
                                getpost = fb.getidpost()
                                if getpost.get('status') == 'error':
                                    JobFail += 1
                                    print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}COMMENT   {do} | {do}Không tìm thấy bài viết')
                                else:
                                    idpost = getpost['idpost']
                                    noidung = random.choice(comments)
                                    cmt = fb.comment(idpost, noidung)
                                    if cmt and cmt.get('trangthai') == 'thanhcong':
                                        nextDelay, JobSuccess, stt = True, JobSuccess + 1, stt + 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {luc}SUCCESS{do} | {trang}COMMENT   {do} | {vang}"{noidung}"{do} | {trang}{idpost}')
                                    else:
                                        JobFail += 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}COMMENT   {do} | {do}Comment không thành công')

                            elif nhiemvu == "group":
                                ten = requests.get('https://dhphuoc.click/vietnamese-name-generator?gioitinh=male').json()['data']['name']
                                timgr = fb.getidgr(ten)
                                if timgr.get('status') == 'error':
                                    JobFail += 1
                                    print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}GROUP     {do} | {do}Không tìm thấy nhóm')
                                else:
                                    id, name = timgr['id'], timgr['name']
                                    thamgia = fb.group(id)
                                    if thamgia and thamgia.get('trangthai') == 'thanhcong':
                                        nextDelay, JobSuccess, stt = True, JobSuccess + 1, stt + 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {luc}SUCCESS{do} | {trang}GROUP     {do} | {luc}{name} {do}| {trang}{id}')
                                    else:
                                        JobFail += 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}GROUP     {do} | {do}Tham gia không thành công')

                            elif nhiemvu == "reaction":
                                getpost = fb.getidpost()
                                if getpost.get('status') == 'error':
                                    JobFail += 1
                                    print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}REACTION  {do} | {do}Không tìm thấy bài viết')
                                else:
                                    idpost = getpost['idpost']
                                    camxuc = random.choice(camxucchon)
                                    tha = fb.reaction(idpost, camxuc)
                                    if tha and tha.get('trangthai') == 'thanhcong':
                                        nextDelay, JobSuccess, stt = True, JobSuccess + 1, stt + 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {luc}SUCCESS{do} | {trang}REACTION  {do} | {vang}{camxuc}{do} | {trang}{idpost}')
                                    else:
                                        JobFail += 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}REACTION  {do} | {do}Thả cảm xúc thất bại')

                            elif nhiemvu == "follow":
                                ten = requests.get('https://dhphuoc.click/vietnamese-name-generator?gioitinh=female').json()['data']['name']
                                timbb = fb.timban(ten)
                                if timbb.get('status') == 'error':
                                    JobFail += 1
                                    print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}FOLLOW    {do} | {do}Không tìm thấy người dùng')
                                else:
                                    id, name = timbb['id'], timbb['name']
                                    if fb.follow(id).get('trangthai') == 'thanhcong':
                                        nextDelay, JobSuccess, stt = True, JobSuccess + 1, stt + 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {luc}SUCCESS{do} | {trang}FOLLOW    {do} | {luc}{name} {do}| {trang}{id}')
                                    else:
                                        JobFail += 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}FOLLOW    {do} | {do}Không có nút theo dõi')

                            elif nhiemvu == "add_friend":
                                ten = requests.get('https://dhphuoc.click/vietnamese-name-generator?gioitinh=male').json()['data']['name']
                                timbb = fb.timban(ten)
                                if timbb.get('status') == 'error':
                                    JobFail += 1
                                    print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}ADD FRIEND{do} | {do}Không tìm thấy người dùng')
                                else:
                                    id, name = timbb['id'], timbb['name']
                                    ketban = fb.ketban(id)
                                    if ketban and ketban.get('trangthai') == 'thanhcong':
                                        nextDelay, JobSuccess, stt = True, JobSuccess + 1, stt + 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {luc}SUCCESS{do} | {trang}ADD FRIEND{do} | {luc}{name} {do}| {trang}{id}')
                                    else:
                                        JobFail += 1
                                        print(f'{vang}[{stt:02d}]{do} | {xanh}{timejob}{do} | {do}FAILED{do} | {trang}ADD FRIEND{do} | {do}Không có nút kết bạn')

                            if JobFail >= 20:
                                check = fb.info()
                                thong_bao_chuyen_acc = f'{thanh}{do}Tài khoản {vang}{namefb} {do}gặp lỗi, tự động chuyển...'
                                if 'spam' in check:
                                    print(f'{thong_bao_chuyen_acc} Lý do: Bị hạn chế tính năng (SPAM)')
                                elif '282' in check:
                                    print(f'{thong_bao_chuyen_acc} Lý do: Checkpoint 282')
                                elif '956' in check:
                                    print(f'{thong_bao_chuyen_acc} Lý do: Checkpoint 956')
                                else:
                                    print(f'{thong_bao_chuyen_acc} Lý do: Cookie die')

                                listCookie.remove(cookie)
                                with open('cookiefb-add.json', 'w') as f:
                                    json.dump(listCookie, f, indent=4)
                                chuyen = True

                            if JobSuccess != 0 and JobSuccess % int(JobBreak) == 0:
                                print(f'{thanh}{luc}Đã hoàn thành {JobSuccess} nhiệm vụ, chuyển tài khoản tiếp theo...')
                                chuyen = True

                            if chuyen:
                                thanhngang(65)
                                Delay(5)
                                break

                            if nextDelay:
                                nextDelay = False
                                if stt % int(JobbBlock) == 0:
                                    print(f'{thanh}{vang}Đạt mốc chống block, tạm nghỉ {DelayBlock} giây.')
                                    Delay(DelayBlock)
                                else:
                                    Delay(delay)

                        except Exception as e:
                            pass
