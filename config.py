import os
import confuse
project_dir = os.getcwd()
config = confuse.Configuration('yadevicebot', __name__)
config.set_file(project_dir + '/config/telegram_app.default.yaml')
config.set_file(project_dir + '/config/telegram_bot.default.yaml')
config.set_file(project_dir + '/config/yandex_iot.default.yaml')
config.set_file(project_dir + '/config/telegram_app.yaml')
config.set_file(project_dir + '/config/telegram_bot.yaml')
config.set_file(project_dir + '/config/yandex_iot.yaml')