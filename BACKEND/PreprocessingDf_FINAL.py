
import pandas as pd 
import numpy as np
from PreprocessingListe_final import *


def procesirani_df():
    # pozovi pretprocesirani dataset u listi
    df = ucitaj_podatke_i_spoji()

    # ucitaj iz datoteke
    #df = pd.read_excel('Rezervacije_Trening.xlsx', index_col=0)

    # FILTRIRANJE SUVIŠNIH REDAKA
    df = df[df['broj_dana'] < 50]
    df = df[df['jedinice'] < 17]
    x = df.query('status_rezervacije == "F" or status_rezervacije == "N"  or status_rezervacije == "O" or status_rezervacije == "EF" or status_rezervacije == "EO" or status_rezervacije == "D"')

    print("UKUPNI BROJ STORNA JE ", df['storno'].sum())

    # izbaci nepotrebne kolone
    df = df.drop(columns=['id','id_rezervacije', 'sif_hotela', 'sif_usluge', 'tip_ro', 'broj_osoba', 'broj_djece', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'sif_drzave'])
    print("OVO JE NAKON PRVOG IZBACIVANJA")
    print(df.columns)

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

    # NUll vrijednosti zamijeni nulom u kolonama
    df['iznos_akontacije'].fillna(value=0, inplace=True)

    # stavi storno na kraj
    dfStorno = df['storno']
    df = df.drop('storno', axis='columns')
    df['storno'] = dfStorno

    # int to float za kolone
    int_kolone = ['kreirano_dana_prije_dolaska', 'broj_dana', 'broj_soba', 'jedinice', 'dat_storna_do_dat_dolaska', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'storno']
    for kolona in int_kolone:
        df[kolona] = df[kolona].astype(float)
        
    # MICANJE OUTLIERA I OSTALIH SUVIŠNIH KOLONA
    df = df.drop('postotak_akontacije', axis='columns')

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
    X = df.drop(columns= ['storno', 'broj_dana', 'p_tlak_zraka_31', 'jedinice', 'iznos_bruto', 'p_tlak_zraka_73', 'p_temp_max_73', 'p_oborine_mogucnost73', 'p_brzina_vjetra_31', 'mjesec', 'dan_u_tjednu', 'dan_u_godini', 'tjedan', 'kreirano_dana_prije_dolaska', 'p_oblaci_pokrice_31', 'p_oblaci_pokrice_73', 'iznos_akontacije', 'nocenja', 'prognoza3', 'prognoza1', 'prognoza7', 'dat_storna_do_dat_dolaska', 'temp_prosjek3', 'temp_max3', 'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7'], axis='columns')

    return X, y