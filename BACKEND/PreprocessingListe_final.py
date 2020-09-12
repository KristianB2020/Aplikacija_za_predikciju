from Models import *
from Domain import *
from pony.orm import *
import pandas as pd
import numpy as np
from uuid import uuid4 as gid, UUID
from openpyxl.workbook import Workbook
import datetime as dt

def ucitaj_podatke_i_spoji():
    listaRezervacija = RezervacijeDani.listaj_trening()
    listaDanaStorna = RezervacijeDani.listaj_sav_storno()
    listaRezervacijaFinal = []
    listaZaModel = []
    listaDana = [1,3,7]
    listaPrognoza = VremePrognoze.listaj_iz_baze_trening()
    listaStorna = []
    listaZaProcesiranjeStorna = []
    listaAktivnih = []
    listaZaProcesiranjeAktivnih = []

    # za svaki dan u listi pronađi otkazane rezervacije prema uvjetu i neotkazane rezervacije na taj dan
    for stavka in listaDanaStorna:
            datum = stavka
            listaElemenata = [element for idx, element in enumerate(listaRezervacija) if element['dan_boravka'] == datum and ((element['storno'] == 1 and (0 <= element['dat_storna_do_dat_dolaska'] <= 8)) or element['storno'] == 0)]
            for e in listaElemenata:
                listaRezervacijaFinal.append(e)

    # izračunaj index vrućine za svaki zapis
    for stavka in listaPrognoza:
            # konstante indexa vrućine (°F)
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783 * 10**-3, -5.481717 * 10**-2, 1.22874*10**-3, 8.5282*10**-4, -1.99*10**-6
            T = (stavka['temp_max'] * 1.8) + 32
            V = stavka['relativna_vlaznost']
            stavka['index_vrucine'] = c1 + c2*T + c3*V + c4*T*V + c5*T**2 + c6*V**2 + c7*T**2*V + c8*T*V**2 + c9*T**2*V**2

    # filtriraj stornirane rezervacije u zasebnu listu zbog daljnjeg procesiranja
    for stavka in listaRezervacijaFinal:
            if stavka['storno'] == 1:
                listaStorna.append(stavka)
            else:
                listaAktivnih.append(stavka)

    # PROCESIRANJE OTKAZANIH REZERVACIJA
    # svakoj otkazanoj rezervaciji pridruži danu boravka prognoze 1, 3 i 7 dana prije dana otkazivanja
    for stavka in listaStorna:
        for dan in listaDana:
            vrijednost = dan + stavka['dat_storna_do_dat_dolaska']
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == vrijednost]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        listaZaProcesiranjeStorna.append(stavka)


    # Obrada null vrijednosti zbog daljnjih kalkulacija
    df = pd.DataFrame(listaZaProcesiranjeStorna)

    # ispši broj null vrijednosti u kolonama
    print(df.isna().sum())

    df['oblaci_pokrice1'] = df["oblaci_pokrice1"].fillna(value=df["oblaci_pokrice1"].mean())
    df['oblaci_pokrice3'] = df["oblaci_pokrice3"].fillna(value=df["oblaci_pokrice3"].mean())
    df['oblaci_pokrice7'] = df["oblaci_pokrice7"].fillna(value=df["oblaci_pokrice7"].mean())

    # kreiranje finalne liste u koju stavljamo sve zapise vezane za otkazane rezervacije
    final = df.to_dict('records')

    # PROCESIRANJE NEOTKAZANIH REZERVACIJA----------------------------------------------------------------------------------------------------------------
    for stavka in listaAktivnih:
        for dan in listaDana:
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == dan]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        # dodaj u finalnu listu i zapise vezane za neotkazane rezervacije
        final.append(stavka)

    for stavka in final:
        # dodaj kljuceve i zapise za promjene u atributima vremena od prognoze do prognoze
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
        # GENERALNA PRAVILA - "izbaci" rezervacije otkazane na vedar dan (prema definiciji) za sva godišnja doba
        pravila_1 = [(10 <= stavka['temp_max1'] <= 30), (10 <= stavka['temp_max7'] <= 30), (10 <= stavka['temp_max3'] <= 30), stavka['brzina_vjetra1'] < 15, stavka['brzina_vjetra7'] < 15, stavka['brzina_vjetra3'] < 15, stavka['prognoza1'] == "Clear" or stavka['prognoza1'] == "Few clouds", stavka['prognoza7'] == "Clear" or stavka['prognoza7'] == "Few clouds" or stavka['prognoza3'] == "Clear" or stavka['prognoza3'] == "Few clouds", stavka['storno'] == 1]
        pravila_1_zima = [(10 <= stavka['temp_max1'] <= 30), (10 <= stavka['temp_max7'] <= 30), (10 <= stavka['temp_max3'] <= 30), stavka['brzina_vjetra1'] < 15, stavka['brzina_vjetra7'] < 15, stavka['brzina_vjetra3'] < 15, stavka['prognoza1'] == "Clear" or stavka['prognoza1'] == "Few clouds", stavka['prognoza7'] == "Clear" or stavka['prognoza7'] == "Few clouds" or stavka['prognoza3'] == "Clear" or stavka['prognoza3'] == "Few clouds", stavka['storno'] == 1, (1 <= stavka['mjesec'] <=12)]
        pravila_2_zima = [(10 <= stavka['temp_max1'] <= 30), (10 <= stavka['temp_max7'] <= 30), (10 <= stavka['temp_max3'] <= 30),stavka['brzina_vjetra1'] < 15, stavka['brzina_vjetra7'] < 15, stavka['brzina_vjetra3'] < 15, stavka['prognoza1'] == "Clear" or stavka['prognoza1'] == "Few clouds", stavka['prognoza7'] == "Clear" or stavka['prognoza7'] == "Few clouds" or stavka['prognoza3'] == "Clear" or stavka['prognoza3'] == "Few clouds", stavka['storno'] == 1, (1 <= stavka['mjesec'] <=3)]
        # "izbaci" storno kada je normalan tlak_zraka i brzina vjetra te prognoza Vedro (koristena Beaufort-ova skala)
        pravilo_vedro1 = [((1009 < stavka['tlak_zraka1'] <= 1022) and (stavka['brzina_vjetra1'] < 24) and (stavka['prognoza1'] == 'Clear' or stavka['prognoza1'] == 'Few clouds')), ((1009 < stavka['tlak_zraka3'] <= 1022) and (stavka['brzina_vjetra3'] < 24) and (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds')), ((1009 < stavka['tlak_zraka7'] <= 1022) and (stavka['brzina_vjetra7'] < 24) and (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds'))]
        # "izbaci" storno kada je normalan tlak_zraka, nema oborina te je prognoza Vedro
        pravilo_vedro2 = [((1009 < stavka['tlak_zraka1'] <= 1022) and (stavka['oborine_mogucnost1'] == 0 ) and (stavka['prognoza1'] == 'Clear' or stavka['prognoza1'] == 'Few clouds')), ((1009 < stavka['tlak_zraka3'] <= 1022) and (stavka['oborine_mogucnost3'] == 0) and (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds')), ((1009 < stavka['tlak_zraka7'] <= 1022) and (stavka['oborine_mogucnost7'] == 0) and (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds'))]
        # "izbaci" storna na povoljan index vrućine te kada je prognoza bila vedro 
        pravilo_vedro3 = [stavka['index_vrucine1'] <= 124 and (stavka['prognoza1'] == 'Clear' or stavka['prognoza1'] == 'Few clouds'), stavka['index_vrucine3'] <= 124 and (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds'), stavka['index_vrucine7'] <= 124 and (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds')]
        if (stavka['kanal'] == 'Grupe') or (stavka['kanal'] == 'Mice'):
            stavka['storno'] = 0
        if stavka['jedinice'] > 15:
            stavka['storno'] = 0
        if all(pravila_1): 
            stavka['storno'] = 0
        if all(pravila_1_zima):
            stavka['storno'] = 0
        if all(pravila_2_zima):
            stavka['storno'] = 0
        if all(pravilo_vedro1):
            stavka['storno'] = 0
        if all(pravilo_vedro2):
            stavka['storno'] = 0
        if all(pravilo_vedro3):
            stavka['storno'] = 0
        # rezervacije koje nisu otkazane imaju praznu (NoneType) vrijednosti u koloni dat_storna_do_datuma_dolaska(if uvjet sprječava pogrešku)
        if stavka['storno'] == 1:    
            # ponovi prethodna pravila sukladno tome koliko se rezervacija otkazala dana prije dolaska
            pravilo_vedro13 = [(1 < stavka['dat_storna_do_dat_dolaska'] <= 3), (1009 < stavka['tlak_zraka3'] <= 1022), (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds'), (stavka['brzina_vjetra3'] < 24), (1009 < stavka['tlak_zraka7'] <= 1022), (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds'), (stavka['brzina_vjetra7'] < 24)]   
            pravilo_vedro17 = [(stavka['dat_storna_do_dat_dolaska'] > 3), (1009 < stavka['tlak_zraka7'] <= 1022), (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds'), (stavka['brzina_vjetra7'] < 24)]
            pravilo_vedro23 = [(1 < stavka['dat_storna_do_dat_dolaska'] <= 3), (1009 < stavka['tlak_zraka3'] <= 1022), (stavka['oborine_mogucnost3'] == 0), (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds'), (1009 < stavka['tlak_zraka7'] <= 1022), (stavka['oborine_mogucnost7'] == 0), (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds')]
            pravilo_vedro27 = [(stavka['dat_storna_do_dat_dolaska'] > 3), (1009 < stavka['tlak_zraka7'] <= 1022), (stavka['oborine_mogucnost7'] == 0), (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds')]
            pravilo_vedro33 = [(1 < stavka['dat_storna_do_dat_dolaska'] <= 3), (stavka['index_vrucine3'] <= 124),  (stavka['prognoza3'] == 'Clear' or stavka['prognoza3'] == 'Few clouds'), (stavka['index_vrucine7'] <= 124),  (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds')]
            pravilo_vedro37 = [(stavka['dat_storna_do_dat_dolaska'] > 3), (stavka['index_vrucine7'] <= 124),  (stavka['prognoza7'] == 'Clear' or stavka['prognoza7'] == 'Few clouds')]
            if all(pravilo_vedro13):
                stavka['storno'] = 0
            if all(pravilo_vedro17):
                stavka['storno'] = 0
            if all(pravilo_vedro23):
                stavka['storno'] = 0
            if all(pravilo_vedro27):
                stavka['storno'] = 0

    dfFinal = pd.DataFrame(final)
    dfFinal.to_excel('Rezervacije_Trening.xlsx')
    return dfFinal

#---------------------------------------------------------------------FUNKCIJA ZA SPAJANJE DATASETA ZA ANALIZU-------------------------------------------
def ucitaj_podatke_i_spoji_za_analizu():
    listaRezervacija = RezervacijeDani.listaj_trening()
    listaDanaStorna = RezervacijeDani.listaj_sav_storno()
    listaRezervacijaFinal = []
    listaZaModel = []
    listaDana = [1,3,7]
    listaPrognoza = VremePrognoze.listaj_iz_baze_trening()
    listaStorna = []
    listaZaProcesiranjeStorna = []
    listaAktivnih = []
    listaZaProcesiranjeAktivnih = []

    # za svaki dan u listi pronađi otkazane rezervacije prema uvjetu i neotkazane rezervacije na taj dan
    for stavka in listaDanaStorna:
            datum = stavka
            listaElemenata = [element for idx, element in enumerate(listaRezervacija) if element['dan_boravka'] == datum and ((element['storno'] == 1 and (0 <= element['dat_storna_do_dat_dolaska'] <= 8)) or element['storno'] == 0)]
            for e in listaElemenata:
                listaRezervacijaFinal.append(e)

    # izračunaj index vrućine za svaki zapis
    for stavka in listaPrognoza:
            # konstante indexa vrućine (°F)
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783 * 10**-3, -5.481717 * 10**-2, 1.22874*10**-3, 8.5282*10**-4, -1.99*10**-6
            T = (stavka['temp_max'] * 1.8) + 32
            V = stavka['relativna_vlaznost']
            stavka['index_vrucine'] = c1 + c2*T + c3*V + c4*T*V + c5*T**2 + c6*V**2 + c7*T**2*V + c8*T*V**2 + c9*T**2*V**2

    # filtriraj stornirane rezervacije u zasebnu listu zbog daljnjeg procesiranja
    for stavka in listaRezervacijaFinal:
            if stavka['storno'] == 1:
                listaStorna.append(stavka)
            else:
                listaAktivnih.append(stavka)

    # PROCESIRANJE OTKAZANIH REZERVACIJA
    # svakoj otkazanoj rezervaciji pridruži danu boravka prognoze 1, 3 i 7 dana prije dana otkazivanja
    for stavka in listaStorna:
        for dan in listaDana:
            vrijednost = dan + stavka['dat_storna_do_dat_dolaska']
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == vrijednost]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        listaZaProcesiranjeStorna.append(stavka)


    # Obrada null vrijednosti zbog daljnjih kalkulacija
    df = pd.DataFrame(listaZaProcesiranjeStorna)

    # ispiši broj null vrijednosti u kolonama
    print(df.isna().sum())

    df['oblaci_pokrice1'] = df["oblaci_pokrice1"].fillna(value=df["oblaci_pokrice1"].mean())
    df['oblaci_pokrice3'] = df["oblaci_pokrice3"].fillna(value=df["oblaci_pokrice3"].mean())
    df['oblaci_pokrice7'] = df["oblaci_pokrice7"].fillna(value=df["oblaci_pokrice7"].mean())

    # kreiranje finalne liste u koju stavljamo sve zapise vezane za otkazane rezervacije
    final = df.to_dict('records')

    # PROCESIRANJE NEOTKAZANIH REZERVACIJA----------------------------------------------------------------------------------------------------------------
    for stavka in listaAktivnih:
        for dan in listaDana:
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == dan]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        # dodaj u finalnu listu i zapise vezane za neotkazane rezervacije
        final.append(stavka)

    dfFinal = pd.DataFrame(final)
    dfFinal.to_excel('Rezervacije_Analiza.xlsx')
    return dfFinal

#---------------------------------------------------------------------FUNKCIJA ZA SPAJANJE DATASETA ZA ANALIZU-------------------------------------------


def ucitaj_podatke_i_spoji_u_jedinstven_set():
    listaRezervacija = RezervacijeDani.listaj_trening()
    listaDanaStorna = RezervacijeDani.listaj_sav_storno()
    listaRezervacijaFinal = []
    listaZaModel = []
    listaDana = [1,3,7]
    listaPrognoza = VremePrognoze.listaj_iz_baze_trening()
    listaStorna = []
    listaZaProcesiranjeStorna = []
    listaAktivnih = []
    listaZaProcesiranjeAktivnih = []

    # za svaki dan u listi pronađi otkazane rezervacije prema uvjetu i neotkazane rezervacije na taj dan
    for stavka in listaDanaStorna:
            datum = stavka
            listaElemenata = [element for idx, element in enumerate(listaRezervacija) if element['dan_boravka'] == datum and ((element['storno'] == 1 and (0 <= element['dat_storna_do_dat_dolaska'] <= 8)) or element['storno'] == 0)]
            for e in listaElemenata:
                listaRezervacijaFinal.append(e)

    # izračunaj index vrućine za svaki zapis
    for stavka in listaPrognoza:
            # konstante indexa vrućine (°F)
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783 * 10**-3, -5.481717 * 10**-2, 1.22874*10**-3, 8.5282*10**-4, -1.99*10**-6
            T = (stavka['temp_max'] * 1.8) + 32
            V = stavka['relativna_vlaznost']
            stavka['index_vrucine'] = c1 + c2*T + c3*V + c4*T*V + c5*T**2 + c6*V**2 + c7*T**2*V + c8*T*V**2 + c9*T**2*V**2

    # filtriraj stornirane rezervacije u zasebnu listu zbog daljnjeg procesiranja
    for stavka in listaRezervacijaFinal:
            if stavka['storno'] == 1:
                listaStorna.append(stavka)
            else:
                listaAktivnih.append(stavka)

    # PROCESIRANJE OTKAZANIH REZERVACIJA
    # svakoj otkazanoj rezervaciji pridruži danu boravka prognoze 1, 3 i 7 dana prije dana otkazivanja
    for stavka in listaStorna:
        for dan in listaDana:
            vrijednost = dan + stavka['dat_storna_do_dat_dolaska']
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == vrijednost]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        listaZaProcesiranjeStorna.append(stavka)


    # Obrada null vrijednosti zbog daljnjih kalkulacija
    df = pd.DataFrame(listaZaProcesiranjeStorna)

    # ispši broj null vrijednosti u kolonama
    print(df.isna().sum())

    df['oblaci_pokrice1'] = df["oblaci_pokrice1"].fillna(value=df["oblaci_pokrice1"].mean())
    df['oblaci_pokrice3'] = df["oblaci_pokrice3"].fillna(value=df["oblaci_pokrice3"].mean())
    df['oblaci_pokrice7'] = df["oblaci_pokrice7"].fillna(value=df["oblaci_pokrice7"].mean())

    # kreiranje finalne liste u koju stavljamo sve zapise vezane za otkazane rezervacije
    final = df.to_dict('records')

    # PROCESIRANJE NEOTKAZANIH REZERVACIJA----------------------------------------------------------------------------------------------------------------
    for stavka in listaAktivnih:
        for dan in listaDana:
            listaIndexa = [idx for idx, element in enumerate(listaPrognoza) if element['datum'] == stavka['dan_boravka'] and element['preostalo_dana'] == dan]
            for index in listaIndexa:
                stavka['tlak_zraka' + str(dan)] = listaPrognoza[index]['tlak_zraka']
                stavka['oblaci_pokrice'+ str(dan)] = listaPrognoza[index]['oblaci_pokrice']
                stavka['temp_prosjek' + str(dan)] = listaPrognoza[index]['temp_prosjek']
                stavka['temp_max' + str(dan)] = listaPrognoza[index]['temp_max']
                stavka['temp_min' + str(dan)] = listaPrognoza[index]['temp_min']
                stavka['oborine_mogucnost' + str(dan)] = listaPrognoza[index]['oborine_akumulirano']
                stavka['brzina_vjetra' + str(dan)] = listaPrognoza[index]['brzina_vjetra']
                stavka['index_vrucine' + str(dan)] = listaPrognoza[index]['index_vrucine']
                stavka['prognoza' + str(dan)] = listaPrognoza[index]['prognoza']
        # dodaj u finalnu listu i zapise vezane za neotkazane rezervacije
        final.append(stavka)

    for stavka in final:
        # dodaj kljuceve i zapise za promjene u atributima vremena od prognoze do prognoze
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
        

    dfFinal = pd.DataFrame(final)
    dfFinal.to_excel('Rezervacije_Jedinstveni_Set.xlsx')
    return dfFinal
