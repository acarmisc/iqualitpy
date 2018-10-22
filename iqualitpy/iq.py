from collections import namedtuple
from datetime import datetime

import requests

from iqualitpy.entities import IqResponse, IqDevice, IqUser


class api():

    @staticmethod
    def post(*args, **kwargs):
        res = requests.post(*args, **kwargs)

        return IqResponse(res)

    @staticmethod
    def secure_post(*args, token=None, **kwargs):
        if not token:
            raise ValueError("Missing token for secure request")

        res = requests.post(*args, headers=dict(Authorization="Token {}".format(token)), **kwargs)

        return IqResponse(res)


class IqClient(object):

    def __init__(self, token, host=None, api_version=None, is_device=False):
        self.host = host or "http://saas.iquality.it"
        self.token = token
        self.api_version = api_version or '1.0'
        self.is_device = is_device

        self.base_url = "{}/api/".format(self.host)
        self.device = self.me() if is_device else None

    def me(self):
        if self.is_device:
            r = api.post("{}devices/auth_device".format(self.base_url), data=dict(token=self.token))
            self.device = IqDevice(**r.payload)
            return self.device

        raise NotImplemented

    def get_user(self, badge):
        if not self.is_device:
            raise ValueError('Only devices can get user')

        r = api.post("{}devices/badges".format(self.base_url), data=dict(badge_code=badge, mac_addr=self.device.mac_addr))
        if r.payload and not self.in_enrollment():
            return IqUser(**r.payload)

        return None

    def update_settings(self):
        if not self.is_device:
            raise ValueError('Only devices has settings')

    def device_beat(self):
        # TODO: check for different method
        import socket
        local_ip = socket.gethostbyname(socket.gethostname()) or ''
        if not self.is_device:
            raise ValueError('Only devices settings')

        api.post("{}devices/beat".format(self.base_url), data=dict(mac_addr=self.device.mac_addr, ip_addr=local_ip))

    def post_attendancetrack(self, user, direction, timestamp=None, coordinates=None):
        data = dict(direction=direction, coordinates=coordinates)
        if self.device:
            data.update(dict(mac_addr=self.device.mac_addr))

        r = api.secure_post("{}attendance/tracks/".format(self.base_url), token=user.token,
                            data=data)
        return r.payload

    def post_timetrack(self):
        raise NotImplemented

    def get_attendancetrack(self):
        raise NotImplemented

    def get_projects(self):
        raise NotImplemented

    def get_activities(self):
        raise NotImplemented

    def in_enrollment(self):
        device = self.me()
        return device.enrollment_on

    def start_timer(self):
        raise NotImplemented

    def stop_timer(self):
        raise NotImplemented

    def telegram_bind_user(self, pin, mobile, chat):
        data = dict(pin=pin, mobile=mobile, chat=chat)
        r = api.secure_post("{}commons/telegram_bind_user".format(self.base_url), token=self.token,
                            data=data)      
        print(r.raw)  
        return r.payload


if __name__ == '__main__':
    TOKEN = '2792737710'
    MAC_ADDR = '27:92:73:77:10'
    BADGE = '00519695687075'

    iq = IqClient(TOKEN, is_device=True)

    print('Calling {} using token {}'.format(iq.base_url, TOKEN))

    print('--- me() ---')
    device = iq.me()
    print(device)

    print('--- beat() ---')
    print(iq.in_enrollment())

    print('--- get_user() ---')
    user = iq.get_user(BADGE)
    print(user)
    print(user.token)

    print('--- post_attendancetrack() ---')
    timetrack = iq.post_attendancetrack(user, direction='IN')
    print(timetrack)

    iq.device_beat()
