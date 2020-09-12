# models.py

from pony.orm import Database, PrimaryKey, Required, Set, db_session, Optional
from uuid import uuid4 as gid, UUID
import datetime as dt
import os


db = Database()

db.bind(provider='postgres', user='Kris', password='bbforlife', host='localhost', database='Mlprojekt')


class User(db.Entity):
    id = PrimaryKey(str)
    ime = Required(str)
    prezime = Required(str)
    email = Required(str)   
    mob = Required(str)
    rola = Required(str)
    lozinka = Required(str)

class Hotel(db.Entity):
    id = PrimaryKey(str)
    naziv = Required(str)
    sifra = Required(int)
    
class Soba(db.Entity):
    id = PrimaryKey(str)
    naziv = Required(str) 
    sifra = Required(str)

class Drzava(db.Entity):
    id = PrimaryKey(str)
    naziv = Required(str)

class Rezervacija(db.Entity):
    id = PrimaryKey(str)
    sif_hotela = Required(str)
    godina = Required(str)
    sif_rezervacije = Required(str)
    rbr_stavke = Required(int)
    vrijeme_kreiranje = Required(dt.time)
    datum_kreiranja = Required(dt.date)
    datum_od = Required(dt.date)
    datum_do  = Required(dt.date)
    broj_dana = Required(int)
    sif_usluge = Required(str)
    status_rezervacije  = Required(str)
    datum_do_potvrde_opcije = Optional(dt.date)
    sif_drzave = Required(str)
    sif_agencije = Required(str)
    tip_ro = Required(str)
    obaveza_akontacije = Required(str)
    iznos_akontacije = Optional(float)
    storno = Required(str)
    vrijeme_storna = Optional(dt.time)
    datum_storna = Optional(dt.date)
    broj_osoba = Required(int)
    broj_djece = Required(int)
    broj_soba = Required(int)
    nocenja = Required(int)
    jedinice = Required(int)
    cijena_pans_usl = Required(float)
    iznos_bruto = Required(float)
    valuta = Required(str)
    tecaj = Optional(float)
    lead_time_dani = Optional(int)
    dat_storna_do_dat_dolaska = Optional(int)
    tip_garancije = Optional(str)
    postotak_akontacije = Optional(float)
    mjesec = Required(int)
    godina_rezervacije = Required(int)
    vrsta_sobe = Required(str)
    kanal = Required(str)
    nacin_rezervacije = Required(str)
    vrsta_sobe_naplata = Required(str)

class RezervacijaDani(db.Entity):
    id = PrimaryKey(str)
    id_rezervacije = Required(str)
    sif_hotela = Required(str)
    godina = Required(str)
    sif_rezervacije = Required(str)
    rbr_stavke = Required(int)
    vrijeme_kreiranje = Required(dt.time)
    datum_kreiranja = Required(dt.date)
    broj_dana = Required(int)
    sif_usluge = Required(str)
    status_rezervacije  = Required(str)
    datum_do_potvrde_opcije = Optional(dt.date)
    sif_drzave = Required(str)
    sif_agencije = Required(str)
    tip_ro = Required(str)
    obaveza_akontacije = Required(str)
    iznos_akontacije = Optional(float)
    storno = Required(int)
    vrijeme_storna = Optional(dt.time)
    datum_storna = Optional(dt.date)
    broj_osoba = Required(int)
    broj_djece = Required(int)
    broj_soba = Required(int)
    nocenja = Required(int)
    jedinice = Required(int)
    cijena_pans_usl = Required(float)
    iznos_bruto = Required(float)
    valuta = Required(str)
    tecaj = Optional(float)
    lead_time_dani = Optional(int)
    dat_storna_do_dat_dolaska = Optional(int)
    tip_garancije = Optional(str)
    postotak_akontacije = Optional(float)
    mjesec = Required(int)
    godina_rezervacije = Required(int)
    vrsta_sobe = Required(str)
    kanal = Required(str)
    nacin_rezervacije = Required(str)
    vrsta_sobe_naplata = Required(str)
    dan_boravka = Required(dt.date)
    
class VremePrognoza(db.Entity):
    id = PrimaryKey(str)
    datum = Required(dt.date)
    datum_prognoze = Required(dt.date)
    temp_prosjek = Required(float)
    temp_max = Required(float)
    temp_min = Required(float)
    vidljivost = Required(float)
    smjer_vjetra_stupnjevi = Required(float)
    brzina_vjetra = Required(float)
    nalet_vjetra_brzina = Optional(float)
    relativna_vlaznost = Optional(float)
    tlak_zraka = Optional(float)
    uv_index = Optional(float)
    oblaci_pokrice = Optional(float)
    oborine_akumulirano = Optional(float)
    dubina_snijega = Optional(float)
    rosa_prosjek = Optional(float)
    prognoza = Required(str)
    preostalo_dana = Required(int)

class Predikcije(db.Entity):
    id = PrimaryKey(str)
    dan_boravka = Required(dt.date)
    sif_rezervacije = Required(str)
    vrsta_sobe = Required(str)
    kanal = Required(str)
    jedinice = Required(int)
    iznos_bruto = Required(float)
    predikcije = Required(int)
    datum_predikcije = Required(dt.date)

db.generate_mapping(check_tables=True, create_tables=True)


# test
if __name__ == "__main__":
    with db_session() as s:
        u = User(id="1", ime="Test", prezime="Test", email="test@test", mob="12345", rola="user", lozinka="123")
        b = Hotel(id="1", naziv="Croatia")
        p = Soba(id="1", naziv="Socijalna skrb", sifra="Prva")
        t = Rezervacija(id = "1", sif_hotela = "28", godina = "2017", sif_rezervacije = "2618", rbr_stavke = 1, vrijeme_kreiranje = "14:08:03", datum_kreiranja = "2017-04-22", datum_od = "2017-04-24", datum_do  = "2017-04-26", broj_dana = 2, sif_usluge = "PLO", status_rezervacije  = "F", datum_do_potvrde_opcije = "23.04.2017", sif_drzave = "HRV", sif_agencije = "5596", tip_ro = "O", obaveza_akontacije = "NE", iznos_akontacije = "0", storno = "NE", vrijeme_storna = "14:08:03", datum_storna = "2017-04-25", broj_osoba = 2, broj_djece = 1, broj_soba = 1, nocenja = 4, jedinice = 4, cijena_pans_usl = 163.8, iznos_bruto = 655.4, valuta = "EUR", tecaj = 7.45, lead_time_dani = 2, dat_storna_do_dat_dolaska = 1, tip_garancije = "D", postotak_akontacije = 0, mjesec = 4, godina_rezervacije = "2017", vrsta_sobe = "D110", kanal = "Individualci", nacin_rezervacije = "Recepcija", vrsta_sobe_naplata = "B2")
        d = Drzava(id="1", naziv="Croatija")
        v = VremePrognoza(id="1", prognoza_za_datum = "2020-03-23", datum_prognoze = dt.datetime.now(), temp_prosjek = 5.0, temp_max = 7.3, temp_min = 1.6, vidljivost = 0.0, smjer_vjetra_stupnjevi = 44, brzina_vjetra = 7.88496, nalet_vjetra_brzina = 16.8236, relativna_vlaznost = "33", tlak_zraka = 1025.64, uv_index = 4.44799, oblaci_pokrice = 22, oborine_akumulirano = 0.0, dubina_snijega = 0, rosa_prosjek = -10.2, prognoza = "Scattered clouds", preostalo_dana = 3)
        r = RezervacijaDani(id = "1", id_rezervacije = "1", sif_hotela = "28", godina = "2017", sif_rezervacije = "2618", rbr_stavke = 1, vrijeme_kreiranje = "14:08:03", datum_kreiranja = "2017-04-22", broj_dana = 2, sif_usluge = "PLO", status_rezervacije  = "F", datum_do_potvrde_opcije = "23.04.2017", sif_drzave = "HRV", sif_agencije = "5596", tip_ro = "O", obaveza_akontacije = "NE", iznos_akontacije = "0", storno = "NE", vrijeme_storna = "14:08:03", datum_storna = "2017-04-25", broj_osoba = 2, broj_djece = 1, broj_soba = 1, nocenja = 4, jedinice = 4, cijena_pans_usl = 163.8, iznos_bruto = 655.4, valuta = "EUR", tecaj = 7.45, lead_time_dani = 2, dat_storna_do_dat_dolaska = 1, tip_garancije = "D", postotak_akontacije = 0, mjesec = 4, godina_rezervacije = "2017", vrsta_sobe = "D110", kanal = "Individualci", nacin_rezervacije = "Recepcija", vrsta_sobe_naplata = "B2", dan_boravka = "2017-04-23")
        o = Predikcije(id = 1, dan_boravka = "2020-01-20", vrsta_sobe = 'A2120', kanal = 'Individualci', jedinice = 1, iznos_bruto = 1000.00, predikcije = 1, datum_predikcije = dt.datetime.now())
    
