from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import datetime
from dateutil.relativedelta import relativedelta
import urllib
from numpy.core.records import record
import requests
import pandas as pd
import xmltodict
import json
import csv

mmaf = []
mmsi = []
full = []
df = []
df_reset = []
DATETIME_n=[]
MMAF_CODE_n=[]
MMAF_NM_n=[]
MMSI_CODE_n=[]
MMSI_NM_n=[]
WIND_DIRECT_n=[]
WIND_SPEED_n=[]
AIR_TEMPERATURE_n=[]
HUMIDITY_n=[]
AIR_PRESSURE_n=[] 

f = open('data.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

for a in rdr:
    mmaf.append(a[0])
    mmsi.append(a[1])
f.close()

#before_day = (datetime.date.today() - datetime.timedelta(days=10)).strftime('%Y%m%d')
before_day = (datetime.date.today() - relativedelta(months=1)).strftime('%Y%m%d')
today = datetime.date.today().strftime('%Y%m%d')
key='DB70E5C4-078F-462C-BC5B-C147CDF55B33'


for one,two in zip(mmaf,mmsi):
        url = f'http://marineweather.nmpnt.go.kr:8001/openWeatherDate.do?serviceKey={key}&'
        queryParams = urlencode({ quote_plus('resultType') : 'xml',
                                quote_plus('date') : today,
                                quote_plus('mmaf') : one,
                                quote_plus('mmsi') : two})
        url2 = url + queryParams
        response = urlopen(url2)
        results = response.read().decode("utf-8")
        results_to_json = xmltodict.parse(results)
        data = json.loads(json.dumps(results_to_json))
        print(type(data))   # dic
        print(data)
        corona=data['result']['recordset']['record']
        #추가하고 싶은 리스트 생성
        # DATETIME_n=[]
        # MMAF_CODE_n=[]
        # MMAF_NM_n=[]
        # MMSI_CODE_n=[]
        # MMSI_NM_n=[]
        # WIND_DIRECT_n=[]
        # WIND_SPEED_n=[]
        # AIR_TEMPERATURE_n=[]
        # HUMIDITY_n=[]
        # AIR_PRESSURE_n=[]   
        #HORIZON_VISIBL_n=[]
        #LATITUDE_n=[]
        #LONGITUDE_n=[]

        for i in corona:
            DATETIME_n.append(i['DATETIME'])
            MMAF_CODE_n.append(i['MMAF_CODE'])
            MMAF_NM_n.append(i['MMAF_NM'])
            MMSI_CODE_n.append(i['MMSI_CODE'])
            MMSI_NM_n.append(i['MMSI_NM'])
            WIND_DIRECT_n.append(i['WIND_DIRECT'])
            WIND_SPEED_n.append(i['WIND_SPEED'])
            AIR_TEMPERATURE_n.append(i['AIR_TEMPERATURE'])
            HUMIDITY_n.append(i['HUMIDITY'])
            AIR_PRESSURE_n.append(i['AIR_PRESSURE'])
            #HORIZON_VISIBL_n.append(i['HORIZON_VISIBL'])
            #LATITUDE_n.append(i['LATITUDE'])
            #LONGITUDE_n.append(i['LONGITUDE'])

        df=pd.DataFrame([DATETIME_n,MMAF_CODE_n,MMAF_NM_n,MMSI_CODE_n,MMSI_NM_n,WIND_DIRECT_n,WIND_SPEED_n,AIR_TEMPERATURE_n,HUMIDITY_n,AIR_PRESSURE_n]).T
        df.columns=['DATETIME','MMAF_CODE','MMAF_NM','MMSI_CODE','MMSI_NM','WIND_DIRECT','WIND_SPEED','AIR_TEMPERATURE','HUMIDITY','AIR_PRESSURE']
        print(df)
#df=df.sort_values(by='기관코드', ascending=True)
df_reset=df.set_index('MMSI_CODE')
print(df_reset)
        # csv 파일 생성
df_reset.to_csv('righttime.csv')
    # 메모장
    #df.to_csv('sample.txt') 

    # json 파일 생성
    #df.to_json('sample.json')