import json
import os
from datetime import datetime
import random
from statistics import mean
import time
from web3 import Web3
import config


# option bsc / avax / fantom / polygon / arbitrum / optimism
address = {
    'polygon': {
        'type': 2,
        'chainId': 137,
        'rpc': config.rpc_links['polygon'],
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'MATIC': 'native',
        'native': 'MATIC',
        'WMATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
        'dstChainId': 109,
        'holograph_id': 4,
        'holograph_gas': 400000000000,
    },
    'arbitrum': {
        'type': 2,
        'rpc': config.rpc_links['arbitrum'],
        'USDC': '0xff970a61a04b1ca14834a43f5de4533ebddb5cc8',
        'USDT': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        'ETH': 'native',
        'native': 'ETH',
        'WETH': '0x82af49447d8a07e3bd95bd0d56f35241523fbab1',
        'dstChainId': 110,
        'holograph_id': 6,
        'holograph_gas': 131250001,
    },
    'optimism': {
        'type': 2,
        'rpc': config.rpc_links['optimism'],
        'USDC': '0x7f5c764cbc14f9669b88837ca1490cca17c31607',
        'ETH': 'native',
        'native': 'ETH',
        'WETH': '0x4200000000000000000000000000000000000006',
        'dstChainId': 111,
        'holograph_id': 7,
        'holograph_gas': 10000001,
    },
    'bsc': {
        'type': 0,
        'chainId': 56,
        'rpc': config.rpc_links['bsc'],
        'USDT': '0x55d398326f99059ff775485246999027b3197955',
        'BUSD': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
        'BNB': 'native',
        'native': 'BNB',
        'WBNB': '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
        'dstChainId': 102,
        'holograph_id': 2,
        'holograph_gas': 4500000000,
    },
    'fantom': {
        'type': 2,
        'rpc': config.rpc_links['fantom'],
        'USDC': '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75',
        'FTM': 'native',
        'native': 'FTM',
        'WFTM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
    
    },
    'avax': {
        'type': 2,
        'chainId': 43114,        
        'rpc': config.rpc_links['avax'],
        'USDC': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDT': '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7',
        'AVAX': 'native',
        'native': 'AVAX',
        'WAVAX': '0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7',
        'dstChainId': 106,
        'holograph_id': 3,
        'holograph_gas': 37500000000,
    },


}

erc20_abi = json.load(open('abi/erc20_abi.json'))
holo_abi = json.load(open('abi/holo_abi.json'))
lzEndpoint_abi = json.load(open('abi/lzEndpoint_abi.json'))

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"


def get_token_balance(wallet, network, token ):
    try:
        web3 = Web3(Web3.HTTPProvider(address[network]['rpc'], request_kwargs=config.request_kwargs))
        wallet = Web3.to_checksum_address(wallet)

        if address[network][token]=="native":
            balance = web3.eth.get_balance(wallet)
            balance = Web3.from_wei(balance, 'ether')
        else:
            erc20_address = web3.to_checksum_address(address[network][token])
            erc20_contract = web3.eth.contract(address=erc20_address, abi=erc20_abi)
            token_decimals = erc20_contract.functions.decimals().call()
            balance = erc20_contract.functions.balanceOf(wallet).call() / 10 ** token_decimals
        time.sleep(2)    
            
        return balance

    except Exception as error:
        return log_error(f'{network} {token} | Ошибка при получении баланса токенов: Проблема либо в rpc, либо в связке rpc-proxy, либо проблемы с самой сетью.')


def get_token_balance_USD(wallet, network, token ):
    try:
        result = get_token_balance(wallet, network, token )
        if result == "error":
            return "error"
        balance = float(result)
        return balance*config.prices[token]

    except Exception as error:
        return log_error(f'{network} {token} | Ошибка при переводе баланса токенов в USD: {error}')


def log(text, status=""):
    now = datetime.now()
    log_text = now.strftime('%d %H:%M:%S')+": "
    with open(log_file, "a", encoding='utf-8') as f:
        if status == "error":
            color_code = "\033[91m"  # red
            log_text = log_text + "ERROR: "
        elif status == "ok":
            color_code = "\033[92m"  # green
            log_text = log_text + "OK: "
        else:
            color_code = "\033[0m"  # white
        log_text = log_text + f"{text}"
        log_text_color = f"{color_code}{log_text}\033[0m"
        f.write(log_text + "\n")
        print(log_text_color)

def log_error(text):
    log(text, "error")
    return "error"

def log_error_critical(text):
    log(text, "error")
    f=open(f"{log_dir}/critical.log", "a", encoding='utf-8')
    f.write(text + "\n")    
    return "error"

def log_ok(text):
    log(text, "ok")
    return "ok"

def save_wallet_to(filename, wallet):
    f=open(f"{log_dir}/{filename}.log", "a", encoding='utf-8')
    f.write(wallet + "\n")  

def timeOut(type="main"):
    if type=="main":
        time_sleep=random.randint(config.timeoutMin, config.timeoutMax)
    if type=="teh":
        time_sleep=random.randint(config.timeoutTehMin, config.timeoutTehMax)
        
    if int(time_sleep/60) > 0:
        log(f"пауза {int(time_sleep/60)} минут")
    time.sleep(time_sleep)

