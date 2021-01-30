import requests

class YandexIot:
    iot_url = 'https://iot.quasar.yandex.ru/m/user'

    def __init__(self, session_id, yandexuid):
        self.__session_id = session_id
        self.__yandexuid = yandexuid

    def get_devices_request(self):
        try:
            r = requests.get(self.iot_url + '/devices', cookies={'Session_id': self.__session_id})
            if r.ok:
                return r.json()
        except:
            return None

    def toggle_device(self, device_id, on = False):
        try:
            json = {
                'actions': [
                    {
                        'type': 'devices.capabilities.on_off',
                        'state': {
                            'instance': 'on',
                            'value': on
                        }
                    }
                ]
            }
            r = requests.post(self.iot_url + '/devices/' + device_id + '/actions', cookies={'Session_id': self.__session_id, 'yandexuid': self.__yandexuid}, headers={'x-csrf-token': self.__csrf_token}, json=json)
            if r.ok:
                return r.json()
        except:
            return None

    def get_csrf_token(self):
        try:
            r = requests.get('https://yandex.ru/quasar?storage=1', cookies={'Session_id': self.__session_id, 'yandexuid': self.__yandexuid})
            if r.ok:
                data = r.json()
                self.__csrf_token = data['storage']['csrfToken2']
                return True
        except:
            return None