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

    @property
    def count_users(self):
        return users.count_users

    @property
    def count_alive(self):
        return users.count_alive

    @property
    def get_count_for_mailing(self):
        return users.get_count_for_mailing

    @property
    def get_batch_for_mailing(self):
        return users.get_batch_for_mailing


@dataclass
class Actions:
    @property
    def count_first_starts(self):
        return actions.count_first_starts

    @property
    def count_buys(self):
        return actions.count_buys

    @property
    def add_first_start(self):
        return actions.add_first_start

    @property
    def add_buy(self):
        return actions.add_buy


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

    @property
    def count_users(self):
        return paid_users.count_users


@dataclass
class Requests:
    users: Users = field(default_factory=Users)
    actions: Actions = field(default_factory=Actions)
    paid_users: PaidUsers = field(default_factory=PaidUsers)
