from Models import *
from Domain import *
from pony.orm import *
from PreprocessingListe_final import *
import pandas as pd
import requests
import numpy as np
from uuid import uuid4 as gid, UUID
from openpyxl.workbook import Workbook
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import itertools  
from pandas import read_csv
from collections import Counter
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from category_encoders import TargetEncoder
from sklearn.metrics import auc, classification_report, roc_curve, roc_auc_score, confusion_matrix, average_precision_score, f1_score, plot_confusion_matrix, precision_recall_curve
from pandas.plotting import scatter_matrix

# # ucitaj dataset sa svim kolona 
df = ucitaj_podatke_i_spoji_za_analizu()

# ucitaj iz datoteke
# df = pd.read_excel('FINALREZERVACIJEEEE.xlsx', index_col=0)

plt.figure()
df.boxplot(column=['iznos_akontacije'])
plt.show()
plt.figure()
df.boxplot(column=['broj_dana'])
plt.show()
plt.figure()
df.boxplot(column=['jedinice'])
plt.show()

print("UKUPNI BROJ STORNA JE ", df['storno'].sum())
# izbaci nepotrebne kolone
df = df.drop(columns=['id','id_rezervacije', 'sif_hotela', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'tip_garancije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine1', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'nacin_rezervacije'])

# #podijeli datetime kolone "dan boravka" i "datum_kreiranja" na dan, mjesec...
df['dan_boravka']= pd.to_datetime(df['dan_boravka'])
df['mjesec'] = df['dan_boravka'].dt.month
df['dan_u_tjednu'] = df['dan_boravka'].dt.dayofweek
df['dan_u_godini'] = df['dan_boravka'].dt.dayofyear
df['tjedan'] = df['dan_boravka'].dt.week

df['datum_kreiranja']= pd.to_datetime(df['datum_kreiranja']) 
df['kreirano_dana_prije_dolaska'] = (df['dan_boravka'] - df['datum_kreiranja']).dt.days

df.drop('datum_kreiranja', axis=1, inplace=True)
df.drop('dan_boravka', axis=1, inplace=True)

# izračunaj postotak storna prema vrsti sobe
df['post_storna'] = 0 

# GRUPIRANJE - broj jedinica po vrsti sobe za sve rezervacije
listaSve = (df.groupby('vrsta_sobe', as_index=False)['jedinice'].sum()).to_dict('records')
print("OVO JE DUŽINA OD SVE", len(listaSve))

# GRUPIRANJE - broj jedinica po vrsti sobe za otkazane rezervacije
x = df[df['storno'] == 1]
listaStorno = (x.groupby('vrsta_sobe', as_index=False)['jedinice'].sum()).to_dict('records')

for stavka in listaSve:
    stavka['storno'] = 0

# pridodaj postotak otkazivanja odgovarajućoj vrsti sobe
for stavka in listaSve:
    listaIndexa = [idx for idx, element in enumerate(listaStorno) if element['vrsta_sobe'] == stavka['vrsta_sobe']]
    for index in listaIndexa:
        stavka['storno'] = listaStorno[index]['jedinice']

for stavka in listaSve:
    stavka['post_storna'] = round(stavka['storno'] / stavka['jedinice'] * 100, 2)

# ubaci postotke u dataset
listaPostotaka = []
for soba in df['vrsta_sobe']:
    listaIndexa = [idx for idx, element in enumerate(listaSve) if element['vrsta_sobe'] == soba]
    for index in listaIndexa:
        listaPostotaka.append(listaSve[index]['post_storna'])
df['post_storna'] = listaPostotaka

# NUll vrijednosti zamijeni nulom u kolonama
df['iznos_akontacije'].fillna(value=0, inplace=True)

# stavi storno na kraj
dfStorno = df['storno']
df = df.drop('storno', axis='columns')
df['storno'] = dfStorno

# int to float za kolone
int_kolone = ['kreirano_dana_prije_dolaska', 'broj_dana', 'jedinice', 'dat_storna_do_dat_dolaska', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'storno']
for kolona in int_kolone:
    df[kolona] = df[kolona].astype(float)


# plotanje po kolonama u datasetu
plt.figure()
df[['jedinice']].plot(kind='hist',rwidth=0.8)
plt.show()


# DISTRIBUCIJA VRIJEDNOSTI OUTPUTA/STORNA
print("Distribucija storna")
print(df['storno'].value_counts())
print("NESTORNIRANO", round(df['storno'].value_counts()[0]/len(df)*100,2), '% od cijelog dataseta')
print("STORNIRANO", round(df['storno'].value_counts()[1]/len(df)*100,2), '% od cijelog dataseta')

plt.figure()
sns.countplot(df['storno'])
plt.title("Broj Outputa", fontsize=18)
plt.xlabel("Da li je storno?", fontsize=15)
plt.ylabel("Broj", fontsize=15)
plt.show()

# INFO - IZNOS AKONTACIJE
print('Top 90% iznosa akontacije su do:', round(df.iznos_akontacije.quantile(.90),2))
print('Top 1% iznosi akontacije su:', round(df.iznos_akontacije.quantile(.99),2))
print('Najveći iznos akontacije:', round(df.iznos_akontacije.quantile(1),2))
print('90% storna je za rezervacije sa akontacijom ispod iznosa od :', round(df.iznos_akontacije[df.storno==1].quantile(.90),2))

# PLOT - STORNO - iznos_akontacije
plt.figure(figsize=(16,5))
sns.boxplot(x=df.iznos_akontacije[df.storno == 1])
plt.title('Distribucija storna uz iznose akontacija',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.iznos_akontacije[df.storno == 0])
plt.title('Distribucija ne-storna uz iznose akontacija', fontsize=17)
plt.show()

# INFO - IZNOS BRUTO
print('Top 90% iznosa akontacije su do:', round(df.iznos_bruto.quantile(.90),2))
print('Top 1% bruto iznosi:', round(df.iznos_bruto.quantile(.99),2))
print('Najveći bruto iznos:', round(df.iznos_bruto.quantile(1),2))
print('98% storna je za rezervacije sa bruto iznosom ispod :', round(df.iznos_bruto[df.storno==1].quantile(.98),2))

# PLOT - STORNO - iznos_bruto
plt.figure(figsize=(16,5))
sns.boxplot(x=df.iznos_bruto[df.storno == 1])
plt.title('Distribucija storna uz bruto iznose ', fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.iznos_bruto[df.storno == 0])
plt.title('Distribucija ne-storna uz bruto iznose', fontsize=17)
plt.show()

# INFO - TLAK ZRAKA
print('Top 95%:', round(df.tlak_zraka1.quantile(.95),2))
print('Top 1%:', round(df.tlak_zraka1.quantile(.99),2))
print('Najveći tlak zraka', round(df.tlak_zraka1.quantile(1),2))
print('95% storna je ispod vrijednosti tlaka zraka od :', round(df.tlak_zraka1[df.storno==1].quantile(.95),2))

# PLOT - STORNO - tlak zraka
plt.figure(figsize=(16,5))
sns.boxplot(x=df.tlak_zraka1[df.storno == 1])
plt.title('Distribucija storna uz vrijednosti tlaka_zraka',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.tlak_zraka1[df.storno == 0])
plt.title('Distribucija ne-storna uz vrijednosti tlaka_zraka',fontsize=17)
plt.show()

# INFO - TEMP MAX
print('Top 95%:', round(df.temp_max1.quantile(.95),2))
print('Top 1%:', round(df.temp_max1.quantile(.99),2))
print('Najveća maksimalna temperatura', round(df.temp_max1.quantile(1),2))
print('95% storna je kod maksimalnih temp ispod:', round(df.temp_max1[df.storno==1].quantile(.95),2))

# PLOT - STORNO - temp_max
plt.figure(figsize=(16,5))
sns.boxplot(x=df.temp_max1[df.storno == 1])
plt.title('Distribucija storna uz vrijednosti maksimalne temperature',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.temp_max1[df.storno == 0])
plt.title('Distribucija ne-storna uz vrijednosti maksimalne temperature',fontsize=17)
plt.show()

# INFO - TEMP MIN
print('Top 95%:', round(df.temp_min1.quantile(.95),2))
print('Top 2%:', round(df.temp_min1.quantile(.98),2))
print('Najniža zabilježena temperatura', round(df.temp_min1.quantile(0),2))
print('95% storna je kod temp ispod:', round(df.temp_min1[df.storno==1].quantile(.95),2))

# PLOT - STORNO - temp_min
plt.figure(figsize=(16,5))
sns.boxplot(x=df.temp_min1[df.storno == 1])
plt.title('Distribucija storna uz vrijednosti minimalne temperature',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.temp_min1[df.storno == 0])
plt.title('Distribucija ne-storna uz vrijednosti minimalne temperature',fontsize=17)
plt.show()

# INFO - OBORINE
print('Top 95%:', round(df.oborine_mogucnost1.quantile(.95),2))
print('Top 1%:', round(df.oborine_mogucnost1.quantile(.99),2))
print('Najveća najavljenja količina oborina', round(df.oborine_mogucnost1.quantile(1),2))
print('98% storna je kod mogućnosti oborina ispod (mm/m2):', round(df.oborine_mogucnost1[df.storno==1].quantile(.98),2))

# PLOT - STORNO - oborine_mogucnost
plt.figure(figsize=(16,5))
sns.boxplot(x=df.oborine_mogucnost1[df.storno == 1])
plt.title('Distribucija storna uz vrijednosti za mogućnosti oborina',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.oborine_mogucnost1[df.storno == 0])
plt.title('Distribucija ne-storna uz vrijednosti za mogućnosti oborina',fontsize=17)
plt.show()

# INFO - VJETAR
print('Top 95%:', round(df.brzina_vjetra1.quantile(.95),2))
print('Top 2%:', round(df.brzina_vjetra1.quantile(.98),2))
print('Najveća brzina vjetra', round(df.brzina_vjetra1.quantile(1),2))
print('98% storna je kod brzine vjetra:', round(df.brzina_vjetra1[df.storno==1].quantile(.98),2))

# PLOT - STORNO - brzina_vjetra
plt.figure(figsize=(16,5))
sns.boxplot(x=df.brzina_vjetra1[df.storno == 1])
plt.title('Distribucija storna uz vrijednosti brzine vjetra',fontsize=17)
plt.show()
# PLOT - NE-STORNO 
plt.figure(figsize=(16,5))
sns.boxplot(x=df.brzina_vjetra1[df.storno == 0])
plt.title('Distribucija ne-storna uz vrijednosti brzine vjetra',fontsize=17)
plt.show()


# MATRICA KORELACIJA
corr_matrix = df.corr()
print(corr_matrix)
matrix = np.triu(corr_matrix.corr())
sns.heatmap(corr_matrix, fmt='.1g', vmin=-1, vmax=1, center= 0, square=True, mask=matrix, cmap="YlGnBu")
# CMAP VRIJEDNOSTI "YlGnBu"  , "Greens", "Blues"
# box and whisker plots
df.plot(kind='box', subplots=True, layout=(20,3), sharex=False, sharey=False, figsize=(10,15))
plt.show()

# PLOTANJE GRAFOVA VEZANIH ISKLJUČIVO UZ SET PODATAKA GDJE JE STORNO = 1 -------------------------------------------------------------------------
x = df[df['storno'] == 1]
plt.figure()
plt.scatter(x=x['mjesec'], y=x['tlak_zraka1'])
plt.title('storno kod tlaka zraka po mjesecima')
plt.xlabel('Mjesec')
plt.ylabel('Tlak_zraka')
plt.show()

plt.figure()
plt.scatter(x=x['mjesec'], y=x['oborine_mogucnost1'])
plt.title('storno prema mogucnosti oborina po mjesecima')
plt.xlabel('Mjesec')
plt.ylabel('Mogucnost oborine / cm')
plt.show()

plt.figure()
plt.scatter(x=x['mjesec'], y=x['oblaci_pokrice1'])
plt.title('storno prema pokricu oblaka po mjesecima')
plt.xlabel('Mjesec')
plt.ylabel('Oblaci pokrice / %')
plt.show()

plt.figure()
plt.scatter(x=x['mjesec'], y=x['brzina_vjetra1'], c='green')
plt.title('storno prema brzini vjetra po mjesecima')
plt.xlabel('Mjesec')
plt.ylabel('Brzina vjetra ')
plt.show()

plt.figure()
plt.scatter(x=x['mjesec'], y=x['temp_prosjek1'], c='lightblue')
plt.title('storno prema temperaturi po mjesecima')
plt.xlabel('Mjesec')
plt.ylabel('Temperatura ')
plt.show()

plt.figure()
plt.scatter(x=x['tlak_zraka1'], y=x['brzina_vjetra1'], c='coral')
plt.title('storno prema brzini vjetra/tlak zraka')
plt.xlabel('Tlak zraka')
plt.ylabel('Brzina vjetra ')
plt.show()

plt.figure()
plt.scatter(x=x['temp_prosjek1'], y=x['tlak_zraka1'], c='darkmagenta')
plt.title('storno Temperatura/Tlak zraka')
plt.xlabel('Temperatura')
plt.ylabel('Tlak zraka')
plt.show()

plt.figure()
plt.scatter(x=x['oborine_mogucnost1'], y=x['tlak_zraka1'], c='forestgreen')
plt.title('storno Oborine/Tlak zraka')
plt.xlabel('Tlak zraka')
plt.ylabel('Oborine cm')
plt.show()



