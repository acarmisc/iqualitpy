from collections import namedtuple


class IqResponse(object):

    def __init__(self, raw):
        self.raw = raw
        try:
            self.full_response = raw.json()
        except Exception as e:
            raise ValueError("Error decoding response {}".format(raw))

        self.payload = self.full_response.get('payload')
        self.response_type = self.full_response.get('response_type')


class IqDevice(object):

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.time_tracking = kwargs.get('time_tracking')
        self.attendance_only = kwargs.get('attendance_only')
        self.mac_addr = kwargs.get('mac_addr') # TODO: to be removed
        self.enrollment_on = kwargs.get('enrollment_on')
        self.location = kwargs.get('location')
        self.enabled = kwargs.get('enabled')
        self.organization = namedtuple("Organization", kwargs.get('organization').keys())(*kwargs.get('organization').values())

    def __repr__(self):
        return "<iqUser {}@{} >".format(self.name, self.organization.name)

    def as_data(self):
        raise NotImplemented


class IqUser(object):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.get('token')
        user_base = kwargs.get('user')
        self.username = user_base.get('username')
        self.organization = namedtuple("Organization", user_base.get('organization').keys())(
            *user_base.get('organization').values())

    def __repr__(self):
        return "<iqUser {}@{}>".format(self.username, self.organization.name)

    def as_data(self):
        raise NotImplemented


class IqProject(object):

    def __init__(self, id, name, organization, employees=None, state=None):
        self.id = id
        self.name = name
        self.organization = organization
        self.employees = employees
        self.state = state

    def __repr__(self):
        return "<iqProject {}>".format(self.name)

    def as_data(self):
        raise NotImplemented


class IqTimeTrack(object):

    def __init__(self, user, date_spent, amount):
        self.user = user
        self.date_spent = date_spent
        self.amount = amount

    def __repr__(self):
        return "<iqTimeTrack {} on {}>".format(self.user, self.date_spent)

    def as_data(self):
        raise NotImplemented
