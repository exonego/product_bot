from dataclasses import dataclass, field

from . import users
from . import actions
from . import paid_users


@dataclass
class Users:
    @property
    def get_user(self):
        return users.get_user

    @property
    def add_user(self):
        return users.add_user

    @property
    def set_role(self):
        return users.set_role

    @property
    def set_banned(self):
        return users.set_banned

    @property
    def set_is_alive(self):
        return users.set_is_alive


@dataclass
class Actions:
    pass


@dataclass
class PaidUsers:
    @property
    def get_user(self):
        return paid_users.get_user

    @property
    def add_user(self):
        return paid_users.add_user

    @property
    def set_role(self):
        return paid_users.set_role

    @property
    def set_banned(self):
        return paid_users.set_banned

    @property
    def set_is_alive(self):
        return paid_users.set_is_alive


@dataclass
class Requests:
    users: Users = field(default_factory=Users)
    actions: Actions = field(default_factory=Actions)
    paid_users: PaidUsers = field(default_factory=PaidUsers)
