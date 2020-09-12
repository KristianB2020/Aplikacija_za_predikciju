import pandas as pd
import psycopg2
from uuid import uuid4 as gid

#pročitaj iz datoteke
data = pd.read_excel("./Excelice/TestRezervacijeZaPredikciju2.xlsx")
#spremi u listu i DB
lista = data.values.tolist()

conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
cur = conn.cursor()

for stavka in lista:
    # provjeri ako su vrijednosti prazne i upiši NULL umjesto njih
    for i in range(39):
        if type(stavka[i]) == pd._libs.tslibs.nattype.NaTType or pd.isna(stavka[i]) == 1:
            stavka[i] = None
    novi_id = str(gid())
    novi = {"id":novi_id, "sif_hotela":stavka[0], "godina":stavka[1], "sif_rezervacije":stavka[2], "rbr_stavke":stavka[3], "vrijeme_kreiranje":stavka[4], "datum_kreiranja":stavka[5], "datum_od":stavka[6], "datum_do":stavka[7], "broj_dana":stavka[8], "sif_usluge":stavka[9], "status_rezervacije":stavka[10], "datum_do_potvrde_opcije":stavka[11], "sif_drzave":stavka[12], "sif_agencije":stavka[13], "tip_ro":stavka[14], "obaveza_akontacije":stavka[15], "iznos_akontacije":stavka[16], "storno":stavka[17], "vrijeme_storna":stavka[18], "datum_storna":stavka[19], "broj_osoba":stavka[20], "broj_djece":stavka[21], "broj_soba":stavka[22], "nocenja":stavka[23], "jedinice":stavka[24], "cijena_pans_usl":stavka[25], "iznos_bruto":stavka[26], "valuta":stavka[27], "tecaj":stavka[28], "lead_time_dani":stavka[29], "dat_storna_do_dat_dolaska":stavka[30], "tip_garancije":stavka[31], "postotak_akontacije":stavka[32], "mjesec":stavka[33], "godina_rezervacije":stavka[34], "vrsta_sobe":stavka[35], "kanal":stavka[36], "nacin_rezervacije":stavka[37], "vrsta_sobe_naplata":stavka[38]}
    sql_insert = """INSERT INTO rezervacija(id, sif_hotela, godina, sif_rezervacije, rbr_stavke, vrijeme_kreiranje, datum_kreiranja, datum_od, datum_do, broj_dana, sif_usluge, status_rezervacije, datum_do_potvrde_opcije, sif_drzave, sif_agencije, tip_ro, obaveza_akontacije, iznos_akontacije, storno, vrijeme_storna, datum_storna, broj_osoba, broj_djece, broj_soba, nocenja, jedinice, cijena_pans_usl, iznos_bruto, valuta, tecaj, lead_time_dani, dat_storna_do_dat_dolaska, tip_garancije, postotak_akontacije, mjesec, godina_rezervacije, vrsta_sobe, kanal, nacin_rezervacije, vrsta_sobe_naplata) VALUES (%(id)s, %(sif_hotela)s, %(godina)s, %(sif_rezervacije)s, %(rbr_stavke)s, %(vrijeme_kreiranje)s, %(datum_kreiranja)s, %(datum_od)s, %(datum_do)s, %(broj_dana)s, %(sif_usluge)s, %(status_rezervacije)s, %(datum_do_potvrde_opcije)s, %(sif_drzave)s, %(sif_agencije)s, %(tip_ro)s, %(obaveza_akontacije)s, %(iznos_akontacije)s, %(storno)s, %(vrijeme_storna)s, %(datum_storna)s, %(broj_osoba)s, %(broj_djece)s, %(broj_soba)s, %(nocenja)s, %(jedinice)s, %(cijena_pans_usl)s, %(iznos_bruto)s, %(valuta)s, %(tecaj)s, %(lead_time_dani)s, %(dat_storna_do_dat_dolaska)s, %(tip_garancije)s, %(postotak_akontacije)s, %(mjesec)s, %(godina_rezervacije)s, %(vrsta_sobe)s, %(kanal)s, %(nacin_rezervacije)s, %(vrsta_sobe_naplata)s)"""
    cur.execute(sql_insert, novi)

conn.commit()






