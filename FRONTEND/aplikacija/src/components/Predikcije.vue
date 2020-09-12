<template>
  <div class="container">
    <div class="prazan">
    </div>
    <div class="prazan">
      <h1 class='naslov'>Predviđeni broj otkazanih rezervacija</h1>
    </div>
    <div class="table-wrapper overflow-auto">
  <div class="column">
    <div class="vertical">
      <table>
        <thead>
          <tr class='oboji'>
            <th hidden="true">Id</th>
            <th class="siri">Datum</th>
            <th class="siri">Deluxe triple soba</th>
            <th class="siri">Deluxe double soba</th>
            <th class="siri">Sea view soba</th>
            <th class="siri">Park view soba</th>
            <th class="siri">Osnovna soba</th>
            <th class="siri">Lux apartman</th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="predikcija in predikcije" :key="predikcija.id">
              <td hidden="true">{{predikcija.id}}</td>
              <td class="siri2"><b>{{predikcija.datum}}</b></td>
              <td class="siri">{{predikcija.A21}}</td>
              <td class="siri">{{predikcija.A2}}</td>
              <td class="siri">{{predikcija.B2}}</td>
              <td class="siri">{{predikcija.E1}}</td>
              <td class="siri">{{predikcija.D1}}</td>
              <td class="siri">{{predikcija.HA}}</td>
            </tr>
        </tbody>
      </table>
    </div>
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
      predikcije: [],
      trazi: '',
    };
  },

  methods: {
    getData() {
      axios
        .get('http://127.0.0.1:8080/predikcije')
        .then((response) => {
          const detalji = this;
          detalji.predikcije = response.data.data;
        });
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
    background: red, linear-gradient(#777, #444);
    border-left: 1px solid #555;
    border-right: 1px solid #777;
    border-top: 1px solid #555;
    border-bottom: 1px solid #333;
    box-shadow: inset 0 1px 0 #999;
    color: #fff;
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
.siri2 {
  color: rgba(32, 77, 15, 0.836);
  font-weight: bold;
  font-style: italic;
  text-shadow: 1px 1px rgb(211, 221, 221);
}
.naslov {
  font-size: 25px;
  font-family: fantasy;
  font-style: italic;
  color: rgba(11, 59, 23, 0.856);
}
.oboji {
  background-color: rgba(66, 100, 58, 0.788); /* ovo je red sa naslovima*/
  background-image: linear-gradient(to bottom, rgb(9, 88, 2), rgb(240, 240, 241));
}


</style>
