import pandas as pd
from datetime import timedelta
from Domain import *
from pony.orm import Database, PrimaryKey, Required, Set, db_session, Optional
from uuid import uuid4 as gid, UUID
import os

#LISTAJ IZ DB REZERVACIJE NASTALE JUČER i RAZLOMI IH NA DANE TE IH SPREMI U DB
def spremiRezervacijeZadnja24Sata():
    listaRezervacija = Rezervacije.listaj_po_datumu_kreiranja_zadnja24h_sve()
    conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
    cur = conn.cursor()
    for rez in listaRezervacija:
        if rez['storno'] == "DA":
            rez['storno'] = 1
        else:
            rez['storno'] = 0
    for rez in listaRezervacija:
        dani = pd.date_range(rez['datum_od'], rez['datum_do']-timedelta(days=1), freq='d').strftime('%Y-%m-%d')
        #print(dani)
        lista = dani.tolist()
        brojDana = rez['broj_dana']
        totalIznos = rez['iznos_bruto'] 
        totalNocenja = rez['nocenja']
        totalPansion = rez['cijena_pans_usl']
        del rez['datum_od']
        del rez['datum_do']
        #IZRAČUNAJ VRIJEDNOSTI PO DANU ZA SVAKU REZERVACIJU
        IznosPoDanu = totalIznos / brojDana
        NocenjaPoDanu = totalNocenja / brojDana 
        PansionPoDanu = totalPansion / brojDana
        for dan in lista:
            dan = dt.datetime.strptime(dan, '%Y-%m-%d').date()
            rez['dan_boravka'] = dan
            rez['iznos_bruto'] = IznosPoDanu 
            rez['nocenja'] = NocenjaPoDanu 
            rez['cijena_pans_usl'] = PansionPoDanu 
            rez['mjesec'] = dan.month
            #spremi u bazu
            novi_id = str(gid())
            novi = {"id":novi_id, "id_rezervacije":rez['id'], "sif_hotela":rez['sif_hotela'], "godina":rez['godina'], "sif_rezervacije":rez['sif_rezervacije'], "rbr_stavke":rez['rbr_stavke'], "vrijeme_kreiranje":rez['vrijeme_kreiranje'], "datum_kreiranja":rez['datum_kreiranja'], "broj_dana":rez['broj_dana'], "sif_usluge":rez['sif_usluge'], "status_rezervacije":rez['status_rezervacije'], "datum_do_potvrde_opcije":rez['datum_do_potvrde_opcije'], "sif_drzave":rez['sif_drzave'], "sif_agencije":rez['sif_agencije'], "tip_ro":rez['tip_ro'], "obaveza_akontacije":rez['obaveza_akontacije'], "iznos_akontacije":rez['iznos_akontacije'], "storno":rez['storno'], "vrijeme_storna":rez['vrijeme_storna'], "datum_storna":rez['datum_storna'], "broj_osoba":rez['broj_osoba'], "broj_djece":rez['broj_djece'], "broj_soba":rez['broj_soba'], "nocenja":rez['nocenja'], "jedinice":rez['jedinice'], "cijena_pans_usl":rez['cijena_pans_usl'], "iznos_bruto":rez['iznos_bruto'], "valuta":rez['valuta'], "tecaj":rez['tecaj'], "lead_time_dani":rez['lead_time_dani'], "dat_storna_do_dat_dolaska":rez['dat_storna_do_dat_dolaska'], "tip_garancije":rez['tip_garancije'], "postotak_akontacije":rez['postotak_akontacije'], "mjesec":rez['mjesec'], "godina_rezervacije":rez['godina_rezervacije'], "vrsta_sobe":rez['vrsta_sobe'], "kanal":rez['kanal'], "nacin_rezervacije":rez['nacin_rezervacije'], "vrsta_sobe_naplata":rez['vrsta_sobe_naplata'], "dan_boravka":rez['dan_boravka']}
            sql_insert = """INSERT INTO rezervacijadani(id, id_rezervacije, sif_hotela, godina, sif_rezervacije, rbr_stavke, vrijeme_kreiranje, datum_kreiranja, broj_dana, sif_usluge, status_rezervacije, datum_do_potvrde_opcije, sif_drzave, sif_agencije, tip_ro, obaveza_akontacije, iznos_akontacije, storno, vrijeme_storna, datum_storna, broj_osoba, broj_djece, broj_soba, nocenja, jedinice, cijena_pans_usl, iznos_bruto, valuta, tecaj, lead_time_dani, dat_storna_do_dat_dolaska, tip_garancije, postotak_akontacije, mjesec, godina_rezervacije, vrsta_sobe, kanal, nacin_rezervacije, vrsta_sobe_naplata, dan_boravka) VALUES (%(id)s, %(id_rezervacije)s, %(sif_hotela)s, %(godina)s, %(sif_rezervacije)s, %(rbr_stavke)s, %(vrijeme_kreiranje)s, %(datum_kreiranja)s, %(broj_dana)s, %(sif_usluge)s, %(status_rezervacije)s, %(datum_do_potvrde_opcije)s, %(sif_drzave)s, %(sif_agencije)s, %(tip_ro)s, %(obaveza_akontacije)s, %(iznos_akontacije)s, %(storno)s, %(vrijeme_storna)s, %(datum_storna)s, %(broj_osoba)s, %(broj_djece)s, %(broj_soba)s, %(nocenja)s, %(jedinice)s, %(cijena_pans_usl)s, %(iznos_bruto)s, %(valuta)s, %(tecaj)s, %(lead_time_dani)s, %(dat_storna_do_dat_dolaska)s, %(tip_garancije)s, %(postotak_akontacije)s, %(mjesec)s, %(godina_rezervacije)s, %(vrsta_sobe)s, %(kanal)s, %(nacin_rezervacije)s, %(vrsta_sobe_naplata)s, %(dan_boravka)s)"""
            cur.execute(sql_insert, novi)
    conn.commit()
    print("GOTOVO")

# #TIMER
# schedule.every().day.at("06:00").do(spremiRezervacijeZadnja24Sata)
# #schedule.every(10).seconds.do(spremiRezervacijeZadnja24Sata)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    spremiRezervacijeZadnja24Sata() 
           
