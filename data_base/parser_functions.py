import re


Male_list = ['кун', 'кун-', 'парень', 'мужчина', 'м', 'мальчик', 'нижний', 'п', 'мужик', 'т-кун', 'мужской',
            'хиккан', 'господин', 'мейл', 'парниша', 'муж', 'm', 'парнишка', 'male', 'куница', 'зумер', 'паренёк',
             'xyn', 'дедушка', 'кунчик', 'cun', 'дядя', 'kun', 'думер', 'укроанон', 'мальчишка', 'чувак',
             'кунский', 'кунь', 'кунец', 'поц']
Female_list = ['тян', 'тян-', 'тяночка', 'тянка', 'девушка', 'женщина', 'ж', 'д', 'девочка', 'мадам',
              'госпожа', 'нижняя', 'баба', 'женский', 'ттян', 'т-тян', 'трап', 'тнус', 'зумерша', 'зумерка',
               'тня', 'пухлотян', 'убертян', 'жинка', 'female', 'тянус', 'герл', 'дефка', 'девка', 'тянучка', 
               'милфа', 'трапик']


cities = {
    'интернет':  ['интернет', 'интернеты', 'инет'],
    'петербург': ['дс2', 'дс-2', 'дс 2', 'спб', 'питер', 'ленинград', 'санкт-петербург'],
    'москва': ['москв', 'дс', 'дс1', 'дс-1', 'мск'],
    'новосибирск': ['новосибирск', 'новосиб'],
    'екатеринбург': ['екатеринбург', 'екб'],
    'казань': ['казань'],
    'нижиний новгород': ['нижиний новгород', 'нижний', 'нн'],
    'челябинск': ['челябинск', 'челяба'],
    'красноярск': ['красноярск'],
    'самара': ['самара'],
    'уфа': ['уфа'],
    'ростов': ['ростов'],
    'омск': ['омск'],
    'краснодар': ['краснодар'],
    'волгоград': ['волгоград'],
    'пермь': ['пермь'],
    'волгоград': ['волгоград'],
    'саратов': ['саратов'],
    'тюмень': ['тюмень'],
    'тольятти': ['тольятти'],
    'барнаул': ['барнаул'],
    'хабаровск': ['хабаровск'],
    'ижевск': ['ижевск'],
    'махачкала': ['махачкала'],
    'хабаровск': ['хабаровск'],
    'иркутск': ['иркутск'],
    'владивосток': ['владивосток'],
    'ярославль': ['ярославль'],
    'кемерово': ['кемерово'],
    'томск': ['томск'],
    'набережные челны': ['челны'],
    'ставрополь': ['ставрополь'],
    'севастополь': ['севастополь'],
    'оренбург': ['оренбург'],
    'новокузнецк': ['новокузнецк'],
    'рязань': ['рязань'],
    'пенза': ['пенза'],
    'чебоксары': ['чебоксары'],
    'липецк': ['липецк'],
    'калининград': ['калининград'],
    'астрахань': ['астрахань'],
    'тула': ['тула'],
    'воронеж': ['воронеж'],
    'киров': ['киров'],
    'сочи': ['сочи'],
    'курск': ['курск'],
    'улан-удэ': ['улан-удэ'],
    'тверь': ['тверь'],
    'мурманск': ['мурманск'],
    'киев': ['киев'],
    'харьков': ['харьков'],
    'одесса': ['одесса'],
    'днепр': ['днепр'],
    'донецк': ['донецк', 'донбасс', 'днр'],
    'запорожье': ['запорожье'],
    'львов': ['львов', 'львив', 'львiв'],
    'кривой рог': ['кривой рог'],
    'николаев': ['николаев'],
    'мариуполь': ['мариуполь'],
    'луганск': ['луганск', 'лнр'],
    'винница': ['винница'],
    'макеевка': ['макеевка'],
    'херсон': ['херсон'],
    'полтава': ['полтатва'],
    'чернигов': ['чернигов', 'чернiгiв'],
    'черкассы': ['черкассы'],
    'житомир': ['житомир'],
    'сумы': ['сумы'],
    'минск': ['минск'],
    'беларусь': ['беларусь', 'белоруссия'],
    'украина': ['украина'],
    'тбилиси': ['тбилиси'],
    'грузия': ['грузия', 'тбилси'],
    'армения': ['армения', 'ереван'],
    'ереван': ['ереван'],
    'казахстан': ['казахстан'],
    'алматы': ['алматы', 'алма-ата'],
    'астана': ['астана'],
    'шымкент': ['шымкент'],
    'актобе': ['актобе'],
    'караганда': ['караганда'],
    'европа': ['евросоюз', 'ес', 'европа'],
    'крым': ['крым'],
    'кавказ': ['кавказ'],
    'сибирь': ['сибирь'],
    'россия': ['россия']
}

short_names = frozenset(('дс', 'нн', 'екб', 'нн', 'нижний', 'уфа', 'ес', 'мск'))

def string_found(substring, string):
    if re.search(r'\b' + re.escape(substring) + r'\b', string):
        return True
    return False



def select_gender(post):
    isMale = False
    isFemale = False
    male_pos = -1
    female_pos = -1
    if any(list(map(lambda x: string_found(x, post.lower()), Male_list))):
        isMale = True
    if any(list(map(lambda x: string_found(x, post.lower()), Female_list))):
        isFemale = True
    if (isMale and isFemale):
        for word in Male_list:
            res_male = re.search(r'\b' + re.escape(word) + r'\b', post.lower())
            if (res_male):
                male_pos = res_male.start()
        for word in Female_list:
            res_female = re.search(r'\b' + re.escape(word) + r'\b', post.lower())
            if (res_female):
                female_pos = res_female.start()
    if (isMale and isFemale):
        if male_pos < female_pos:
            return 'Male'
        else:
            return 'Female'
    elif isMale:
        return 'Male'
    elif isFemale:
        return 'Female'
    else:
        if re.search(r'[мждпт]{1}\d{2}', post.lower()):
            str_gender_age = re.search(r'[мждпт]{1}\d{2}', post.lower()).group(0)
            gender, age = str_gender_age[0], str_gender_age[1::]
            if (gender in ['м', 'п']):
                return 'Male'
            else:
                return 'Female'
        elif re.search(r'\d{2}[мждпт]{1}', post.lower()):
            str_gender_age = re.search(r'\d{2}[мждпт]{1}', post.lower()).group(0)
            gender, age = str_gender_age[-1], str_gender_age[0:2]
            if (gender in ['м', 'п']):
                return 'Male'
            else:
                return 'Female'
        else:
            return 'Not_found'



def select_city(post):
    city = 'unknown'
    if post.lower().strip() == 'все':
        return 'все'
    for c in cities.keys():
        for name in cities[c]:
            if name in post.lower():
                if (name in short_names):
                    if string_found(name, post.lower()):
                        city = c
                else:
                    city = c
    return city



def strip_age(str_age):
    str_list = re.split('-|:| ', str_age)
    str_new = [int(i) for i in str_list if i.isnumeric()]
    return str_new