import os, io
import asyncio
import time
import requests, json, html, re
from datetime import datetime, timedelta
from data_base.parser_functions import *
import aioschedule
from create_bot import bot

def clean_string(text):
    text = text.replace('<br>', ' \n')
    text = html.unescape(text)
    text = re.sub('<[^>]+>', '', text)
    return text


def get_last_num(file_name):
    last_one = 0
    with open(file_name, 'r', encoding='utf-8') as file:
        last_one = json.loads(file.read())[-1]
    return last_one['num']


def delete_symbols(fname, n):
    with open(fname, 'rb+') as filehandle:
        for _ in range(n):
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
            filehandle.tell()
            
def write_string(fname, string):
    with open(fname, 'a+', encoding='utf-8') as outfile:
        outfile.seek(0, io.SEEK_END) # searching for end of file
        outfile.write(string)


def select_age(post):
    age = -1
    #res_age = re.search(r'\D\d{2}\D', post) #r'\s\d{2}\s'
    res_age = re.search(r'\d{2}\D', post) #r'\s\d{2}\s'
    if res_age:
        #print(f'### Age = {res_age.group(0)}')
        age = int(re.sub('\D', '', res_age.group(0)))
        if age < 51:
            return age
    else:
        return -1



def select_city_update(post):
    city = 'unknown'
    cities_mult = set()
    for c in cities.keys():
        for name in cities[c]:
            if name in post.lower():
                if (name in short_names):
                    if string_found(name, post.lower()):
                        city = c
                        cities_mult.add(c)
                        res_city = re.search(r'\b' + re.escape(name) + r'\b', post.lower())
                else:
                    city = c
                    cities_mult.add(c)
    return list(cities_mult)


async def update_json_web(url, file_out):
    channel_id = -1001670729864
    print(f'### Current time -> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    # read thread from url
    thread = requests.get(url)
    thread_json = thread.json()
    print(f'file: {file_out}')
    last_number = get_last_num(file_out)
    print('last post obtained =', last_number)
    # 
    if os.path.isfile(file_out):
        # File exists
        # Delete bracket symbol and ']' and '\t' from the end of file
        delete_symbols(file_out, 2)
        with open(file_out, 'a+', encoding='utf-8') as outfile:
            outfile.seek(0, io.SEEK_END)  # searching for end of file
            outfile.write(',\n')  # write colon ','
            n_added = 0
            for post in thread_json['threads'][0]['posts']:
                if post['num'] <= last_number:
                    continue
                if '<a href="/soc/res/' in post['comment']:
                    continue
                else:
                    post_text = clean_string(post['comment'])
                    entry = {
                        'date': post['date'],
                        'comment': post_text,
                        'num': post['num'], 
                        'gender': select_gender(post_text),
                        'age': select_age(post_text),
                        'city': select_city_update(post_text)
                    }
                    json.dump(entry, outfile, indent=4, ensure_ascii=True)
                    n_added += 1
                    outfile.write(',\n')
                    # send message to group
                    #await bot.send_message(channel_id, post_text)
            print('added =', n_added)
            outfile.write('\n]')
        delete_symbols(file_out, 4) # delete excessive colon ','
        write_string(file_out, '\n]') # write closing bracket ']'
        # print data obtained
    else:
        print('There is no', file_out)
    # Sleep for n seconds
    #await asyncio.sleep(n)


async def update_json_every(n):
    aioschedule.every(n).seconds.do(update_json_web, "https://2ch.hk/soc/res/5959967.json", 'Thread_v2.json')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)