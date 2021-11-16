import re
import cx_Oracle
import config.database as db

def connect():
    # create a connection to the Oracle Database
    con = cx_Oracle.connect(db.DATABASE['USER'], db.DATABASE['PASSWORD'], db.DATABASE['NAME'])
    # create a new cursor
    cur = con.cursor()

    return con, cur

def no_accent_vietnamese(s):
    s = s.lower()
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    # s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    # s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    # s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    # s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    # s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    # s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    # s = re.sub(r'[Đ]', 'D', s)
    return s

def create_key(s):
    res = no_accent_vietnamese(s)
    res = res.replace(" ", "_")
    res = res.replace(",", "")
    return res

