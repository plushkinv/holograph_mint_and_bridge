#Автор
PLushkin https://t.me/plushkin_blog        

**На чай с плюшками автору:**
Полигон, БСК, Арбитрум - любые токены - `0x79a266c66cf9e71Af1108728e455E0B1D311e95E`
Трон TRC-20 только USDT, остальное не доходит - `TEZG4iSmr31wWnvBixKgUN9Aax4bbgu1s3`

#Чё делает

3 варианта работы:
1️⃣mint.py - минтит НФтшку в слуйчано сети , сеть выбирается из тех где хватает денег для минта.
2️⃣bridge.py - находит в одной из этих сетей новую НФТ и отправляет ее в случйаную сеть 
3️⃣main.py - вначале минтит в случайной сети , потом сразу отправляет в случайную сеть через мост.

можно использовать прокси кому надо и настраивать задержки между кошельками.



#Запуск

1. перед запуском добавьте приватные ключи в private_keys.txt
2. настройте config.py под себя
3. перед очередным запуском, в config.py, в самом низу заполните актуальные цены
4. Установка и запуск: 

Linux/Mac
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```
Windows - https://www.youtube.com/watch?v=EqC42mnbByc&t=6s
```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```




