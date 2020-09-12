<template>
    <div class="container">
        <div class="jumbotron mt-5 boja">
            <div class="col-sm-8 mx-auto">
                <h1 class="text-center boja">PODACI VAŠEG PROFILA</h1>
            </div>
            <table class="table col-md-6 mx-auto">
                <tbody>
                    <tr>
                        <td class="boja">Ime</td>
                        <td><input class="sjena" type="text" v-model="u_ime"></td>
                    </tr>
                    <tr>
                        <td class="boja">Prezime</td>
                        <td><input class="sjena" type="text" v-model="u_prezime"></td>
                    </tr>
                    <tr>
                        <td class="boja">E-Pošta</td>
                        <td><input class="sjena" type="text" v-model="u_email"></td>
                    </tr>
                    <tr>
                        <td class="boja">Broj mobitela</td>
                        <td><input class="sjena" type="text" v-model="u_mob"></td>
                    </tr>
                    <tr>
                        <td class="boja">Lozinka</td>
                        <td><input class="sjena" type="text" v-model="u_loz"></td>
                    </tr>
                     <tr>
                        <td class="boja centar"><button class="btn btn-primary"
                        @click.prevent="azurirajUser()">
                            SPREMI NOVE PODATKE</button></td>
                    </tr>
                    <tr></tr>
                    <tr class="sakrij" v-show="upozorenje">
                        <p class="crveno">PODACI PROMIJENJENI !!</p>
                        <p class="crveno">MOLIMO VAS DA OSVJEŽITE STRANICU TE SE PONOVNO ULOGIRATE
                            KAKO BISTE MOGLI NASTAVITI KORISTITI APLIKACIJU</p>
                        <td class="crveno centar"><button class="btn btn-dark"
                        @click.prevent="prijava()">
                            PRIJAVA</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import VueJwtDecode from 'vue-jwt-decode';

export default {
  name: 'DetaljiUser',
  mounted() {
    this.dajPodatke();
  },
  data() {
    return {
      useri: [],
      u_id: '',
      u_ime: '',
      u_prezime: '',
      u_email: '',
      u_mob: '',
      u_loz: '',
      u_rola: '',
      upozorenje: false,
    };
  },
  methods: {
    dajPodatke() {
      const token = localStorage.detalji;
      const decoded = VueJwtDecode.decode(token);
      this.u_ime = decoded.ime;
      this.u_prezime = decoded.prezime;
      this.u_email = decoded.email;
      this.u_mob = decoded.mob;
      this.u_loz = decoded.lozinka;
    },
    azurirajUser() {
      const token = localStorage.detalji;
      const decoded = VueJwtDecode.decode(token);
      this.u_id = decoded.id;
      this.u_rola = decoded.rola;
      axios.put('http://127.0.0.1:8080/useri', {
        id: this.u_id,
        ime: this.u_ime,
        prezime: this.u_prezime,
        email: this.u_email,
        mob: this.u_mob,
        rola: this.u_rola,
        lozinka: this.u_loz,
      }).then((response) => {
        console.log(response.data);
        this.upozorenje = true;
        localStorage.clear();
      })
        .catch((e) => {
          console.error(e);
        });
    },
    prijava() {
      this.$router.push({ name: 'Pocetni' });
    },
  },
};
</script>

<style lang="scss" scoped>
.prazan {
  height: 50px;
  display: flex;
  justify-content: flex-start;
}

.column1 {
    width: 50%;
}

.column2 {
    width: 50%;
}

.nova {
    width: 300px;
}

.inputnova {
    width: 400px;
    background-color: #F1F1F1;
}

.boja {
    color: rgb(16, 143, 47);
    background-color: transparent;
}

.sjena {
    box-shadow: 2px 5px 9px green;
}

.centar {
    justify-content: center;
}

.crveno {
    color: red;
}
</style>
