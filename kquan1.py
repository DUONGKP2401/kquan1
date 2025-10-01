import hashlib
from collections import Counter
import statistics
import platform
from datetime import datetime
import base64
import urllib.parse
import requests
import random
import string
import math
import json
import os
import random
import requests
import time
from colorama import Fore, Style, init
init(autoreset=True)

NV={
    1:'Bậc thầy tấn công',
    2:'Quyền sắt',
    3:'Thợ lặn sâu',
    4:'Cơn lốc sân cỏ',
    5:'Hiếp sĩ phi nhanh',
    6:'Vua home run'
}

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

def banner(game):
    banner="""
████████╗██████╗ ██╗  ██╗
 ╚══██╔══╝██╔══██╗██║ ██╔╝
    ██║   ██║  ██║█████╔╝
    ██║   ██║  ██║██╔═██╗
    ██║   ██████╔╝██║  ██╗
    ╚═╝   ╚═════╝ ╚═╝  ╚═╝
    """
    for i in banner.split('\n'):
        x,y,z=200,255,255
        for j in range(len(i)):
            prints(x,y,z,i[j],end='')
            x-=4
            time.sleep(0.001)
        print()
    prints(247, 255, 97,"✨" + "═" * 45 + "✨")
    prints(32, 230, 151,f"🌟 XWORLD - {game} ALQQV1 (QUANQUANV1) 🌟".center(45))
    prints(247, 255, 97,"═" * 47)
    prints(7, 205, 240,"Telegram: @tankeko12")
    prints(7, 205, 240,"Nhóm Zalo: https://zalo.me/g/ddxsyp497")
    prints(7, 205, 240,"Admin: DUONG PHUNG")
    prints(247, 255, 97,"═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243,'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ',end='')
        x=input()
        if x.lower()=='y':
            with open('data-xw-cdtd.txt','r',encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97,"═" * 47)
    str_guide="""
    Hướng dẫn lấy link:
    1. Truy cập vào trang web xworld.io
    2. Đăng nhập tài khoản của bạn
    3. Tìm và nhấn vào "Chạy đua tốc độ"
    4. Nhấn "Lập tức truy cập"
    5. Copy link trang web đó và dán vào đây
"""
    prints(218, 255, 125,str_guide)
    prints(247, 255, 97,"═" * 47)
    prints(125, 255, 168,'📋 Nhập link của bạn:',end=' ')
    link=input()
    user_id=link.split('&')[0].split('?userId=')[1]
    user_secretkey=link.split('&')[1].split('secretKey=')[1]
    prints(218, 255, 125,f'    User ID của bạn là {user_id}')
    prints(218, 255, 125,f'    User Secret Key của bạn là {user_secretkey}')
    json_data={
        'user-id':user_id,
        'user-secret-key':user_secretkey,
    }
    with open('data-xw-cdtd.txt','w+',encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def load_config_cdtd():
    if os.path.exists('config_cdtd_ctool.txt'):
        prints(0, 255, 243,'Bạn có muốn sử dụng cấu hình đã lưu hay không? (y/n) ',end='')
        x=input()
        if x.lower()=='y':
            with open('config_cdtd_ctool.txt','r',encoding='utf-8') as f:
                return json.load(f)
    
    str_coin_type="""
Nhập loại tiền mà bạn muốn chơi:
    1. USDT
    2. BUILD
    3. WORLD
"""
    prints(219, 237, 138,str_coin_type)
    while True:
        prints(125, 255, 168,'Nhập loại tiền bạn muốn chơi (1/2/3):',end=' ')
        x=input()
        if x in ['1', '2', '3']:
            Coin = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}[x]
            break
        else:
            prints(247, 30, 30, 'Nhập sai, vui lòng nhập lại ...', end='\r')
    
    prints(255, 13, 69,'VUI LÒNG CÀI ĐẶT CÁC THAM SỐ CHO TOOL:')
    
    coins = float(input(f'    Nhập số {Coin} bạn muốn đặt cho MỖI NHÂN VẬT: '))
    take_profit = float(input(f'    Chốt lời khi đạt được bao nhiêu {Coin} (nhập 0 để bỏ qua): '))
    stop_loss = float(input(f'    Cắt lỗ khi thua bao nhiêu {Coin} (nhập 0 để bỏ qua): '))
    consecutive_loss_stop = int(input('    Dừng tool sau bao nhiêu ván thua liên tiếp (nhập 0 để bỏ qua): '))
    
    # New questions for loss multiplication
    prints(255, 165, 0, 'CÀI ĐẶT GẤP THẾP KHI THUA:')
    use_multiplier = input('    Bạn có muốn nhân tiền cược sau khi thua không? (y/n): ').lower() == 'y'
    loss_multiplier = 1.0
    if use_multiplier:
        loss_multiplier = float(input('    Nhân bao nhiêu lần sau mỗi lần thua? (ví dụ: 2): '))

    games_to_play = int(input('    Chơi bao nhiêu ván thì nghỉ (nhập 0 để chơi liên tục): '))
    games_to_rest = 0
    if games_to_play > 0:
        games_to_rest = int(input('    Nghỉ bao nhiêu ván rồi chơi tiếp: '))

    config={
        'Coin': Coin,
        'initial_coins': coins,
        'current_coins': coins,
        'take_profit': take_profit if take_profit > 0 else 99999999,
        'stop_loss': stop_loss if stop_loss > 0 else 99999999,
        'consecutive_loss_stop': consecutive_loss_stop if consecutive_loss_stop > 0 else 99999999,
        'use_multiplier': use_multiplier,
        'loss_multiplier': loss_multiplier,
        'games_to_play': games_to_play,
        'games_to_rest': games_to_rest
    }
    with open('config_cdtd_ctool.txt','w+',encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    return config

def top_100_cdtd():
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'origin': 'https://sprintrun.win',
        'priority': 'u=1, i',
        'referer': 'https://sprintrun.win/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = requests.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers).json()
        nv=[1,2,3,4,5,6]
        kq=[]
        for i in range(1,7):
            kq.append(response['data']['athlete_2_win_times'][str(i)])
        return nv,kq
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy top 100: {e}')
        time.sleep(5)
        return top_100_cdtd()

def top_10_cdtd(headers):
    params = ''
    try:
        response = requests.get('https://api.sprintrun.win/sprint/recent_10_issues', params=params, headers=headers).json()
        ki=[]
        kq=[]
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            kq.append(i['result'][0])
        return ki,kq
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy top 10: {e}')
        time.sleep(5)
        return top_10_cdtd(headers)

def print_data(data_top10_cdtd,data_top100_cdtd):
    prints(247, 255, 97,"═" * 47)
    prints(0, 255, 250,"DỮ LIỆU 10 VÁN GẦN NHẤT:".center(50))
    for i in range(len(data_top10_cdtd[0])):
        prints(255,255,0,f'Kì {data_top10_cdtd[0][i]}: Người về nhất : {NV[int(data_top10_cdtd[1][i])]}')
    prints(247, 255, 97,"═" * 47)
    prints(0, 255, 250,"DỮ LIỆU 100 VÁN GẦN NHẤT:".center(50))
    for i in range(6):
        prints(255,255,0,f'{NV[int(i+1)]} về nhất {data_top100_cdtd[1][int(i)]} lần')
    prints(247, 255, 97,"═" * 47)

def selected_NV_enhanced(data_top100_cdtd):
    """
    Chọn ngẫu nhiên 3 nhân vật khác nhau để đặt cược.
    Lựa chọn này hoàn toàn ngẫu nhiên và không dựa vào tỷ lệ thắng trước đó.
    """
    champions = list(range(1, 7))  # Danh sách tất cả các nhân vật từ 1 đến 6
    # Chọn ngẫu nhiên 3 nhân vật không trùng lặp từ danh sách.
    return random.sample(champions, 3)


def kiem_tra_kq_cdtd(headers, kqs_dat, ki):
    prints(0, 255, 37,f'Đang đợi kết quả của kì #{ki}')
    start_time = time.time()
    while True:
        try:
            data_top10_cdtd = top_10_cdtd(headers)
            if int(data_top10_cdtd[0][0]) == int(ki):
                winner = int(data_top10_cdtd[1][0])
                prints(0, 255, 30,f'Kết quả của kì {ki}: Người về nhất là {NV[winner]}')
                if winner in kqs_dat:
                    prints(0, 255, 37,'XIN CHÚC MỪNG. BẠN ĐÃ THẮNG!')
                    return True
                else:
                    prints(255, 0, 0,'BẠN ĐÃ THUA. CHÚC BẠN MAY MẮN LẦN SAU!')
                    return False
            elapsed_time = time.time() - start_time
            prints(0, 255, 197,f'Đang đợi kết quả {elapsed_time:.0f}s...', end='\r')
            time.sleep(1)
        except Exception as e:
            prints(255, 0, 0, f"Lỗi khi kiểm tra kết quả: {e}")
            time.sleep(5)


def user_asset(headers):
    try:
        json_data = {
            'user_id': int(headers['user-id']),
            'source': 'home',
        }
        response = requests.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        asset={
            'USDT':response['data']['user_asset']['USDT'],
            'WORLD':response['data']['user_asset']['WORLD'],
            'BUILD':response['data']['user_asset']['BUILD']
        }
        return asset
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy số dư: {e}')
        time.sleep(5)
        return user_asset(headers)

def print_stats_cdtd(stats, headers, config):
    try:
        current_asset = user_asset(headers)
        profit = current_asset[config['Coin']] - stats['asset_0']
        
        prints(247, 255, 97,"═" * 47)
        prints(70, 240, 234,'Thống kê:')
        prints(50, 237, 65,f"Số trận thắng : {stats['win']}/{stats['win'] + stats['lose']}")
        
        win_rate = 0
        if stats['win'] + stats['lose'] > 0:
            win_rate = stats['win'] / (stats['lose'] + stats['win']) * 100
        prints(0, 255, 20, f'Tỉ lệ thắng {win_rate:.2f}%')

        prints(255, 0, 0, f"Chuỗi thua : {stats['consecutive_lose']} (Tối đa: {config['consecutive_loss_stop']})")
        
        if profit >= 0:
            prints(0, 255, 20, f"Lãi: {profit:.4f} {config['Coin']}")
        else:
            prints(255, 0, 0, f"Lỗ: {profit:.4f} {config['Coin']}")
        
        prints(255, 165, 0, f"Mức cược hiện tại: {config['current_coins']:.4f} {config['Coin']}")

        if config['games_to_play'] > 0:
            prints(100, 100, 255, f"Số ván trong phiên: {stats['games_played']}/{config['games_to_play']}")
            if stats['games_to_skip'] > 0:
                prints(255, 255, 0, f"Đang nghỉ, còn lại {stats['games_to_skip']} ván.")

        prints(247, 255, 97,"═" * 47)
    except Exception as e:
        prints(255,0,0,f'Lỗi khi in thống kê: {e}')

def print_wallet(asset):
    prints(247, 255, 97,"═" * 47)
    prints(238, 250, 7,'SỐ DƯ CỦA BẠN:')
    prints(23, 232, 159,f" USDT:{asset['USDT']:.4f}    WORLD:{asset['WORLD']:.4f}    BUILD:{asset['BUILD']:.4f}".center(50))
    prints(247, 255, 97,"═" * 47)

def bet_cdtd(headers, ki, config, selected_champions):
    prints(255,255,0,f"Chuẩn bị đặt cược cho kì #{ki}:")
    for champion_id in selected_champions:
        try:
            json_data = {
                'issue_id': int(ki),
                'bet_group': 'winner',
                'asset_type': config['Coin'],
                'athlete_id': champion_id,
                'bet_amount': config['current_coins'],
            }
            response = requests.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data).json()
            if response.get('code') == 0 and response.get('msg') == 'ok':
                prints(0, 255, 19, f"    -> Đã đặt {config['current_coins']} {config['Coin']} cho '{NV[champion_id]}' thành công.")
            else:
                prints(255, 0, 0, f"    -> Lỗi khi đặt cho '{NV[champion_id]}': {response.get('msg', 'Lỗi không xác định')}")
        except Exception as e:
            prints(255,0,0,f"    -> Lỗi nghiêm trọng khi đặt cược cho '{NV[champion_id]}': {e}")
        time.sleep(0.5) # Thêm độ trễ nhỏ giữa các lần cược


def main_cdtd():
    banner("CHẠY ĐUA TỐC ĐỘ")
    data=load_data_cdtd()
    config=load_config_cdtd()

    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://xworld.info/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }
    
    initial_asset = user_asset(headers)
    stats={
        'win': 0,
        'lose': 0,
        'consecutive_lose': 0,
        'asset_0': initial_asset[config['Coin']],
        'games_played': 0,
        'games_to_skip': 0,
    }

    while True:
        clear_screen()
        banner('CHẠY ĐUA TỐC ĐỘ')
        current_asset = user_asset(headers)
        print_wallet(current_asset)
        
        data_top10_cdtd = top_10_cdtd(headers)
        data_top100_cdtd = top_100_cdtd()
        print_data(data_top10_cdtd, data_top100_cdtd)
        
        print_stats_cdtd(stats, headers, config)

        # Kiểm tra điều kiện dừng
        profit = current_asset[config['Coin']] - stats['asset_0']
        if profit >= config['take_profit']:
            prints(0, 255, 0, f"Đã đạt mục tiêu chốt lời! Dừng tool. Lãi: {profit:.4f} {config['Coin']}")
            break
        if -profit >= config['stop_loss']:
            prints(255, 0, 0, f"Đã chạm ngưỡng cắt lỗ! Dừng tool. Lỗ: {profit:.4f} {config['Coin']}")
            break
        if stats['consecutive_lose'] >= config['consecutive_loss_stop'] and config['consecutive_loss_stop'] > 0:
            prints(255, 0, 0, f"Đã thua {stats['consecutive_lose']} ván liên tiếp! Dừng tool.")
            break

        # Logic nghỉ
        if stats['games_to_skip'] > 0:
            prints(255, 255, 0, f"Ván này nghỉ, bỏ qua đặt cược. Còn lại {stats['games_to_skip']} ván nghỉ.")
            stats['games_to_skip'] -= 1
            next_issue = data_top10_cdtd[0][0] + 1
            prints(100, 100, 255, f"Đang chờ qua kì #{next_issue}...")
            # Đợi cho đến khi kì tiếp theo kết thúc
            while True:
                latest_issue = top_10_cdtd(headers)[0][0]
                if latest_issue >= next_issue:
                    prints(0, 255, 0, f"Kì #{next_issue} đã kết thúc. Chuẩn bị cho ván tiếp theo.")
                    break
                time.sleep(5)
            time.sleep(10)
            continue
            
        kqs_dat = selected_NV_enhanced(data_top100_cdtd)
        prints(247, 255, 97,"═" * 47)
        prints(0, 246, 255, f'BOT CHỌN ĐẶT QUÁN QUÂN: {", ".join([NV[kq] for kq in kqs_dat])}')
        prints(247, 255, 97,"═" * 47)
        
        next_ki = data_top10_cdtd[0][0] + 1
        bet_cdtd(headers, next_ki, config, kqs_dat)
        
        result = kiem_tra_kq_cdtd(headers, kqs_dat, next_ki)
        
        if result: # Thắng
            stats['win'] += 1
            stats['consecutive_lose'] = 0
            # Reset bet amount to initial on win
            config['current_coins'] = config['initial_coins']
        else: # Thua
            stats['lose'] += 1
            stats['consecutive_lose'] += 1
            # Multiply bet amount on loss if enabled
            if config['use_multiplier']:
                config['current_coins'] *= config['loss_multiplier']
        
        stats['games_played'] += 1

        # Logic bắt đầu nghỉ
        if config['games_to_play'] > 0 and stats['games_played'] >= config['games_to_play']:
            prints(255, 165, 0, f"Đã chơi {stats['games_played']} ván. Bắt đầu nghỉ {config['games_to_rest']} ván.")
            stats['games_to_skip'] = config['games_to_rest']
            stats['games_played'] = 0

        time.sleep(10)

if __name__ == "__main__":
    try:
        main_cdtd()
    except KeyboardInterrupt:
        prints(255, 0, 0, "\nĐã dừng tool theo yêu cầu của người dùng.")
