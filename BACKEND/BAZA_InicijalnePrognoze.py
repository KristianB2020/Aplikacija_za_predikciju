import pandas as pd
import psycopg2
from uuid import uuid4 as gid

#pročitaj iz datoteke
data = pd.read_csv("./Excelice/Prognoze_povijesni_podaci.csv", sep = None, header=0, engine='python')
#spremi u listu i DB
lista = data.values.tolist()

print(lista[0])
conn = psycopg2.connect("dbname=Mlprojekt user=Kris password=bbforlife host=localhost")
cur = conn.cursor()

for stavka in lista:
    for i in range(1,19):
        if type(stavka[i]) == pd._libs.tslibs.nattype.NaTType or pd.isna(stavka[i]) == 1:
            stavka[i] = None
    novi_id = str(gid())
    novi = {"id":novi_id, "datum":stavka[1], "datum_prognoze":stavka[2], "temp_prosjek":stavka[3], "temp_max":stavka[4], "temp_min":stavka[5], "vidljivost":stavka[6], "smjer_vjetra_stupnjevi":stavka[7], "brzina_vjetra":stavka[8], "nalet_vjetra_brzina":stavka[9], "relativna_vlaznost":stavka[10], "tlak_zraka":stavka[11], "uv_index":stavka[12], "oblaci_pokrice":stavka[13], "oborine_akumulirano":stavka[14], "dubina_snijega":stavka[15], "rosa_prosjek":stavka[16], "prognoza":stavka[17], "preostalo_dana":stavka[18]}
    cur.execute("""INSERT INTO vremeprognoza3(id, datum, datum_prognoze, temp_prosjek, temp_max, temp_min, vidljivost, smjer_vjetra_stupnjevi, brzina_vjetra, nalet_vjetra_brzina, relativna_vlaznost, tlak_zraka, uv_index, oblaci_pokrice, oborine_akumulirano, dubina_snijega, rosa_prosjek, prognoza, preostalo_dana) VALUES (%(id)s, %(datum)s, %(datum_prognoze)s, %(temp_prosjek)s, %(temp_max)s, %(temp_min)s, %(vidljivost)s, %(smjer_vjetra_stupnjevi)s, %(brzina_vjetra)s, %(nalet_vjetra_brzina)s, %(relativna_vlaznost)s, %(tlak_zraka)s, %(uv_index)s, %(oblaci_pokrice)s, %(oborine_akumulirano)s, %(dubina_snijega)s, %(rosa_prosjek)s, %(prognoza)s, %(preostalo_dana)s)""", novi)

conn.commit()
print("Prognoza učitana")




