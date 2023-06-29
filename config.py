
#то что ниже обязательно заполнить своими данными
proxy_use = 0 #  0 - не использовать, 1 - прокси без ссылки , 2 - прокси со ссылкой для смены ip
proxy_login = 'pfds464'
proxy_password = '9c3a07'
proxy_address = 'no.com'
proxy_port = '157'
proxy_changeIPlink = "http:/5cce3b204"


#то что ниже желательно настроить под себя
NFT_adress = "0x6d6768a0b24299bede0492a4571d79f535c330d8"
count_nfts = 1  # количество сколько хотите сминтить
network4mint = ['avax', 'polygon', 'bsc', 'arbitrum', 'optimism']  # выберите сети, в одной из них будет случайно сминчена НФТ
network4bridge = ['avax', 'polygon', 'bsc', 'arbitrum', 'optimism']  # выберите сети, в одну из них будет будет отправлена НФТ через мост


#укажите паузу в работе между кошельками, минимальную и максимальную. 
#При смене каждого кошелька будет выбрано случайное число. Значения указываются в секундах
timeoutMin = 10 #минимальная 
timeoutMax = 30 #максимальная
#задержки между операциями в рамках одного кошелька
timeoutTehMin = 3 #минимальная 
timeoutTehMax = 10 #максимальная



#то что ниже можно менять только если понимаешь что делаешь
proxies = { 'all': f'http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}',}
if proxy_use:
    request_kwargs = {"proxies":proxies, "timeout": 120}
else:
    request_kwargs = {"timeout": 120}
gas_kef=1.5 #коэфициент допустимого расхода газа на подписание транзакций. можно выставлять от 1.3 до 2

rpc_links = {
    'polygon': 'https://polygon-rpc.com/',
    'arbitrum': 'https://arb1.arbitrum.io/rpc',
    'optimism':  'https://rpc.ankr.com/optimism',
    'bsc': 'https://bscrpc.com',
    'fantom': 'https://rpc.ftm.tools/',
    'avax': 'https://api.avax.network/ext/bc/C/rpc',
}

prices = {
    "MATIC": 0.645,
    "AVAX": 11.8,
    "BNB": 246,
    "ETH": 1900,
}