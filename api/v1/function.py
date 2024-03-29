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
    res = no_accent_vietnamese(s.strip())
    res = res.replace(" ", "_")
    res = res.replace(",", "")
    return res

def parseString(data):
    if data is None:
        return ""

    t = type(data)
    if t != str:
        return data

    data = data.replace("  ", " ").strip()
    return data

def parseUser(data):
    data = parseString(data)
    data = data.replace("@SCB.COM.VN", "")
    return data


def parseCoordinate(data, default=0):
    if data is None:
        return default

    t = type(data)
    if t == float:
        return data
    elif t == int:
        return data
    elif t == str:
        data = data.replace("  ", " ").strip()
        return float(data)

    data = data.replace(",", "").replace("%", "").strip()

    val = default
    try:
        val = float(data)
    except:
        val = default
    return val


def parseFloat(data, precision=2, r=True):
    if data is None:
        return 0

    t = type(data)
    if t == float:
        if r:
            return round(data, precision)
        return data
    elif t == int:
        return data
    elif t == str:
        data = data.replace("  ", " ").strip()
        return float(data)

    data = data.replace(",", "").replace("%", "").strip()

    val = 0
    try:
        val = float(data)
        if r:
            val = round(data, precision)
    except:
        val = 0
    return val

