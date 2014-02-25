__author__ = 'nikolay'

from google.appengine.ext import ndb


class User(ndb.Model):
    user_id = ndb.StringProperty()
    user_object = ndb.UserProperty()
    devices = ndb.KeyProperty(repeated=True)


class Device(ndb.Model):
    device_id = ndb.StringProperty()


class DeviceSpecificModel(ndb.Model):
    device = ndb.KeyProperty()

    @classmethod
    def query(cls, user, *args, **kwargs):
        if not isinstance(user, ndb.Key):
            raise TypeError()
        if user.kind() == 'User':
            devices = user.get().devices
            devices.append(user)
            filt = cls.device.IN(devices)
        elif user.kind() == 'Device':
            filt = cls.device == user
        else:
            raise ValueError()
        return super(DeviceSpecificModel, cls).query(filt, *args, **kwargs)


def get_device(device_id):
    return Device.query(Device.device_id == device_id).get(keys_only=True) or Device(device_id=device_id).put()


def get_user_by_device(device_id):
    device = get_device(device_id)
    user = User.query(User.devices == device).get(keys_only=True)
    if user is None:
        return device, device
    else:
        return device, user