# RFECV za klasifikaciju atributa prema važnosti
import numpy as np
from sklearn.feature_selection import RFECV
from Models import *
from Domain import *
from PreprocessingListe_final import *
import pandas as pd
import datetime as dt
from category_encoders import TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from xgboost import XGBClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold, RepeatedStratifiedKFold
import matplotlib.pyplot as plt

# UČITAJ PODATKE
# df = ucitaj_podatke_i_spoji()
df = pd.read_excel('FINALREZERVACIJEEEE.xlsx', index_col=0)

# FILTRIRANJE SUVIŠNIH REDAKA
df = df[df['broj_dana'] < 50]
df = df[df['jedinice'] < 17]
x = df.query('status_rezervacije == "F" or status_rezervacije == "N"  or status_rezervacije == "O" or status_rezervacije == "EF" or status_rezervacije == "EO" or status_rezervacije == "D"')

print("UKUPNI BROJ STORNA JE ", df['storno'].sum())

# plt.figure()
# corr_matrix = x.corr()
# print(corr_matrix)
# matrix = np.triu(corr_matrix.corr())
# sns.heatmap(corr_matrix, fmt='.1g', vmin=-1, vmax=1, center= 0, square=True, mask=matrix, cmap="YlGnBu")
# # CMAP VRIJEDNOSTI "YlGnBu"  , "Greens", "Blues"
# # box and whisker plots
# df.plot(kind='box', subplots=True, layout=(20,4), sharex=False, sharey=False, figsize=(15,20))
# plt.show()

# MICANJE KORELIRANIH KOLONA
# correlated_features = set()
# correlation_matrix = data.drop('Survived', axis=1).corr()

# for i in range(len(correlation_matrix.columns)):
#     for j in range(i):
#         if abs(correlation_matrix.iloc[i, j]) > 0.8:
#             colname = correlation_matrix.columns[i]
#             correlated_features.add(colname)


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

# IZRAČUNAJ POSTOTAK STORNA PREMA VRSTI SOBE 
df['post_storna'] = 0 
#  broj jedinica po vrsti sobe za sve rezervacije
listaSve = (df.groupby('vrsta_sobe', as_index=False)['jedinice'].sum()).to_dict('records')
print("OVO JE DUŽINA OD SVE", len(listaSve))
#  broj jedinica po vrsti sobe za otkazane rezervacije
x = df[df['storno'] == 1]
listaStorno = (x.groupby('vrsta_sobe', as_index=False)['jedinice'].sum()).to_dict('records')

for stavka in listaSve:
    stavka['storno'] = 0

#  pridodaj postotak otkazivanja odgovarajućoj vrsti sobe
for stavka in listaSve:
    listaIndexa = [idx for idx, element in enumerate(listaStorno) if element['vrsta_sobe'] == stavka['vrsta_sobe']]
    for index in listaIndexa:
        stavka['storno'] = listaStorno[index]['jedinice']

for stavka in listaSve:
    stavka['post_storna'] = round(stavka['storno'] / stavka['jedinice'] * 100, 2)

dfPostotaka = pd.DataFrame(listaSve)
dfPostotaka.to_excel("Postoci.xlsx")

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

	
d_oborine_mogucnost = np.percentile(df['oborine_mogucnost1'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost1'], 99) 
df = df[df.oborine_mogucnost1.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_oborine_mogucnost = np.percentile(df['oborine_mogucnost3'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost3'], 99) 
df = df[df.oborine_mogucnost3.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_oborine_mogucnost = np.percentile(df['oborine_mogucnost7'], 0) 
g_oborine_mogucnost = np.percentile(df['oborine_mogucnost7'], 99) 
df = df[df.oborine_mogucnost7.between(d_oborine_mogucnost, g_oborine_mogucnost)]

d_temp_min = np.percentile(df['temp_min1'], 0) 
g_temp_min = np.percentile(df['temp_min1'], 99) 
df = df[df.temp_min1.between(d_temp_min, g_temp_min)]

d_iznos_akontacije = np.percentile(df['iznos_akontacije'], 0) 
g_iznos_akontacije = np.percentile(df['iznos_akontacije'], 98) 
df = df[df.iznos_akontacije.between(d_iznos_akontacije, g_iznos_akontacije)]


df.reset_index(drop=True, inplace=True)

# PODJELA NA INPUT I OUTPUT & PIPELINE ZA IMPUTER, SCALER, TARGET ENCODING 
y = df.storno
X = df.drop(columns= ['storno', 'dat_storna_do_dat_dolaska' ], axis='columns')

print(X.info())

X = X.drop(columns=['id','id_rezervacije', 'sif_hotela', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'datum_do_potvrde_opcije', 'datum_storna', 'vrsta_sobe_naplata',  'godina_rezervacije', 'obaveza_akontacije', 'sif_drzave'])

print(X.info())

# DEFINIRAJ LISTE ZA NUMERIČKE I ZA KATEGORIČKE VARIJABLE
numericke = ['broj_osoba', 'broj_djece', 'iznos_akontacije', 'nocenja', 'broj_soba', 'broj_dana', 'jedinice', 'iznos_bruto', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 'oborine_mogucnost1', 'p_tlak_zraka_31', 'p_tlak_zraka_73', 'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31', 
            'p_temp_max_73', 'p_oborine_mogucnost31', 'p_oborine_mogucnost73', 'p_oblaci_pokrice_31', 'p_oblaci_pokrice_73', 'p_brzina_vjetra_31', 'p_brzina_vjetra_73', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'kreirano_dana_prije_dolaska', 'post_storna', 'temp_prosjek1', 'temp_prosjek3', 'temp_max3',
            'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7', 'index_vrucine1', 'index_vrucine3', 'index_vrucine7',]
kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'prognoza3', 'prognoza1', 'prognoza7', 'sif_usluge', 'tip_ro', 'tip_garancije', 'lead_time_dani']

print(len(numericke))
print(len(kategoricke))
# SIMPLE IMPUTER za null i vrijednosti koje nedostaju
num_pipeline = Pipeline([('impute', SimpleImputer(strategy='mean'))])
kat_pipeline = Pipeline([('impute', SimpleImputer(strategy='most_frequent'))])

final_pipeline = ColumnTransformer([('continuous', num_pipeline, numericke), ('cat', kat_pipeline, kategoricke)], remainder='passthrough')
X_imputed = final_pipeline.fit_transform(X,y)
print(type(X_imputed))

# TARGET ENCODING KATEGORIČKIH VARIJABLI
te = TargetEncoder()
X_kodirano = te.fit_transform(X_imputed, y)

skalar = MinMaxScaler()
X_fit = skalar.fit_transform(X_kodirano,y)

rfc = XGBClassifier()
rfecv = RFECV(estimator=rfc, step=1, cv=StratifiedKFold(5), scoring='f1', min_features_to_select=1, verbose=1)
rfecv.fit(X_fit, y)

print('Optimalan broj značajki je: {}'.format(rfecv.n_features_))
print(np.where(rfecv.support_ == False)[0])
X.drop(X.columns[np.where(rfecv.support_ == False)[0]], axis=1, inplace=True)


plt.figure(figsize=(16, 9))
plt.title('Recursive Feature Elimination sa unakrsnom validacijom', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Broj odabranih značajki', fontsize=14, labelpad=20)
plt.ylabel('% pravilne klasifikacije', fontsize=14, labelpad=20)
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#303F9F', linewidth=3)
plt.show()


# PLOT PO VAŽNOSTI
dset = pd.DataFrame()
dset['atribut'] = X.columns
dset['vaznost'] = rfecv.estimator_.feature_importances_
dset = dset.sort_values(by='vaznost', ascending=False)
plt.figure(figsize=(16, 14))
plt.barh(y=dset['atribut'], width=dset['vaznost'], color='#1976D2')
plt.title('RFECV - Vaznost atributa', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Vaznost', fontsize=14, labelpad=20)
plt.show()




