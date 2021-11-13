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
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('đ', 'd', s)
    return s

def create_key(s):
    res = no_accent_vietnamese(s)
    res = res.replace(" ", "_")
    res = res.replace(",", "")
    return res

