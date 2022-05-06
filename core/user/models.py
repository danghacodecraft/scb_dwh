import binascii
import os
import json

from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BaseModel
from library.constant.gender import GENDER_TYPE_CHOICE, GENDER_TYPE_MALE
from library.functions import today


MENU_FILE = json.load(open('config/menu.json'))


class User(BaseModel):
    id = models.AutoField(db_column='id', primary_key=True)

    avatar_url = models.CharField(
        max_length=50, db_column='avatar_url',
        blank=True, null=True, verbose_name=_('Avatar Url'))

    mobile = models.CharField(
        max_length=50, db_column='mobile',
        blank=True, null=True, verbose_name=_('Mobile'))

    name = models.CharField(
        max_length=255, db_column='name', blank=True,
        null=True, verbose_name=_('Name'))

    username = models.CharField(
        max_length=50, db_column='username',
        verbose_name=_('Username')
    )

    password = models.CharField(
        max_length=200, db_column='password',
        blank=True, null=True, verbose_name=_('Password'))

    gender = models.IntegerField(
        db_column='gender', default=GENDER_TYPE_MALE,
        choices=GENDER_TYPE_CHOICE)

    birthday = models.DateTimeField(db_column='birthday', blank=True, null=True)

    address = models.CharField(
        max_length=200, db_column='address', blank=True,
        null=True, verbose_name=_('Address'))

    token = models.CharField(
        max_length=50, db_column='token',
        blank=True, null=True, verbose_name=_('token'))

    token_date = models.DateTimeField(db_column='token_date', blank=True, null=True)

    class Meta:
        db_table = 'dwh_user'
        verbose_name_plural = _('User')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
            self.token_date = today()
        return super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_token(self):
        import base64

        key = '{}:{}'.format(self.id, self.token)
        key = key.encode()

        try:
            return base64.b64encode(key).decode('utf-8')
        except Exception:  # noqa
            return None

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()


class DWHUser:
    def __init__(self, username=None, password=None, fullname=None, jobtitle=None, avatar=None, department=None, branch_code=None, employee_id=None, email=None, menu_id=None):
        self.id = username
        self.username = username
        self.password = password
        self.name = fullname

        self.token = None

        if avatar:
            avatar = avatar.replace('/var/www/EmployeeImage/', '')
            self.avatar = '/cdn/{}'.format(avatar)
        else:
            self.avatar = None
        self.position = 'Director'
        self.department = department
        self.jobtitle = jobtitle
        self.branch_code = branch_code

        self.employee_id = employee_id
        self.email = email

        if menu_id:

            self.menu = list()

            for _index in menu_id.split(';'):
                try:
                    self.menu.append(MENU_FILE[int(_index)-1])
                except IndexError:
                    pass

    def set_token(self, token):
        self.token = token


