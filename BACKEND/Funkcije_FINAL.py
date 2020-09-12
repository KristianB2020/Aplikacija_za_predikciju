import pandas as pd
from Domain import *
from uuid import uuid4 as gid, UUID
from datetime import timedelta, datetime
from pony.orm import Database, PrimaryKey, Required, Set, db_session, Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from datetime import timedelta, date
import os
import pickle
import psycopg2

# PREPROCESSING ZA PREDIKCIJE ZA DANAS ------------------------------------------------------------------------------------------------
def napravi_predikcije_za_danas():
    listaRezervacija = RezervacijeDani.listaj_rez_za_danas()
    listaPrognoza = VremePrognoze.listaj_prog_za_danas()

    # izračunaj dodatne stavke poput indexa vrućine za svaki zapis iz liste prognoza
    for stavka in listaPrognoza:
        # konstante indexa vrućine (°F)
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783 * 10**-3, -5.481717 * 10**-2, 1.22874*10**-3, 8.5282*10**-4, -1.99*10**-6
        T = (stavka['temp_max'] * 1.8) + 32
        V = stavka['relativna_vlaznost']
        stavka['index_vrucine'] = c1 + c2*T + c3*V + c4*T*V + c5*T**2 + c6*V**2 + c7*T**2*V + c8*T*V**2 + c9*T**2*V**2


    listaZaModel = []

    # SPOJI REZERVACIJE PO DATUMU S ODGOVARAJUĆIM PROGNOZAMA 1, 3 I 7 DANA PRIJE TOG DATUMA
    danas = dt.date.today()
    lista_br_dana_prije_dolaska = [1, 3, 7]

    for stavka in listaRezervacija:
        if stavka['vrsta_sobe'] == 'S2':
            stavka['vrsta_sobe'] = 'B220'
        if stavka['vrsta_sobe'] == 'DSU' or stavka['vrsta_sobe'] == 'S1' or stavka['vrsta_sobe'] == 'DSUM':
            stavka['vrsta_sobe'] = 'D1'
        if stavka['vrsta_sobe'] == 'S2':
            stavka['vrsta_sobe'] = 'B220'
        if stavka['vrsta_sobe'] == 'N31' or stavka['vrsta_sobe'] == 'N41' or stavka['vrsta_sobe'] == 'APP4' or stavka['vrsta_sobe'] == 'N52':
            stavka['vrsta_sobe'] = 'HA42M'
        for i in range(len(listaPrognoza)):
            for vrijednost in lista_br_dana_prije_dolaska:
                if vrijednost == listaPrognoza[i]['preostalo_dana']:
                    stavka['tlak_zraka' + str(vrijednost)] = listaPrognoza[i]['tlak_zraka']                
                    stavka['oblaci_pokrice' + str(vrijednost)] = listaPrognoza[i]['oblaci_pokrice']
                    stavka['temp_prosjek' + str(vrijednost)] = listaPrognoza[i]['temp_prosjek']
                    stavka['temp_max' + str(vrijednost)] = listaPrognoza[i]['temp_max']
                    stavka['temp_min' + str(vrijednost)] = listaPrognoza[i]['temp_min']
                    stavka['oborine_mogucnost' + str(vrijednost)] = listaPrognoza[i]['oborine_akumulirano']
                    stavka['brzina_vjetra' + str(vrijednost)] = listaPrognoza[i]['brzina_vjetra']
                    stavka['index_vrucine' + str(vrijednost)] = listaPrognoza[i]['index_vrucine']
                    stavka['prognoza' + str(vrijednost)] = listaPrognoza[i]['prognoza']
                    listaZaModel.append(stavka)

    for stavka in listaZaModel:
        stavka['p_tlak_zraka_31'] = stavka['tlak_zraka3'] - stavka['tlak_zraka1']
        stavka['p_tlak_zraka_73'] = stavka['tlak_zraka7'] - stavka['tlak_zraka3']
        stavka['p_temp_min_31'] = stavka['temp_min3'] - stavka['temp_min1']
        stavka['p_temp_min_73'] = stavka['temp_min7'] - stavka['temp_min3']
        stavka['p_temp_max_31'] = stavka['temp_max3'] - stavka['temp_max1']
        stavka['p_temp_max_73'] = stavka['temp_max7'] - stavka['temp_max3']
        stavka['p_oborine_mogucnost31'] = stavka['oborine_mogucnost3'] - stavka['oborine_mogucnost1']
        stavka['p_oborine_mogucnost73'] = stavka['oborine_mogucnost7'] - stavka['oborine_mogucnost3']
        stavka['p_oblaci_pokrice_31'] = stavka['oblaci_pokrice3'] - stavka['oblaci_pokrice1']
        stavka['p_oblaci_pokrice_73'] = stavka['oblaci_pokrice7'] - stavka['oblaci_pokrice3']
        stavka['p_brzina_vjetra_31'] = stavka['brzina_vjetra3'] - stavka['brzina_vjetra1']
        stavka['p_brzina_vjetra_73'] = stavka['brzina_vjetra7'] - stavka['brzina_vjetra3']

    df = pd.DataFrame(listaZaModel)

    # ListaSaSiframa, df_danb, df_bruto i df_jed su kreirani za spremanje sa predikcijama u DB
    ListaSaSiframa = df['sif_rezervacije']
    df['dan_boravka']= pd.to_datetime(df['dan_boravka'])
    df_danb =  df['dan_boravka']
    df_jed =  df['jedinice']
    df_bruto =  df['iznos_bruto']
    df = df.drop(columns=['id','id_rezervacije', 'sif_hotela', 'datum_kreiranja', 'dan_boravka', 'sif_usluge', 'tip_ro', 'broj_osoba', 'broj_djece', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'sif_drzave'])
    
    # NUll vrijednosti zamijeni nulom u kolonama
    df['iznos_akontacije'].fillna(value=0, inplace=True)

    # makni ostale suvišne kolone
    df = df.drop(columns= ['broj_dana', 'storno', 'postotak_akontacije', 'p_tlak_zraka_31', 'jedinice', 'p_tlak_zraka_73', 'p_temp_max_73', 'p_oborine_mogucnost73', 'p_brzina_vjetra_31', 'p_oblaci_pokrice_31', 'p_oblaci_pokrice_73', 'iznos_akontacije', 'nocenja', 'prognoza3', 'prognoza1', 'prognoza7', 'dat_storna_do_dat_dolaska', 'temp_prosjek3', 'temp_max3', 'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7'], axis='columns')
    df['tip_garancije'] = df['tip_garancije'].fillna('O')

    # Definicija tipova kolona za daljnje procesiranje
    numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 
                 'oborine_mogucnost1',  'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
    kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']

    # LOAD PIPELINE-A
    PrepPipeline = pickle.load(open('./Pipeline/Pipeline_Total.pkl', 'rb'))
    X_fit = PrepPipeline.transform(df)

    # učitaj model za predikciju
    prag_odluke = 0.609095
    model = pickle.load(open('./Modeli/Model_Final.pkl', 'rb'))
    predikcije = (model.predict_proba(X_fit)[:,1]>=prag_odluke).astype(int)

    broj_zapisa = predikcije.shape[0]
    lista_id = []
    listaDatuma = []
    for i in range(broj_zapisa):
        i = str(gid())
        lista_id.append(i)

    # spremi excelicu sa predikcijama
    for i in df_danb:
        i = (datetime.date(i))
        listaDatuma.append(i)

    df_pred = pd.DataFrame(lista_id, columns=['id'])
    df_pred['dan_boravka'] = listaDatuma
    df_pred['sif_rezervacije'] = ListaSaSiframa
    df_pred['vrsta_sobe'] = df['vrsta_sobe']
    df_pred['kanal'] = df['kanal']
    df_pred['jedinice'] = df_jed
    df_pred['iznos_bruto'] = df_bruto
    df_pred['predikcije'] = predikcije
    df_pred['datum_predikcije'] = date.today()


    # df_pred.to_excel('./Excelice/Predikcije/Predikcije' + str(date.today()) + '.xlsx')
    #listaPredikcija = df_pred.to_numpy()
    listaPredikcija = df_pred.to_dict('records')
    print(listaPredikcija[0])

    # SPREMI U DB
    conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
    for stavka in listaPredikcija:
        novi = {"id":stavka['id'], "dan_boravka":stavka['dan_boravka'], "sif_rezervacije":stavka['sif_rezervacije'],  "vrsta_sobe":stavka['vrsta_sobe'], "kanal":stavka['kanal'], "jedinice":stavka['jedinice'], "iznos_bruto":stavka['iznos_bruto'], "predikcije":stavka['predikcije'], "datum_predikcije":stavka['datum_predikcije']}
        cur = conn.cursor()
        cur.execute("""INSERT INTO predikcije(id, dan_boravka, sif_rezervacije, vrsta_sobe, kanal, jedinice, iznos_bruto, predikcije, datum_predikcije) VALUES (%(id)s, %(dan_boravka)s, %(sif_rezervacije)s, %(vrsta_sobe)s, %(kanal)s, %(jedinice)s, %(iznos_bruto)s, %(predikcije)s, %(datum_predikcije)s)""", novi)
        conn.commit()
    print("nova predikcija uspješno ubačena")


# PREPROCESSING ZA PREDIKCIJE OD SUTRA DO PLUS 8 DANA ------------------------------------------------------------------------------------------------

def napravi_predikcije_za_ostale_dane():
    listaZaSpremanje = []

    # KREIRAJ LISTU SA DATUMIMA ZA IDUĆIH 8 DANA OD SUTRA
    sutra = (dt.date.today()) + timedelta(days = 1)
    listaDana = []
    for i in range(0, 8):
        datum = sutra + timedelta(days=i)
        listaDana.append(datum)
    lista_br_dana_prije_dolaska = [1, 3, 7]

    # UCITAJ PODATKE IZ DB 
    for dan in listaDana:
        listaZaModel = []
        razlika = (dan - (dt.date.today())).days
        listaRezervacija = RezervacijeDani.listaj_rez_za_datum(dan)
        listaPrognoza = VremePrognoze.listaj_prog_za_datum(dan)
        jucer = dan - timedelta(days=1)
        listaPredikcija = Outputi.listaj_pred_za_datum(jucer)
        # izračunaj dodatne stavke poput indexa vrućine za svaki zapis iz liste prognoza
        for stavka in listaPrognoza:
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783 * 10**-3, -5.481717 * 10**-2, 1.22874*10**-3, 8.5282*10**-4, -1.99*10**-6
            T = (stavka['temp_max'] * 1.8) + 32
            V = stavka['relativna_vlaznost']
            stavka['index_vrucine'] = c1 + c2*T + c3*V + c4*T*V + c5*T**2 + c6*V**2 + c7*T**2*V + c8*T*V**2 + c9*T**2*V**2

        # PREPROCESIRAJ PODATKE
        for stavka in listaRezervacija:
            if stavka['vrsta_sobe'] == 'S2':
                stavka['vrsta_sobe'] = 'B220'
            if stavka['vrsta_sobe'] == 'DSU' or stavka['vrsta_sobe'] == 'S1' or stavka['vrsta_sobe'] == 'DSUM':
                stavka['vrsta_sobe'] = 'D1'
            if stavka['vrsta_sobe'] == 'S2':
                stavka['vrsta_sobe'] = 'B220'
            if stavka['vrsta_sobe'] == 'N31' or stavka['vrsta_sobe'] == 'N41' or stavka['vrsta_sobe'] == 'APP4' or stavka['vrsta_sobe'] == 'N52':
                stavka['vrsta_sobe'] = 'HA42M'
            for i in range(len(listaPrognoza)):
                for vrijednost in lista_br_dana_prije_dolaska:
                    if (stavka['dan_boravka'] == listaPrognoza[i]['datum']) and ((razlika + vrijednost) == listaPrognoza[i]['preostalo_dana']):
                        stavka['tlak_zraka' + str(vrijednost)] = listaPrognoza[i]['tlak_zraka']                
                        stavka['oblaci_pokrice' + str(vrijednost)] = listaPrognoza[i]['oblaci_pokrice']
                        stavka['temp_prosjek' + str(vrijednost)] = listaPrognoza[i]['temp_prosjek']
                        stavka['temp_max' + str(vrijednost)] = listaPrognoza[i]['temp_max']
                        stavka['temp_min' + str(vrijednost)] = listaPrognoza[i]['temp_min']
                        stavka['oborine_mogucnost' + str(vrijednost)] = listaPrognoza[i]['oborine_akumulirano']
                        stavka['brzina_vjetra' + str(vrijednost)] = listaPrognoza[i]['brzina_vjetra']
                        stavka['index_vrucine' + str(vrijednost)] = listaPrognoza[i]['index_vrucine']
                        stavka['prognoza' + str(vrijednost)] = listaPrognoza[i]['prognoza']
            listaZaModel.append(stavka)

        for stavka in listaZaModel:
            stavka['p_tlak_zraka_31'] = stavka['tlak_zraka3'] - stavka['tlak_zraka1']
            stavka['p_tlak_zraka_73'] = stavka['tlak_zraka7'] - stavka['tlak_zraka3']
            stavka['p_temp_min_31'] = stavka['temp_min3'] - stavka['temp_min1']
            stavka['p_temp_min_73'] = stavka['temp_min7'] - stavka['temp_min3']
            stavka['p_temp_max_31'] = stavka['temp_max3'] - stavka['temp_max1']
            stavka['p_temp_max_73'] = stavka['temp_max7'] - stavka['temp_max3']
            stavka['p_oborine_mogucnost31'] = stavka['oborine_mogucnost3'] - stavka['oborine_mogucnost1']
            stavka['p_oborine_mogucnost73'] = stavka['oborine_mogucnost7'] - stavka['oborine_mogucnost3']
            stavka['p_oblaci_pokrice_31'] = stavka['oblaci_pokrice3'] - stavka['oblaci_pokrice1']
            stavka['p_oblaci_pokrice_73'] = stavka['oblaci_pokrice7'] - stavka['oblaci_pokrice3']
            stavka['p_brzina_vjetra_31'] = stavka['brzina_vjetra3'] - stavka['brzina_vjetra1']
            stavka['p_brzina_vjetra_73'] = stavka['brzina_vjetra7'] - stavka['brzina_vjetra3']

        # PROVJERI AKO JE NEKA REZERVACIJA VEĆ KLASIFICIRANA KAO STORNO U PRETHODNOJ PREDIKCIJI I OZNAČI JE SUKLADNO (da se izbjegne slučaj da jedan dan iste rezervacije bude klasificiran kao storno, a drugi ne)
        for stavka in listaZaModel:
            for i in range(len(listaPredikcija)):
                if stavka['sif_rezervacije'] == listaPredikcija[i]['sif_rezervacije']:
                    stavka['storno'] = 1
                else:
                    stavka['storno'] = 0

        dfTotal = pd.DataFrame(listaZaModel)

        # PODIJELI NA STORNO DA/NE, PREMA FILTRIRANJU U PRETHODNOM KORAKU
        dfDA = dfTotal[dfTotal['storno'] == 1]
        df = dfTotal[dfTotal['storno'] == 0]

        # NASTAVI PROCESIRANJE PODATAKA IZ FILTRIRANIH REZERVACIJA
        # ListaSaSiframa, df_danb, df_bruto i df_jed su kreirani za spremanje sa predikcijama u DB
        ListaSaSiframa = df['sif_rezervacije']
        df['dan_boravka']= pd.to_datetime(df['dan_boravka'])
        df_danb =  df['dan_boravka']
        df_jed =  df['jedinice']
        df_bruto =  df['iznos_bruto']
        df = df.drop(columns=['id','id_rezervacije', 'sif_hotela', 'datum_kreiranja', 'dan_boravka', 'sif_usluge', 'tip_ro', 'broj_osoba', 'broj_djece', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'sif_drzave'])
    
        # zamijeni NUll vrijednosti 
        df['iznos_akontacije'].fillna(value=0, inplace=True)
        df['tip_garancije'] = df['tip_garancije'].fillna('O')
        df = df.drop(columns= ['broj_dana', 'storno', 'postotak_akontacije', 'p_tlak_zraka_31', 'jedinice', 'iznos_bruto', 'p_tlak_zraka_73', 'p_temp_max_73', 'p_oborine_mogucnost73', 'p_brzina_vjetra_31', 'p_oblaci_pokrice_31', 'p_oblaci_pokrice_73', 'iznos_akontacije', 'nocenja', 'prognoza3', 'prognoza1', 'prognoza7', 'dat_storna_do_dat_dolaska', 'temp_prosjek3', 'temp_max3', 'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7'], axis='columns')
        
        # Definicija tipova kolona za daljnje procesiranje
        numericke = ['index_vrucine1', 'temp_prosjek1', 'broj_soba', 'temp_max1', 'temp_min1', 'brzina_vjetra1', 'tlak_zraka1', 'oblaci_pokrice1', 'oborine_mogucnost1',  'p_temp_min_31', 'p_temp_min_73', 'p_temp_max_31',  'p_oborine_mogucnost31', 'p_brzina_vjetra_73']
        kategoricke = ['nacin_rezervacije', 'status_rezervacije', 'vrsta_sobe', 'kanal', 'tip_garancije']

        # LOAD PIPELINE-A
        PrepPipeline = pickle.load(open('./Pipeline/Pipeline_Total.pkl', 'rb'))
        X_fit = PrepPipeline.transform(df)

        # učitaj model za predikciju
        prag_odluke = 0.609095
        model = pickle.load(open('./Modeli/Model_Final.pkl', 'rb'))
        predikcije = (model.predict_proba(X_fit)[:,1]>=prag_odluke).astype(int)

        broj_zapisa = predikcije.shape[0]
        lista_id = []
        listaDatuma = []
        for i in range(broj_zapisa):
            i = str(gid())
            lista_id.append(i)

        for i in df_danb:
            i = (datetime.date(i))
            listaDatuma.append(i)

        df_pred = pd.DataFrame(lista_id, columns=['id'])
        df_pred['dan_boravka'] = listaDatuma
        df_pred['sif_rezervacije'] = ListaSaSiframa
        df_pred['vrsta_sobe'] = df['vrsta_sobe']
        df_pred['kanal'] = df['kanal']
        df_pred['jedinice'] = df_jed
        df_pred['iznos_bruto'] = df_bruto
        df_pred['predikcije'] = predikcije
        df_pred['datum_predikcije'] = date.today()

        # PROCESIRAJ I PRIDODAJ OTPRIJE FILTRIRANE ZAPISE KONAČNOM DATASETU ZA UPIS U BAZU
        listaSifriRezervacija = dfDA['sif_rezervacije']
        dfDA = dfDA.drop(columns=['postotak_akontacije', 'id','id_rezervacije', 'sif_hotela', 'sif_usluge', 'tip_ro', 'broj_osoba', 'broj_djece', 'cijena_pans_usl', 'godina', 'sif_rezervacije', 'rbr_stavke', 'vrijeme_kreiranje', 'valuta', 'tecaj', 'vrijeme_storna', 'sif_agencije', 'tip_garancije', 'lead_time_dani', 'datum_do_potvrde_opcije', 'mjesec', 'datum_storna', 'vrsta_sobe_naplata', 'index_vrucine1', 'index_vrucine3', 'index_vrucine7', 'godina_rezervacije', 'obaveza_akontacije', 'nacin_rezervacije', 'sif_drzave'])
        dfDA['dan_boravka']= pd.to_datetime(dfDA['dan_boravka'])
        dfDA = dfDA.drop(columns= ['datum_kreiranja', 'storno', 'iznos_akontacije', 'nocenja', 'prognoza3', 'prognoza1', 'prognoza7', 'dat_storna_do_dat_dolaska', 'temp_prosjek1', 'temp_prosjek3', 'temp_max3', 'temp_min3', 'brzina_vjetra3', 'tlak_zraka3', 'oblaci_pokrice3', 'oborine_mogucnost3', 'temp_prosjek7', 'temp_max7', 'temp_min7', 'brzina_vjetra7', 'tlak_zraka7', 'oblaci_pokrice7', 'oborine_mogucnost7'], axis='columns')

        listaIdStorna = []
        for i in range(dfDA.shape[0]):
            i = str(gid())
            listaIdStorna.append(i)

        dfDodaj = pd.DataFrame(listaIdStorna, columns=['id'])
        dfDodaj['dan_boravka'] = dfDA['dan_boravka']
        dfDodaj['sif_rezervacije'] = listaSifriRezervacija
        dfDodaj['vrsta_sobe'] = dfDA['vrsta_sobe']
        dfDodaj['kanal'] = dfDA['kanal']
        dfDodaj['jedinice'] = dfDA['jedinice']
        dfDodaj['iznos_bruto'] = dfDA['iznos_bruto']
        dfDodaj['predikcije'] = 1
        dfDodaj['datum_predikcije'] = date.today()


        df_pred = df_pred.append(dfDodaj, ignore_index = True)
        df_pred = df_pred[~(df_pred.isna().any(axis=1))]
        
        # SPREMI U DB
        listaPredikcija = df_pred.to_dict('records')
        conn = psycopg2.connect(("dbname=Mlprojekt user=Kris password=bbforlife host=localhost"))
        for stavka in listaPredikcija:
            novi = {"id":stavka['id'], "dan_boravka":stavka['dan_boravka'], "sif_rezervacije":stavka['sif_rezervacije'],  "vrsta_sobe":stavka['vrsta_sobe'], 
                    "kanal":stavka['kanal'], "jedinice":stavka['jedinice'], "iznos_bruto":stavka['iznos_bruto'], "predikcije":stavka['predikcije'], 
                    "datum_predikcije":stavka['datum_predikcije']}
            cur = conn.cursor()
            cur.execute("""INSERT INTO predikcije(id, dan_boravka, sif_rezervacije, vrsta_sobe, kanal, jedinice, iznos_bruto, predikcije, datum_predikcije) 
                        VALUES (%(id)s, %(dan_boravka)s, %(sif_rezervacije)s, %(vrsta_sobe)s, %(kanal)s, %(jedinice)s, %(iznos_bruto)s, %(predikcije)s,
                        %(datum_predikcije)s)""", novi)
            conn.commit()

    print("predikcije uspješno ubačene")



