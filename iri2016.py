#%%
import requests
import re
import datetime as dt
import pandas as pd
import numpy as np

i_url = 'https://omniweb.gsfc.nasa.gov/cgi/vitmo/vitmo_model.cgi'
url_headers = {
    'User-Agent':
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
     '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
}

iri_post = {
    'model': 'iri_2016',
    'year': '2000',
    'month': '1',
    'day': '1',
    'time_flag': '0',
    'hour': '1.5',
    'geo_flag': '0',
    'latitude': '50',
    'longitude': '40',
    'height': '100',
    'profile': '1',
    'start': '100',
    'stop': '2000',
    'step': '50',
    'sun_n': '',
    'ion_n': '',
    'radio_f': '',
    'radio_f81': '',
    'htec_max': '',
    'ne_top': '0',
    'imap': '0',
    'ffof2': '0',
    'hhmf2': '0',
    'ib0': '2',
    'probab': '0',
    'fauroralb': '1',
    'ffoE': '1',
    'dreg': '0',
    'tset': '0',
    'icomp': '0',
    'nmf2': '0',
    'hmf2': '0',
    'user_nme': '0',
    'user_hme': '0',
    'user_B0': '0',
    'format': '0',
    'vars': range(0, 61),
    'linestyle': 'solid',
    'charsize': '',
    'symbol': '2',
    'symsize': '',
    'yscale': 'Linear',
    'xscale': 'Linear',
    'imagex': '640',
    'imagey': '480'
}


# 获取数据
response = requests.post(i_url, data=iri_post, headers=url_headers)
pattern = re.compile('<pre>.*?Selected parameters are:(.*?)</pre><HR>', re.S)
results = re.findall(pattern, response.text)

# 替换文本中的','为空格，方便后面的pandas获取数据
results0 = re.sub(r',', ' ', results[0])

# 将获取的数据保存到临时文件iri_temp.dat中
with open('iri_temp.dat', mode='w+', newline='') as f:
    for result in results0:
        f.write(result)

# 从临时文件中获取数据
# 获取pandas的列名，及其相应的单位
iri_cof = pd.read_csv(
    'iri_temp.dat',
    sep='\s+',
    nrows=61,
    usecols=[0, 1, 2],
    names=[
        'index',
        'iri_cof',
        'unit',
    ],
    index_col='index')

iri_time_parser = lambda date: dt.datetime.strptime(date, '%Y %j')

d = pd.read_csv(
    'iri_temp.dat',
    parse_dates={'date': [0, 3]},
    date_parser=iri_time_parser,
    infer_datetime_format=True,
    keep_date_col=True,
    index_col='date',
    header=61,
    skip_blank_lines=True,
    sep='\s+',
    names=list(iri_cof['iri_cof']))
