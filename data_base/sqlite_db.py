import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('2ch_base.db')
    cur = base.cursor()
    if base:
        print('Data base connection is OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(gender TEXT, age TEXT, city TEXT, time_period TEXT, username TEXT, mess_id TEXT PRIMARY KEY)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values())[0:6])
        base.commit()


#async def sql_read():
#    for ret in cur.execute('SELECT * FROM').fetchall():
#        await