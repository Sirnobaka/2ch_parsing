import re, io, os
import requests, json, html, time
from time import gmtime, strftime
from datetime import datetime, timedelta

file_data = '/home/andy/Learning/Prog/Python_files/Telegram/2Ch_parsing/Thread_v2.json'

def filter_gender(gen, required_gen):
    if required_gen == 'Not_found':
        return True
    elif gen == required_gen:
        return True
    else:
        return False

    
def filter_age(age, required_min, required_max):
    if required_min < 16 or required_max >= 50:
            return True
    try:
        
        if age >= required_min and age <= required_max:
            return True
        else:
            return False
    except:
        return False

    
def filter_city(cities, required_city):
    if required_city.lower() in cities:
        return True
    elif required_city.lower().strip() == 'все':
        return True
    else:
        return False
    
    
def filter_date(post_date, days_max):
    date_str = re.split('/| |:', post_date)
    date_str.pop(3)
    date_obj = datetime(int('20'+date_str[2]), int(date_str[1]), int(date_str[0]),\
                        hour=int(date_str[3]), minute=int(date_str[4]), second=int(date_str[4]))
    date_now = datetime.now()
    delta = date_now - date_obj
    if delta.days < days_max:
        return True
    else:
        return False


def filter_data(gender, age_min, age_max, city, days_max):
    answers = []
    with open(file_data, 'r', encoding='utf-8') as data_json:
        data = json.loads(data_json.read())
        for post in data:
            if all([filter_gender(post['gender'], gender),
                    filter_age(post['age'], age_min, age_max),
                    filter_city(post['city'], city),
                    filter_date(post['date'], days_max)]):
                answers.append(post['date'] + '\n' + 30*'-' + '\n' + post['comment'])
            else:
                continue
    return answers