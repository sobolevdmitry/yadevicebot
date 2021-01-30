YaDeviceBot
=========
Just another weekend project

![Screenshot](https://raw.githubusercontent.com/sobolevdmitry/yadevicebot/main/img/screenshot.jpg)
## Getting Started
- You must have Python 3 and PyPi installed in your system (see <https://python.org> and <https://pypi.python.org/pypi/pip> for more)
- Clone this repository and create a new folder `./var/sessions`
- Install requirements: `python3 -m pip install -r requirements.txt`
- Set up configuration files (see below)
- Now you can start bot: `bash ./start.sh` or `python3 ./main.py`
## Config files
Copy *.default.yaml to *.yaml and set up your files
### telegram_app.yaml
- Get your own api id and hash here: <https://my.telegram.org/>
### telegram_bot.yaml
- Get your bot token here: <https://t.me/botfather>
- Set bot admin ids
### yandex_iot.yaml
- Get your session id and yandexuid from cookies here: <https://yandex.ru>