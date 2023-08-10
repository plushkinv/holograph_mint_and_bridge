from eth_abi import encode
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
        web3 = Web3(Web3.HTTPProvider(fun.address['polygon']['rpc'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address

        log(f"I-{i}: Начинаю работу с {wallet}")
        
        flag_no_money = 1
        networks = config.network4mint
        random.shuffle(networks)
        for network in networks:
            if fun.get_token_balance_USD(wallet, network, fun.address[network]['native']) >= config.min_balance_4_main:
                flag_no_money = 0
                break
        
        if flag_no_money == 1:
            log_error("Не достаточно нативнки на кошельке чтобы сминтить")
            save_wallet_to("no_money", private_key)
            save_wallet_to("no_money_aw", wallet)
            continue

        log(f"выбрана сеть для минта {network}")
        fee = config.protocol_fee[network] * (1 + random.randint(100000000,999999999)/10000000000)
        
        web3 = Web3(Web3.HTTPProvider(fun.address[network]['rpc'], request_kwargs=config.request_kwargs))
       
        dapp_abi = json.load(open('abi/nft_abi.json'))
        dapp_address = web3.to_checksum_address(config.NFT_adress)
        dapp_contract = web3.eth.contract(address=dapp_address, abi=dapp_abi)



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
                'value': web3.to_wei(fee , "ether"),
                'maxFeePerGas': maxFeePerGas,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,    
                'nonce': nonce
            })
        else:
            transaction = dapp_contract.functions.purchase(config.count_nfts).build_transaction({
                'from': wallet,
                'value': web3.to_wei(fee , "ether"),
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
    


    fun.timeOut("teh")

###########
    try:
        HolographBridgeAddress = Web3.to_checksum_address('0xD85b5E176A30EdD1915D6728FaeBD25669b60d8b')
        LzEndAddress = Web3.to_checksum_address('0x3c2269811836af69497E5F486A85D7316753cf62')
        nftAddress = Web3.to_checksum_address(config.NFT_adress)    
        
        networks = config.network4mint
        random.shuffle(networks)
        balance = 0
        for network in networks:
            web3 = Web3(Web3.HTTPProvider(fun.address[network]['rpc'], request_kwargs=config.request_kwargs))
            ntf = web3.eth.contract(address=nftAddress, abi=dapp_abi)
            balance = ntf.functions.balanceOf(wallet).call()
            if balance >= 1:
                log(f'Нашел NFT в количестве {balance} в сети {network}')
                break

        if balance == 0:
            log (f'Не нашел НФТ в этом кошельке')
            save_wallet_to("NFT_not_have", private_key)
            continue
        
        networks = config.network4bridge.copy()
        if network in networks:
            networks.remove(network)
        to_network=random.choice(networks)
        log(f'Хочу отправить в {to_network}')

        holograph_contract = web3.eth.contract(address=HolographBridgeAddress, abi=fun.holo_abi)
        lzEndpoint_contract = web3.eth.contract(address=LzEndAddress, abi=fun.lzEndpoint_abi)


        nft_id = ntf.functions.tokensOfOwner(wallet).call()[0]
        payload = web3.to_hex(encode(['address', 'address', 'uint256'], [wallet, wallet, nft_id]))
        to_gas_price = fun.address[to_network]['holograph_gas']
        to_gas_limit = random.randint(450000, 500000)    
 
    

        lzFee = lzEndpoint_contract.functions.estimateFees(fun.address[to_network]['dstChainId'],HolographBridgeAddress,'0x',False,'0x').call()[0]
        lzFee = int(lzFee * 2.5)    

        balance = 0
        balance = web3.eth.get_balance(wallet)
        if balance < lzFee * 1.1:
            fun.log_error(f'Не достаточно нативки для оплаты газа')
            save_wallet_to("NFT_bridge_no_money", private_key)
            save_wallet_to("NFT_bridge_no_money_aw", wallet)
            continue 
            
    except Exception as error:
        error_str = str(error)
        fun.log_error(f'NFT bridge false: {error}')
        save_wallet_to("NFT_bridge_error", private_key)   
        continue  

    trying = 0 
    while True:
        trying += 1 
        log(f"попытка {trying}")
        fun.timeOut("teh")
        try:

            if  fun.address[network]['type']:
                maxPriorityFeePerGas = web3.eth.max_priority_fee
                fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
                baseFee=round(mean(fee_history['baseFeePerGas']))
                maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)
                transaction = holograph_contract.functions.bridgeOutRequest(
                    fun.address[to_network]['holograph_id'], 
                    nftAddress, 
                    to_gas_limit, 
                    to_gas_price, 
                    payload
                    ).build_transaction({
                    'from': wallet,
                    'value': lzFee,
                    'maxFeePerGas': maxFeePerGas,
                    'maxPriorityFeePerGas': maxPriorityFeePerGas,   
                    'nonce': web3.eth.get_transaction_count(wallet),
                })
            else:
                gasPrice = web3.eth.gas_price
                transaction = holograph_contract.functions.bridgeOutRequest(fun.address[to_network]['holograph_id'], nftAddress, to_gas_limit, to_gas_price, payload).build_transaction({
                    'from': wallet,
                    'value': lzFee,
                    'gasPrice': gasPrice,
                    'nonce': web3.eth.get_transaction_count(wallet),
                })
                gasLimit = web3.eth.estimate_gas(transaction)
                transaction['gas'] = int(gasLimit * config.gas_kef) 


            # Подписываем и отправляем транзакцию
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
            tx_result = web3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_result['status'] == 1:
                fun.log_ok(f'NFT _bridge OK: {tx_hash}')
                break
            else:
                fun.log_error(f'NFT bridge false: {tx_hash}')

        except Exception as error:
            error_str = str(error)
            fun.log_error(f'NFT bridge false: {error}')

        if trying > 3 :
            fun.log_error("Ниче не получается! ищи этот кошелек в логах NFT_bridge_error")
            save_wallet_to("NFT_bridge_error", private_key)   
            break            


        
    fun.timeOut()    





















log("Ну типа все!")