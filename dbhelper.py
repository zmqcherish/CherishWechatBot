import sqlite3

db_file = 'data.db'


def insert_msg(item):
    try:
        db = sqlite3.connect(db_file)
        with db:
            cursor = db.cursor()
            cursor.execute(''' INSERT INTO msg(msg_id, `type`, content, `from`, user_name, from_id, group_name, timestamp, `time`) VALUES(?,?,?,?,?,?,?,?,?)''', item)
    except sqlite3.IntegrityError:
        print('error')
    except Exception as ex:
        print(ex)
    finally:
        db.close()


def select_item_by_id(msg_id):
    try:
        db = sqlite3.connect(db_file)
        db.row_factory = sqlite3.Row
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT * from msg WHERE msg_id = '{}'".format(msg_id))
            return list(cursor.fetchall())
    except sqlite3.IntegrityError:
        print('error')
    finally:
        db.close()


def select_item_with_sql(sql):
    try:
        db = sqlite3.connect(db_file)
        db.row_factory = sqlite3.Row
        with db:
            cursor = db.cursor()
            cursor.execute(sql)
            return list(cursor.fetchall())
    except sqlite3.IntegrityError:
        print('error')
    finally:
        db.close()
