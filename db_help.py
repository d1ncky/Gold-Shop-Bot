import sqlite3
import random

db = sqlite3.connect('users.db')
sql = db.cursor()

db1 = sqlite3.connect('config.db')
sql1 = db1.cursor()

idgolds = 1

def check_user(ids):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    info = sql.execute(f'''select * from user where id = "{ids}"''')
    return info.fetchone()

def register_user(ids, name):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"insert into user values ('{ids}', '{0}', '{0}', '{0}', '{0}')")
    return db.commit()



def add_ref(ids):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"UPDATE user SET referals={check_user(ids)[2]+1} WHERE id={ids}")
    return db.commit()

def add_gold(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"UPDATE user SET gold={int(check_user(ids)[4])+int(suma)} WHERE id={ids}")
    return db.commit()

def del_gold(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"UPDATE user SET gold={int(check_user(ids)[4])-int(suma)} WHERE id={ids}")
    return db.commit()

def golds(suma):
    sql1.execute('''create table if not exists user (
    id TEXT, 
    golds REAL,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql1.execute(f"UPDATE user SET golds=? WHERE id=?", (float(suma[0]), idgolds))
    return db1.commit()

def goldsc():
    sql1.execute('''create table if not exists user (
    id TEXT, 
    golds REAL,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    info = sql1.execute(f'''select * from user where id = "{idgolds}"''')
    return info.fetchone()
def dbgolds():
    sql1.execute('''create table if not exists user (
    id TEXT, 
    golds REAL,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql1.execute(f"insert into user values ('{1}', '{0}', '{0}', '{0}', '{0}')")
    return db1.commit()

def del_balance(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"UPDATE user SET cash={int(check_user(ids)[3])-int(suma)} WHERE id={ids}")
    return db.commit()

def add_balance(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT, 
    name TEXT,
    referals BIGINT,
    cash BIGINT,
    gold BIGINT
    )''')
    sql.execute(f"UPDATE user SET cash={int(check_user(ids)[3])+int(suma)} WHERE id={ids}")
    return db.commit()