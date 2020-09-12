from Models import *
from pony.orm import *
import psycopg2
from uuid import uuid4 as gid, UUID
from datetime import datetime, date, time, timedelta
import time
import json
import schedule
import jwt


class Useri:
    @db_session()
    def listaj():
        q = select(s for s in User)
        data = [x.to_dict() for x in q]
        return data

    @db_session
    def dodaj(s):
        try:
            s["id"] = str(gid())
            s = User(**s)
            return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def user_update(data):
        try:
            User[data['id']].ime = data['ime']
            User[data['id']].prezime = data['prezime']
            User[data['id']].email = data['email']
            User[data['id']].mob = data['mob']
            User[data['id']].rola = data['rola']
            User[data['id']].lozinka = data['lozinka']
            return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def user_brisi(data):
        try:
            User[data].delete()
            return True, None
        except Exception as e:
            return False, str(e)
    
    #METODA ZA PROVJERU UPISANE EMAIL ADRESE I LOZINKE U BAZI
    @db_session
    def provjeri_login(data):
        userMail = data['data']['email']
        userPass = data['data']['pass']
        try:
            q = select(s for s in User if s.email == userMail and s.lozinka == userPass)
            Userdata = [x.to_dict() for x in q]
            return Userdata, False
        except Exception as e:
            return False, str(e)     

    #METODA ZA PROVJERU ROLE ADMIN
    @db_session
    def provjeri_login_admin(data):
        userMail = data['data']['email']
        userPass = data['data']['pass']
        try:
            q = select(s for s in User if s.email == userMail and s.lozinka == userPass and s.rola == 'admin')
            Userdata = [x.to_dict() for x in q]
            return Userdata, False
        except Exception as e:
            return False, str(e)

    #METODA ZA VRAĆANJE PODATAKA TRENUTNOG USERA IZ BAZE NA TEMELJU EMAIL ADRESE I LOZINKE
    @db_session
    def daj_trenutnog(data):
        key = 'ovo je tajni kljuc za projekt iz ML-a'
        userMail = data['data']['email']
        userPass = data['data']['pass']
        q = select(s for s in User if s.email == userMail and s.lozinka == userPass)
        rez = [x.to_dict() for x in q]
        token = jwt.encode({'id':rez[0]['id'], 'ime':rez[0]['ime'], 'prezime':rez[0]['prezime'], 
                            'email':rez[0]['email'], 'mob':rez[0]['mob'], 'rola':rez[0]['rola'], 'lozinka':rez[0]['lozinka']},
                             key, algorithm='HS256')
        return token

#---------------------------------------------------------------------DRZAVE------------------------------------------------------------------
class Drzave:
    @db_session()
    def listaj():
        # ORM upit
        q = select(s for s in Drzava)
        data = [x.to_dict() for x in q]
        return data

    @db_session
    def dodaj(s):
        try:
            if id not in s:                          
                s["id"] = str(gid())                
                s = Drzava(**s)                       
                return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def drzava_update(data):
        try:
            Drzava[data['id']].naziv = data['naziv']
            return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def drzava_brisi(data):
        try:
            Drzava[data].delete()
            return True, None
        except Exception as e:
            return False, str(e)

#---------------------------------------------------------------------SOBE------------------------------------------------------------------
class Sobe:
    @db_session()
    def listaj():
        q = select(s for s in Soba)
        data = [x.to_dict() for x in q]
        return data

    @db_session
    def dodaj(s):
        try:
            if id not in s:                          
                s["id"] = str(gid())                
                s = Soba(**s)                       
                return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def soba_update(data):
        try:
            Soba[data['id']].naziv = data['naziv']
            Soba[data['id']].sifra = data['sifra']
            return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def soba_brisi(data):
        try:
            Soba[data].delete()
            return True, None
        except Exception as e:
            return False, str(e)

#---------------------------------------------------------------------HOTELI------------------------------------------------------------------
class Hoteli:
    @db_session()
    def listaj():
        q = select(s for s in Hotel)
        data = [x.to_dict() for x in q]
        return data

    @db_session
    def dodaj(s):
        try:
            if id not in s:                          
                s["id"] = str(gid())                
                s = Hotel(**s)                       
                return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def hotel_update(data):
        try:
            Hotel[data['id']].naziv = data['naziv']
            Hotel[data['id']].sifra = data['sifra']
            return True, None
        except Exception as e:
            return False, str(e)

    @db_session
    def hotel_brisi(data):
        try:
            Hotel[data].delete()
            return True, None
        except Exception as e:
            return False, str(e)

# ---------------------------------------------------------------------PROGNOZE---------------------------------------------------------

class VremePrognoze:
    @db_session()
    def listaj_iz_baze():
        q = select(s for s in VremePrognoza)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_iz_baze_inicijalno():
        datum = datetime.strptime('2020-01-01', '%Y-%m-%d')
        q = select(s for s in VremePrognoza if s.datum < datum and s.preostalo_dana == 1)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_prog_za_datum(datum):
        q = select(s for s in VremePrognoza if s.datum == datum)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_prog_za_danas():
        danas = dt.date.today()
        q = select(s for s in VremePrognoza if s.datum == danas)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_prognoze_1i3i7():
        q = select(s for s in VremePrognoza if s.preostalo_dana == 1 or s.preostalo_dana == 3 or s.preostalo_dana == 7 )
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_iz_baze_trening():
        datum = datetime.strptime('2020-01-01', '%Y-%m-%d')
        q = select(s for s in VremePrognoza if s.datum < datum)
        data = [x.to_dict() for x in q]
        return data

# ---------------------------------------------------------------------REZERVACIJE---------------------------------------------------------

class Rezervacije:
    #UVEZI REZERVACIJE OD JUČER
    @db_session()
    def listaj_po_datumu_kreiranja_zadnja24h_sve():
        jucer = datetime.now() - timedelta(days=1)
        q = select(s for s in Rezervacija if s.datum_kreiranja == dt.datetime.strptime(jucer.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_po_datumu_kreiranja_zadnja24h_samo_aktivne():
        jucer = datetime.now() - timedelta(days=400)
        q = select(s for s in Rezervacija if s.datum_kreiranja == dt.datetime.strptime(jucer.strftime('%Y-%m-%d'), '%Y-%m-%d') and s.storno == "NE")
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj():
        q = select(s for s in Rezervacija)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_po_godini():
        q = select(s for s in Rezervacija if s.godina == "2020")
        data = [x.to_dict() for x in q]
        return data

# ---------------------------------------------------------------------REZERVACIJE-DANI---------------------------------------------------------

class RezervacijeDani:
    @db_session()
    def listaj():
        q = select(s for s in RezervacijaDani)
        data = [x.to_dict() for x in q]
        return data
    
    # listaj rezervacije stornirane određen broj dana prije dolaska
    @db_session()
    def listaj_storno(dana):
        q = select(s.dan_boravka for s in RezervacijaDani if s.dat_storna_do_dat_dolaska == dana)
        data = list(q)
        return data

    # listaj storno za rezervacije za treniranje modela
    @db_session()
    def listaj_trening():
        datum = datetime.strptime('2019-12-15', '%Y-%m-%d')
        q = select(s for s in RezervacijaDani if s.dan_boravka <= datum)
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_sav_storno():
        q = select(s.dan_boravka for s in RezervacijaDani if between(s.dat_storna_do_dat_dolaska, 0, 8))
        data = list(q)
        return data

    @db_session()
    def listaj_rez_za_danas():
        danas = dt.date.today()
        q = select(s for s in RezervacijaDani if s.dan_boravka == danas and s.storno == 0 and (s.status_rezervacije == 'O' or s.status_rezervacije == 'F' ))
        data = [x.to_dict() for x in q]
        return data

    @db_session()
    def listaj_rez_za_datum(datum):
        q = select(s for s in RezervacijaDani if s.dan_boravka == datum and s.storno == 0 and (s.status_rezervacije == 'O' or s.status_rezervacije == 'F' ))
        data = [x.to_dict() for x in q]
        return data


# ---------------------------------------------------------------------PREDIKCIJE---------------------------------------------------------

class Outputi:
    def ucitaj_predikcije():
        listaPredikcija = []
        start = date.today()
        conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
        for i in range(0,8):
            cur = conn.cursor()
            datum = (start + timedelta(days=i)).strftime('%Y-%m-%d')
            cur.execute("""select sum (predikcije) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(A21)s 
                        and datum_predikcije = %(datump)s
                        union all
                        select sum (predikcije) from predikcije where dan_boravka = %(datum)s and (vrsta_sobe = %(A2)s or vrsta_sobe like %(A2M)s 
                        or vrsta_sobe like %(A220)s  or vrsta_sobe like %(A210)s) and datum_predikcije = %(datump)s 
                        union all
                        select sum (predikcije) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(B2)s 
                        and datum_predikcije = %(datump)s
                        union all
                        select sum (predikcije) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(E1)s 
                        and datum_predikcije = %(datump)s
                        union all
                        select sum (predikcije) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(D1)s 
                        and datum_predikcije = %(datump)s
                        union all
                        select sum (predikcije) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(HA)s 
                        and datum_predikcije = %(datump)s""", 
                        {'datum': datum, 'datump': start.strftime('%Y-%m-%d'), 'A21':'A21%', 'A2':'A2%', 'A2M':'A2M%', 'A220':'A220%', 'A210':'A210%', 
                        'B2':'B2%', 'E1':'E1%','D1':'D1%','HA':'HA%',})
            podaci = cur.fetchall()
            # pretvori None u nulu
            jed_list = [x[0] for x in podaci]
            jed_list = [0 if v is None else v for v in jed_list]
            zapis = {'datum':datum, 'A21':jed_list[0], 'A2':jed_list[1], 'B2':jed_list[2], 'E1':jed_list[3], 'D1':jed_list[4], 'HA':jed_list[5]}
            print(zapis)
            listaPredikcija.append(zapis)
        cur.close()
        conn.close ()
        for zapis in listaPredikcija:
            zapis['id'] = str(gid())
        return listaPredikcija

    def ucitaj_jedinice():
        listaJedinice = []
        start = date.today()
        conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
        cur = conn.cursor()
        for i in range(0,8):
            datum = (start + timedelta(days=i)).strftime('%Y-%m-%d')
            cur.execute("""select sum (jedinice) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(A21)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (jedinice) from predikcije where dan_boravka = %(datum)s and (vrsta_sobe like %(A2M20)s or vrsta_sobe like %(A2M)s or vrsta_sobe like %(A220)s  or vrsta_sobe like %(A210)s) and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (jedinice) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(B2)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (jedinice) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(E1)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (jedinice) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(D1)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (jedinice) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(HA)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s""", {'datum': datum, 'datump': start.strftime('%Y-%m-%d'), 'otkazana': 1, 'A21':'A21%', 'A2M20':'A2M20%', 'A2M':'A2M%', 'A220':'A220%', 'A210':'A210%', 'B2':'B2%', 'E1':'E1%','D1':'D1%','HA':'HA%',})
            podaci = cur.fetchall()
            # pretvori None u nulu
            jed_list = [x[0] for x in podaci]
            jed_list = [0 if v is None else v for v in jed_list]
            zapis = {'datum':datum, 'A21':jed_list[0], 'A2':jed_list[1], 'B2':jed_list[2], 'E1':jed_list[3], 'D1':jed_list[4], 'HA':jed_list[5]}
            listaJedinice.append(zapis)
        cur.close()
        conn.close()
        for zapis in listaJedinice:
            zapis['id'] = str(gid())
        return listaJedinice

    def ucitaj_iznos():
        listaIznosa = []
        start = date.today()
        conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
        for i in range(0,8):
            cur = conn.cursor()
            datum = (start + timedelta(days=i)).strftime('%Y-%m-%d')
            cur.execute("""select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(A21)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and (vrsta_sobe = %(A2)s or vrsta_sobe like %(A2M)s or vrsta_sobe like %(A220)s  or vrsta_sobe like %(A210)s) and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(B2)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(E1)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(D1)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s
                        union all
                        select sum (iznos_bruto) from predikcije where dan_boravka = %(datum)s and vrsta_sobe like %(HA)s and datum_predikcije = %(datump)s and predikcije = %(otkazana)s""", {'datum': datum, 'datump': start.strftime('%Y-%m-%d'), 'otkazana': 1 , 'A21':'A21%', 'A2':'A2%', 'A2M':'A2M%', 'A220':'A220%', 'A210':'A210%', 'B2':'B2%', 'E1':'E1%','D1':'D1%','HA':'HA%',})
            podaci = cur.fetchall()
            # pretvori None u nulu
            jed_list = [x[0] for x in podaci]
            jed_list = [0 if v is None else v for v in jed_list]
            zapis = {'datum':datum, 'A21':jed_list[0], 'A2':jed_list[1], 'B2':jed_list[2], 'E1':jed_list[3], 'D1':jed_list[4], 'HA':jed_list[5]}
            print(zapis)
            listaIznosa.append(zapis)
        cur.close()
        conn.close()
        for zapis in listaIznosa:
            zapis['id'] = str(gid())
        return listaIznosa

    @db_session()
    def listaj_pred_za_datum(datum):
        q = select(s for s in Predikcije if s.dan_boravka == datum)
        data = [x.to_dict() for x in q]
        return data

