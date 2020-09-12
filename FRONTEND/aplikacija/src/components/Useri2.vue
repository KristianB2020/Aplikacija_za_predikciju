<template>
  <div class="container">
    <div class="prazan">
    </div>
    <div class="prazan">
      <h1 class="naslov">Lista korisnika</h1>
    </div>
    <div name="MojModal" id="MojModal" ref="my-modal" class="modal fade">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Podaci odabranog korisnika:</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p class="poseban">ID:<input type="text" v-model="trenutniId"></p>
          <p class="poseban">Ime: <input type="text" v-model="trenutnoIme"></p>
          <p class="poseban">Prezime: <input type="text" v-model="trenutnoPrezime"></p>
          <p class="poseban">E-mail: <input type="text" v-model="trenutniEmail"></p>
          <p class="poseban">Mob: <input type="text" v-model="trenutniMob"></p>
          <p class="poseban">Rola: <input type="text" v-model="trenutnaRola"></p>
          <p class="poseban">Lozinka: <input type="text" v-model="trenutnaLozinka"></p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="azurirajUser()"
          data-dismiss="modal">Save changes</button>
            <button type="button" class="btn btn-danger" @click="brisiUser(trenutniId)"
             data-dismiss="modal">Delete</button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
    </div>
    <div class="table-wrapper overflow-auto">
  <div class="column">
      <div class="search-wrapper">
      <label class="input-label-new">Pretraži korisnike:  </label>
    <input class="searchbox" type="text" v-model="trazi" placeholder="Unesi...."/>
    </div>
    <div class="vertical">
    <table>
      <thead>
      <tr class='oboji'>
        <th hidden="true">ID</th>
        <th class="siri">Ime</th>
        <th class="siri">Prezime</th>
        <th class="siri">E-mail</th>
        <th class="siri">Mob</th>
        <th class="siri">Rola</th>
        <th class="siri">Lozinka</th>
        <th class="siri">Uredi</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in filtriraniUseri" :key="user.id">
        <td hidden="true">{{user.id}}</td>
        <td class="siri">{{user.ime}}</td>
        <td class="siri">{{user.prezime}}</td>
        <td class="siri">{{user.email}}</td>
        <td class="siri">{{user.mob}}</td>
        <td class="siri">{{user.rola}}</td>
        <td class="siri">{{user.lozinka}}</td>
        <td class="siri"><button class="btn btn-success"
        data-toggle="modal" data-target="#MojModal"
        @click="odabraniUser(user)"><i><font-awesome-icon :icon="['fa', 'edit']"/>  
        </i> / <i><font-awesome-icon :icon="['fa', 'trash']"/></i>
        </button>
        </td>
      </tr>
      </tbody>
    </table>
    </div>
    </div>
    <div class="column2">
    <form class="column2-new-data">
    <label class="input-label-new">Unesite podatke novog korisnika:  </label>
    </form>
    <div class="prazan2">
    </div>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="idUser" placeholder="id...NOT REQUIRED"/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="imeUser" placeholder="ime..."/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="prezimeUser" placeholder="prezime..."/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="emailUser" placeholder="email..."/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="mobUser" placeholder="mob..."/>
    </form>
    <form class="column2-new-data">
      <select class="drop" type="text" v-model="rolaUser">
         <option value="user">user</option>
         <option value="admin">admin</option>
   </select>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="lozinkaUser" placeholder="lozinka..."/>
    </form>
    <div class="prazan">
    </div>
    <form class="input-submit">
      <input type="button" class="btn btn-success" @click="createUser()" value="submit">
    </form>
    </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';

export default {
  mounted() {
    this.provjeriLocal();
  },
  data() {
    return {
      useri: [],
      idUser: null,
      imeUser: null,
      prezimeUser: null,
      emailUser: null,
      mobUser: null,
      rolaUser: null,
      lozinkaUser: null,
      trazi: '',
      trenutniId: '',
      trenutnoIme: '',
      trenutnoPrezime: '',
      trenutniEmail: '',
      trenutniMob: '',
      trenutnaRola: '',
      trenutnaLozinka: '',
    };
  },
  computed: {
    filtriraniUseri() {
      return this.useri.filter((useri) => {
        return useri.ime.toLowerCase().includes(this.trazi.toLowerCase()) ||
        useri.prezime.toLowerCase().includes(this.trazi.toLowerCase()) ||
        useri.email.toLowerCase().includes(this.trazi.toLowerCase());
      });
    },
  },

  methods: {
    getData() {
      axios
        .get('http://127.0.0.1:8080/useri')
        .then((response) => {
          const detalji = this;
          detalji.useri = response.data.data;
        });
    },
    createUser() {
      axios.post('http://127.0.0.1:8080/useri', {
        id: this.idUser,
        ime: this.imeUser,
        prezime: this.prezimeUser,
        email: this.emailUser,
        mob: this.mobUser,
        rola: this.rolaUser,
        lozinka: this.lozinkaUser,
      }).then((response) => {
        console.log(response.data);
        this.getData();
        this.idUser = '';
        this.imeUser = '';
        this.prezimeUser = '';
        this.emailUser = '';
        this.mobUser = '';
        this.rolaUser = '';
        this.lozinkaUser = '';
      })
        .catch((e) => {
          console.error(e);
        });
    },
    azurirajUser() {
      axios.put('http://127.0.0.1:8080/useri', {
        id: this.trenutniId,
        ime: this.trenutnoIme,
        prezime: this.trenutnoPrezime,
        email: this.trenutniEmail,
        mob: this.trenutniMob,
        rola: this.trenutnaRola,
        lozinka: this.trenutnaLozinka,
      }).then((response) => {
        console.log(response.data);
        this.getData();
      })
        .catch((e) => {
          console.error(e);
        });
    },
    brisiUser(tid) {
      console.log(tid);
      axios.delete('http://127.0.0.1:8080/useri', {
        params: { id: tid },
      })
        .then((response) => {
          console.log(response.data);
          this.getData();
        })
        .catch((e) => {
          console.error(e);
        });
    },
    odabraniUser(user) {
      this.trenutniId = user.id;
      this.trenutnoIme = user.ime;
      this.trenutnoPrezime = user.prezime;
      this.trenutniEmail = user.email;
      this.trenutniMob = user.mob;
      this.trenutnaRola = user.rola;
      this.trenutnaLozinka = user.lozinka;
    },
    vratiNaHome() {
      localStorage.removeItem('ulaz');
      this.$router.push({ name: 'Pocetni' });
    },
    provjeriLocal() {
      const info = localStorage.getItem('ulaz');
      if (info === 'OK') {
        this.getData();
      } else {
        this.$router.push({ name: 'LoginFail' });
      }
    },
  },
};
</script>

<style lang="scss" scoped>    /* fiksni header i scroll na tablici */

.table-wrapper{
  display: block;

  width: 100%;
  margin-left: auto;
  height: 90vh;
  overflow-y: scroll;
  margin-bottom: 20px;
}
table {
    background: #f5f5f5;
    border-collapse: separate;
    box-shadow: inset 0 1px 0 #fff;
    font-size: 12px;
    line-height: 24px;
    margin: 30px auto;
    text-align: left;
    width: 800px;
}   

th {
    border-left: 1px solid #555;
    border-right: 1px solid #777;
    border-top: 1px solid #555;
    border-bottom: 1px solid #333;
    box-shadow: inset 0 1px 0 #999;
    font-weight: bold;
    padding: 10px 15px;
    position: relative;
    text-shadow: 0 1px 0 #000;  
}

th:after {
    background: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,.08));
    content: '';
    display: block;
    height: 25%;
    left: 0;
    margin: 1px 0 0 0;
    position: absolute;
    top: 25%;
    width: 100%;
}

th:first-child {
    border-left: 1px solid #777;    
    box-shadow: inset 1px 1px 0 #999;
}

th:last-child {
    box-shadow: inset -1px 1px 0 #999;
}

td {
    border-right: 1px solid #fff;
    border-left: 1px solid #e8e8e8;
    border-top: 1px solid #fff;
    border-bottom: 1px solid #e8e8e8;
    padding: 10px 15px;
    position: relative;
    transition: all 300ms;
}

td:first-child {
    box-shadow: inset 1px 0 0 #fff;
}   

td:last-child {
    border-right: 1px solid #e8e8e8;
    box-shadow: inset -1px 0 0 #fff;
}   

tr {
    background: lightgrey; /* ovo je boja parnih redaka u tablici*/ 
    text-align: center;
}

tr:nth-child(odd) td {
    background: rgba(72, 199, 40, 0.08); /* ovo je boja parnih redaka u tablici*/ 
}

tr:last-of-type td {
    box-shadow: inset 0 -1px 0 #fff; 
}

tr:last-of-type td:first-child {
    box-shadow: inset 1px -1px 0 #fff;
}   

tr:last-of-type td:last-child {
    box-shadow: inset -1px -1px 0 #fff;
}   
tbody:hover td {
    color: transparent;
    text-shadow: 0 0 3px #aaa;
}

tbody:hover tr:hover td {
    color: #444;
    text-shadow: 0 1px 0 #fff;
}
.prazan {
  display: flex;
  justify-content: flex-start;
  margin-top:10%;
}
.prazan2 {
  height: 34px;
}
.search-wrapper {
  display: flex;
  justify-content: flex-end;
}
.searchbox {
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom-color: green($color: #0d9e00);
  font-style: italic;
  background-color: #f1f1f100;
  border-bottom-color: #000;
}

.column2-new-data{
  display: flex;
  justify-content: flex-end;

}

.new-submit {
  display: flex;
  justify-content: flex-end;
}

.input-label-new {
  display: flex;
  height: 30px;
  line-height: 35px;
  margin-right: 10px;

}

.oboji {
  background-color: rgba(66, 100, 58, 0.788); /* ovo je red sa naslovima*/
  background-image: linear-gradient(to bottom, rgb(9, 88, 2), rgb(240, 240, 241));
  color: white;
}

.input-new {
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: black;
  vertical-align: text-bottom;
  font-style: italic;
  box-shadow: 1px 1px 1px green;
  font-style: italic;
  background-color: transparent;
  text-emphasis-color: black;
}

.input-new::placeholder{
  color: darkslategrey;
  font-family: fantasy;
}
.column {
  float: left;
  width: 65%;
}

.column2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 34%;
  padding-left: 13%;
 
}
.drop{
  width: 180px;
  background-color: transparent;
}

footer{
  margin-top:30px!important;
}
.poseban {
  font-size: 20px;
  color: darkslategray;
  padding: 0.1cm;
  margin-right: 1.5cm;
}
.naslov {
  font-family: fantasy;
  font-style: italic;
}
@media (max-width:1300px){
 .table-wrapper{
    display:block;
    margin-left:10%;
    margin-bottom: 0; 
  }
    .column{
    width: 100%;
  }
  .column2{
    width: 100%;
  }
}


@media (max-width:768px) {
 
  .new-submit{
    justify-content: center;
  }
  .prazan{
    justify-content: center;
  }
  .column2{
    width: 100%;
    float: none;
    margin-right: 10px;
  }
  .input-label-new{
    justify-content: center;
  }

  
}


</style>
