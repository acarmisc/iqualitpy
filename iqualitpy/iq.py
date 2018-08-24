from collections import namedtuple
from datetime import datetime

import requests

from iqualitpy.entities import IqResponse, IqDevice, IqUser


class api():

    @staticmethod
    def post(*args, **kwargs):
        res = requests.post(*args, **kwargs,)

        return IqResponse(res)

    @staticmethod
    def secure_post(*args, token=None, **kwargs):
        if not token:
            raise ValueError("Missing token for secure request")

        res = requests.post(*args, **kwargs, headers=dict(Authorization="Token {}".format(token)))

        return IqResponse(res)


class IqClient(object):

    def __init__(self, token, host=None, api_version=None, is_device=False):
        self.host = host or "http://saas.iquality.it"
        self.token = token
        self.api_version = api_version or '1.0'
        self.is_device = is_device
        self.device = None

        self.base_url = "{}/api/".format(self.host)

    def me(self):
        if self.is_device:
            r = api.post("{}devices/auth_device".format(self.base_url), data=dict(token=self.token))
            self.device = IqDevice(**r.payload)
            return self.device

        raise NotImplemented

    def get_user(self, badge):
        if not self.is_device:
            raise ValueError('Only devices settings')

        r = api.post("{}devices/badges".format(self.base_url), data=dict(badge_code=badge, mac_addr=self.device.mac_addr))
        return IqUser(**r.payload)

    def update_settings(self):
        if not self.is_device:
            raise ValueError('Only devices settings')
        raise NotImplemented

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


if __name__ == '__main__':
    TOKEN =
    MAC_ADDR =
    BADGE =

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