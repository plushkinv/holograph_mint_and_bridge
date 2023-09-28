import json
from statistics import mean
import time
from web3 import Web3
import requests
import random
from datetime import datetime
import config
import fun
from fun import log, log_error, log_ok, save_wallet_to


current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')


keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key = row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i += 1
    if random.randint(0, 100) < config.veroyatnost_minta:
        log("skip")
        continue
        
    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    try:
        fun.get_new_prices()

        web3 = Web3(Web3.HTTPProvider(fun.address['polygon']['rpc'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address

        log(f"I-{i}: Начинаю работу с {wallet}")
        
        flag_no_money = 1
        networks = config.network4mint
        random.shuffle(networks)
        for network in networks:
            if fun.get_token_balance_USD(wallet, network, fun.address[network]['native']) >= 0.1*config.count_nfts:
                flag_no_money = 0
                break
        
        if flag_no_money == 1:
            log_error("Не достаточно нативнки на кошельке чтобы сминтить")
            save_wallet_to("no_money", private_key)
            save_wallet_to("no_money_aw", wallet)
            continue

        log(f"выбрана сеть для минта {network}")
        
        
        web3 = Web3(Web3.HTTPProvider(fun.address[network]['rpc'], request_kwargs=config.request_kwargs))
    
        dapp_abi = json.load(open('abi/nft_abi.json'))
        dapp_address = web3.to_checksum_address(config.NFT_adress)
        dapp_contract = web3.eth.contract(address=dapp_address, abi=dapp_abi)
        fee = int(dapp_contract.functions.getHolographFeeWei(config.count_nfts).call()*1.03)
        

        if fun.address[network]['type']:
            maxPriorityFeePerGas = web3.eth.max_priority_fee
            fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
            baseFee=round(mean(fee_history['baseFeePerGas']))
            maxFeePerGas = maxPriorityFeePerGas + round(baseFee * 1.5)
        else:
            gasPrice = web3.eth.gas_price  
        nonce = web3.eth.get_transaction_count(wallet)
            
        if fun.address[network]['type']:
            transaction = dapp_contract.functions.purchase(config.count_nfts).build_transaction({
                'from': wallet,
                'value': fee,
                'maxFeePerGas': maxFeePerGas,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,    
                'nonce': nonce
            })
        else:
            transaction = dapp_contract.functions.purchase(config.count_nfts).build_transaction({
                'from': wallet,
                'value': fee,
                'gasPrice': gasPrice,
                'nonce': nonce
            })
            gasLimit = web3.eth.estimate_gas(transaction)
            transaction['gas'] = int(gasLimit * 1.3)

    
        # Подписываем и отправляем транзакцию
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_result['status'] == 1:
            log_ok(f'mint OK: {tx_hash}')
        else:
            log_error(f' mint false: {tx_hash}')
            save_wallet_to("mint_error", private_key)
            continue
                
    except Exception as error:
        log_error(f' mint false: {error}')
        save_wallet_to("mint_error", private_key)
        continue
    

    fun.timeOut()

log("Ну типа все!")