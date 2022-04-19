from datetime import datetime

import pyotp
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

import base64


SYSTEM_EPOCH = 1600000000

CLIENT_OTP_KEY = '5um4f7zrdh5gkc3uhma2d42sw57a'

ENCODE_LOGIN_KEY = 'eSu4dxNENrBxg3VKunP4j6Bre2uZhnK3'

BYPASS_TOKEN = 'vjvjan2sd5s5uty'


def get_time_value(time_round):
    current_time = datetime.now()

    current_second = current_time.second

    current_time_no_second = int(current_time.timestamp()) + time_round - (current_second % time_round)

    return current_time_no_second


def get_otp(time_round=10, user_key=""):
    time_cur = get_time_value(time_round)
    otp_cur = generate_otp(time_cur, user_key)

    time_previous = time_cur - time_round
    otp_pre = generate_otp(time_previous, user_key)

    time_next = time_cur + time_round
    otp_next = generate_otp(time_next, user_key)
    return [otp_pre, otp_cur, otp_next]


def generate_otp(counter, user_key=''):
    otp = pyotp.HOTP(CLIENT_OTP_KEY + user_key)
    token = otp.at(counter)
    return token


def decode_key(key):
    bin_key = format(int(key), 'b')
    _time = int(bin_key[-32:], 2)
    bin_random = int(bin_key[:-32], 2)
    return _time, bin_random


class AESCipher:
    BLOCK_SIZE = 16

    def __init__(self, key=ENCODE_LOGIN_KEY):
        self.key = key.encode('utf8')

    def encrypt(self, message):
        iv = Random.new().read(self.BLOCK_SIZE)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = aes.encrypt(pad(message, self.BLOCK_SIZE))
        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, encrypted):
        encrypted = base64.b64decode(encrypted)
        iv = encrypted[:self.BLOCK_SIZE]
        message = encrypted[self.BLOCK_SIZE:]
        aes = AES.new(self.key, AES.MODE_CBC, iv, )
        decrypt = aes.decrypt(message)
        return unpad(decrypt, self.BLOCK_SIZE).decode()
