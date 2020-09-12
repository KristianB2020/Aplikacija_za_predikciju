<template>
  <div class="container">
    <div class="prazan">
    </div>
    <div class="prazan">
      <h1>Lista korisnika</h1>
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
          <p>ID: <input type="text" v-model="trenutniId"></p>
          <p>Ime: <input type="text" v-model="trenutnoIme"></p>
          <p>Prezime: <input type="text" v-model="trenutnoPrezime"></p>
          <p>E-mail: <input type="text" v-model="trenutniEmail"></p>
          <p>Mob: <input type="text" v-model="trenutniMob"></p>
          <p>Rola: <input type="text" v-model="trenutnaRola"></p>
          <p>Lozinka: <input type="text" v-model="trenutnaLozinka"></p>
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
    <table id="verticaltable" class="table table-striped table-hover"
      cellspacing="0" width="100%">
      <thead>
      <tr>
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

.verticaltable {
  border: 2px solid #474b49;
  border-radius: 3px;
  border-color: #074b01;
  height: auto;
}

.verticaltable table {
  margin-bottom: 20px;
  border-collapse: collapse;
  display: table;
  table-layout: fixed; /* This will ensure the cells within the table will keep there width. */
  width: 100%;
}

thead {
  height: 50px;
  text-align: center;
  color: white;
}

tbody {    
  width: 100%;
}

#verticaltable thead {
  width: 100%;
}
#verticaltable th, tr {
  opacity: .8;
  color: #074b01;
}

#verticaltable th {
  background: linear-gradient(to bottom right, #7FD625, #009345);
  color: #fff;
}
.prazan {
  display: flex;
  justify-content: flex-start;
  margin-top:10%;
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
  background-color: #F1F1F1;
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
  background-color: #F1F1F1;
}

.input-new {
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: green($color: #0d9e00);
  vertical-align: text-bottom;
  font-style: italic;
  background-color: #F1F1F1;
   box-shadow: 2px 5px 9px green;
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
}

footer{
  margin-top:30px!important;
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
