from flask import Flask, Response, jsonify, request, make_response
from Domain import *
from flask_cors import CORS
import datetime
import json
import jwt
from urllib.parse import urlparse


app = Flask(__name__)

CORS(app)
#-----------------------------------------------------------USERI-------------------------------------------------------------------------------
@app.route("/useri", methods=["GET"])
def handle_useri():
    useri = Useri.listaj()
    print(useri)
    return jsonify({"data": useri})

@app.route("/useri", methods=["POST"])
def handle_useri_dodaj():
    status, greske = Useri.dodaj(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route('/useri', methods = ['PUT'])
def azuriraj_usera():
    status, greske = Useri.user_update(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route('/useri', methods = ['DELETE'])
def brisi_usera():
    status, greske = Useri.user_brisi(request.args.get('id'))
    if status:
        return Response(status=204)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route('/useri/login', methods = ['POST'])
def ulogiraj_usera():
    status, greske = Useri.provjeri_login(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route('/admin/login', methods = ['POST'])
def ulogiraj_admina():
    status, greske = Useri.provjeri_login_admin(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/useri/ulogiran", methods=["POST"])
def trenutni_user():
    trenUser = Useri.daj_trenutnog(request.get_json())
    return trenUser

# ---------------------------------------------------PREDIKCIJE----------------------------------------------------------

@app.route("/predikcije", methods=["GET"])
def handle_predikcije():
    outputi = Outputi.ucitaj_predikcije()
    return jsonify({"data": outputi})

@app.route("/jedinice", methods=["GET"])
def handle_jedinice():
    outputi = Outputi.ucitaj_jedinice()
    return jsonify({"data": outputi})

@app.route("/iznosi", methods=["GET"])
def handle_iznose():
    outputi = Outputi.ucitaj_iznos()
    return jsonify({"data": outputi})

#-----------------------------------------------------------DRZAVE-------------------------------------------------------------------------------

@app.route("/drzave", methods=["GET"])
def handle_drzave():
    drzave = Drzave.listaj()
    return jsonify({"data": drzave})

@app.route("/drzave", methods=["POST"])
def handle_drzave_dodaj():
    status, greske = Drzave.dodaj(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/drzave", methods = ['PUT'])
def handle_azuriraj_drzavu():
    status, greske = Drzave.drzava_update(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/drzave", methods = ['DELETE'])
def handle_brisi_drzavu():
    status, greske = Drzave.drzava_brisi(request.args.get('id'))
    if status:
        return Response(status=204)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

#-----------------------------------------------------------SOBE-------------------------------------------------------------------------------

@app.route("/sobe", methods=["GET"])
def handle_sobe():
    sobe = Sobe.listaj()
    return jsonify({"data": sobe})

@app.route("/sobe", methods=["POST"])
def handle_sobe_dodaj():
    status, greske = Sobe.dodaj(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/sobe", methods = ['PUT'])
def handle_azuriraj_sobu():
    status, greske = Sobe.soba_update(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/sobe", methods = ['DELETE'])
def handle_brisi_sobu():
    status, greske = Sobe.soba_brisi(request.args.get('id'))
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

#-----------------------------------------------------------HOTELI-------------------------------------------------------------------------------

@app.route("/hoteli", methods=["GET"])
def handle_hoteli():
    hoteli = Hoteli.listaj()
    return jsonify({"data": hoteli})

@app.route("/hoteli", methods=["POST"])
def handle_hoteli_dodaj():
    status, greske = Hoteli.dodaj(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/hoteli", methods = ['PUT'])
def handle_azuriraj_hotel():
    status, greske = Hoteli.hotel_update(request.get_json())
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r

@app.route("/hoteli", methods = ['DELETE'])
def handle_brisi_hotel():
    status, greske = Hoteli.hotel_brisi(request.args.get('id'))
    if status:
        return Response(status=201)
    else:
        r = Response(status=500)
        r.set_data(greske)
        return r


#-----------------------------------------------------------MAIN-------------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)

