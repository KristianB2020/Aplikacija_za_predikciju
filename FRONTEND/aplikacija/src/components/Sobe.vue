<template>
  <div class="container">
     <div class="prazan">
      <h1 class="naslov">Lista soba</h1>
    </div>
    <div name="MojModal" id="MojModal" ref="my-modal" class="modal fade">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Podaci odabrane sobe:</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p>ID: <input type="text" v-model="trenutniId"></p>
          <p>Naziv: <input type="text" v-model="trenutniNaziv"></p>
          <p>Naziv: <input type="text" v-model="trenutnaSifra"></p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="azurirajSoba()"
          data-dismiss="modal">Save changes</button>
            <button type="button" class="btn btn-danger" @click="brisiSoba(trenutniId)"
             data-dismiss="modal">Delete</button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
    </div>
    <div class="table-wrapper overflow-auto">
    <div class="column">
      <div class="search-wrapper">
      <label class="input-label-new">Pretraži sobe:  </label>
    <input class="searchbox" type="text" v-model="trazi" placeholder="Unesi naziv sobe...."/>
    </div>
    <div class="vertical">
    <table>
      <thead>
      <tr class='oboji'>
        <th scope="row">Id</th>
        <th scope="row">Naziv sobe</th>
        <th scope="row">Sifra sobe</th>
        <th scope="row">Uredi</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="soba in filtriraneSobe" :key="soba.id">
        <td>{{soba.id}}</td>
        <td>{{soba.naziv}}</td>
        <td>{{soba.sifra}}</td>
        <td><button class="btn btn-success"
        data-toggle="modal" data-target="#MojModal"
        @click="odabranaSoba(soba)"><i><font-awesome-icon :icon="['fa', 'edit']"/>  
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
    <label class="input-label-new">Unesite podatke nove sobe:  </label>
    </form>
    <div class="prazan2"></div>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="idSoba" placeholder="id..."/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="NazivSoba" placeholder="naziv..."/>
    </form>
    <form class="column2-new-data">
      <input class="input-new" type="text" v-model="SifraSoba" placeholder="sifra..."/>
    </form>
    <div class="prazan">
    </div>
    <form class="input-submit">
      <input type="button" class="btn btn-success" @click="createSoba()" value="submit">
    </form>
    </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */ 
import axios from 'axios';

export default {
  name: 'Tablica',
  mounted() {
    this.provjeriLocal();
  },
  data() {
    return {
      sobe: [],
      idSoba: null,
      NazivSoba: null,
      SifraSoba: null,
      trazi: '',
      trenutniId: '',
      trenutniNaziv: '',
      trenutnaSifra: '',
    };
  },
  computed: {
    filtriraneSobe() {
      return this.sobe.filter((sobe) => {
        console.log('Sobe');
        return sobe.naziv.toLowerCase().includes(this.trazi.toLowerCase());
      });
    },
  },

  methods: {
    getData() {
      axios
        .get('http://127.0.0.1:8080/sobe')
        .then((response) => {
          console.log(response.data);
          const detalji = this;
          detalji.sobe = response.data.data;
        });
    },
    createSoba() {
      axios.post('http://127.0.0.1:8080/sobe', {
        id: this.idSoba,
        naziv: this.NazivSoba,
        sifra: this.SifraSoba,
      }).then((response) => {
        console.log(response.data);
        this.getData();
        this.NazivSoba = '';
        this.SifraSoba = '';
      })
        .catch((e) => {
          console.error(e);
        });
    },
    azurirajSoba() {
      axios.put('http://127.0.0.1:8080/sobe', {
        id: this.trenutniId,
        naziv: this.trenutniNaziv,
        sifra: this.trenutnaSifra,
      }).then((response) => {
        console.log(response.data);
        this.getData();
      })
        .catch((e) => {
          console.error(e);
        });
    },
    brisiSoba(tid) {
      console.log(tid);
      axios.delete('http://127.0.0.1:8080/sobe', {
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
    odabranaSoba(soba) {
      this.trenutniId = soba.id;
      this.trenutniNaziv = soba.naziv;
      this.trenutnaSifra = soba.sifra;
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
  display: flex;
  justify-content: center;
  width: 100%;
  margin-left: auto;
  height: 90vh;

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
  background-color: transparent;
}
.prazan2 {
  height: 72px;
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
  background-color: transparent;
}

.input-new {
  border-top: none;
  border-right: none;
  border-left: none;
  border-bottom: green($color: #0d9e00);
  vertical-align: text-bottom;
  font-style: italic;
  background-color: transparent;
   box-shadow: 2px 2px 6px green;
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
 
}
footer{
  margin-top:30px!important;
}
.naslov {
  font-family: fantasy;
  font-style: italic;
}
.oboji {
  background-color: rgba(66, 100, 58, 0.788); /* ovo je red sa naslovima*/
  background-image: linear-gradient(to bottom, rgb(9, 88, 2), rgb(240, 240, 241));
  color: white;
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
