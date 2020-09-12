# from Funkcije import *
from Funkcije_FINAL import *


def napravi_predikcije():
    napravi_predikcije_za_danas()
    napravi_predikcije_za_ostale_dane()

#TIMER
schedule.every().day.at("06:00").do(napravi_predikcije)
#schedule.every(10).seconds.do(napravi_predikcije)
while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    napravi_predikcije()
           
