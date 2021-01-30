from config import config, project_dir
from telethon import TelegramClient, events
from telethon.tl.custom import Button
import logging
import datetime
import service.yandex_iot

logging.basicConfig(level=logging.INFO)
yandex_iot = service.yandex_iot.YandexIot(config['yandex_iot']['session_id'].get(), config['yandex_iot']['yandexuid'].get())
bot = TelegramClient(project_dir + '/var/sessions/' + config['telegram_bot']['name'].get(), config['telegram_app']['api_id'].get(), config['telegram_app']['api_hash'].get()).start(bot_token=config['telegram_bot']['token'].get())

def is_admin(user_id):
    if user_id in config['telegram_bot']['admins'].get():
        return True
    else:
        return False

def get_devices_keyboard():
    response = yandex_iot.get_devices_request()
    if response:
        buttons = []
        for room in response['rooms']:
            buttons.append([
                Button.inline('🚪' + room['name'], bytes('device_update_info', 'utf-8'))
            ])
            for device in room['devices']:
                is_active = False
                for capability in device['capabilities']:
                    if capability['state']['instance'] == 'on' and capability['state']['value']:
                        is_active = True
                power = None
                for property in device['properties']:
                    if property['parameters']['instance'] == 'power':
                        power = property['state']['value']
                        break
                if device['name'] == 'Елка':
                    device_icon = '🎄'
                elif device['name'] == 'Увлажнитель':
                    device_icon = '💧'
                elif device['name'] == 'Робот':
                    device_icon = '🤖'
                elif device['type'] == 'devices.types.light':
                    device_icon = '💡'
                else:
                    device_icon = '🔌'
                buttons.append([
                    Button.inline(device_icon + ' ' + device['name'] + ' ' + ((str(power) + 'W') if is_active and power else ''), bytes('device_update_info', 'utf-8')),
                    Button.inline(('🟢 Выключить' if is_active else '🔴  Включить'), bytes('device_turn_off_' + device['id'], 'utf-8') if is_active else bytes('device_turn_on_' + device['id'], 'utf-8'))
                ])
        return buttons
    return False

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('/devices — получить данные об устройствах')

@bot.on(events.NewMessage(pattern='/id'))
async def id(event):
    sender = await event.get_sender()
    await event.reply(str(sender.id))

@bot.on(events.NewMessage(pattern='/devices'))
async def devices(event):
    sender = await event.get_sender()
    if is_admin(sender.id):
        chat = await event.get_chat()
        keyboard = get_devices_keyboard()
        if keyboard:
            await bot.send_message(chat, 'Данные на ' + datetime.datetime.now().strftime('%H:%M:%S'), buttons=keyboard)
        else:
            await event.reply('Не удалось получить данные из Яндекса')
    else:
        await event.reply('У вас нет доступа')

@bot.on(events.CallbackQuery(pattern=r'device_update_info'))
async def device_update_info(event):
    sender = await event.get_sender()
    if is_admin(sender.id):
        keyboard = get_devices_keyboard()
        if keyboard:
            await event.edit(text='Данные на ' + datetime.datetime.now().strftime('%H:%M:%S'), buttons=keyboard)
            await event.answer('Данные обновлены')
        else:
            await event.answer('Не удалось получить данные из Яндекса')
    else:
        await event.answer('У вас нет доступа')

@bot.on(events.CallbackQuery(pattern=r'device_turn_.*'))
async def device_turn_on_off(event):
    sender = await event.get_sender()
    if is_admin(sender.id):
        data = event.data.decode("utf-8").split('_')
        device_id = data[-1]
        on = True if data[-2] == 'on' else False
        csrf_token = yandex_iot.get_csrf_token()
        if csrf_token:
            response = yandex_iot.toggle_device(device_id, on)
            if response:
                keyboard = get_devices_keyboard()
                if keyboard:
                    await event.edit(text='Данные на ' + datetime.datetime.now().strftime('%H:%M:%S'), buttons=keyboard)
                if on:
                    await event.answer('🟢 Устройство включено')
                else:
                    await event.answer('🔴 Устройство выключено')
            else:
                await event.answer('😞 Не удалось включить/выключить устройство')
        else:
            await event.answer('Не удалось получить данные из Яндекса')
    else:
        await event.answer('У вас нет доступа')

bot.run_until_disconnected()