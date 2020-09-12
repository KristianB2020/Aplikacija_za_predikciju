import requests
import pandas as pd
import numpy as np
import psycopg2
from uuid import uuid4 as gid, UUID
import json
import schedule
import itertools
import time
import datetime as dt
from datetime import datetime, date, time, timedelta

def spremi_prognozu_u_bazu():
    url ='https://api.weatherbit.io/v2.0/forecast/daily?city=vrsar&country=hr&key=6517f6215ddb471da8a1f03a55fe694a'
    json_data = requests.get(url).json()
    dataframe = pd.DataFrame(json_data['data'])
    #izbaci weather////////////////////////////////////////////
    dataframe2 = dataframe.drop('weather', 1)
    #kreiraj novi df iz liste samo s weather kolonama//////////
    dataframe3 = pd.DataFrame((dataframe['weather']).tolist())
    #kreiraj novi df samo s description kolonom///////////////////
    dataframe4 = dataframe3['description']
    #makni kolone koje ne trebamo !!!!!!!!!!
    dataframe2 = dataframe.drop(columns=['moonrise_ts','wind_cdir', 'high_temp', 'sunset_ts', 'ozone', 'moon_phase', 'ts', 'sunrise_ts', 'app_min_temp', 'pop', 'wind_cdir_full', 'slp', 'moon_phase_lunation', 'app_max_temp', 'snow', 'max_dhi', 'clouds_hi', 'low_temp', 'moonset_ts', 'datetime', 'clouds_mid', 'clouds_low'])
    dataframe2['forecast_date'] = dt.datetime.now().strftime('%Y-%m-%d')
    #pravilni redoslijed kolona
    dataframe2 = dataframe2[['valid_date', 'forecast_date', 'temp','max_temp','min_temp', 'vis', 'wind_dir', 'wind_spd', 'wind_gust_spd', 'rh', 'pres', 'uv', 'clouds', 'precip', 'snow_depth', 'dewpt']]
    #dodaj kolonu description kao dodatnu kolonu u df2//////
    dataframe2['Weather'] = dataframe4
    #nova kolona za broj dana između dana prognoze i dana za koji je prognoza napravljena
    dataframe2['preostalo_dana'] = ""

    #DATAFRAME U LISTU i INSERT PROGNOZE ZA 16 DANA OD DANAS
    lista2 = dataframe2.values.tolist()
    # ubaci vrijednosti u novu kolonu
    for a in lista2:
        a[17] = ((datetime.strptime(a[0], '%Y-%m-%d')) - (datetime.strptime(a[1], '%Y-%m-%d'))).days
        
    #spremi u DB
    conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
    for stavka in lista2:
        novi_id = str(gid())
        novi = {"id":novi_id, "datum":stavka[0], "datum_prognoze":stavka[1], "temp_prosjek":stavka[2], "temp_max":stavka[3], "temp_min":stavka[4], "vidljivost":stavka[5], "smjer_vjetra_stupnjevi":stavka[6], "brzina_vjetra":stavka[7], "nalet_vjetra_brzina":stavka[8], "relativna_vlaznost":stavka[9], "tlak_zraka":stavka[10], "uv_index":stavka[11], "oblaci_pokrice":stavka[12], "oborine_akumulirano":stavka[13], "dubina_snijega":stavka[14], "rosa_prosjek":stavka[15], "prognoza":stavka[16], "preostalo_dana":stavka[17]}
        print(novi)
        conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
        cur = conn.cursor()
        cur.execute("""INSERT INTO vremeprognoza(id, datum, datum_prognoze, temp_prosjek, temp_max, temp_min, vidljivost, smjer_vjetra_stupnjevi, brzina_vjetra, nalet_vjetra_brzina, relativna_vlaznost, tlak_zraka, uv_index, oblaci_pokrice, oborine_akumulirano, dubina_snijega, rosa_prosjek, prognoza, preostalo_dana) VALUES (%(id)s, %(datum)s, %(datum_prognoze)s, %(temp_prosjek)s, %(temp_max)s, %(temp_min)s, %(vidljivost)s, %(smjer_vjetra_stupnjevi)s, %(brzina_vjetra)s, %(nalet_vjetra_brzina)s, %(relativna_vlaznost)s, %(tlak_zraka)s, %(uv_index)s, %(oblaci_pokrice)s, %(oborine_akumulirano)s, %(dubina_snijega)s, %(rosa_prosjek)s, %(prognoza)s, %(preostalo_dana)s)""", novi)
        conn.commit()
    print("nova prognoza uspješno ubačena")

    #TIMER
    #schedule.every().day.at("06:00").do(spremi_prognozu_u_bazu)
    #schedule.every(10).seconds.do(spremi_prognozu_u_bazu)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

if __name__ == "__main__":
    spremi_prognozu_u_bazu()
