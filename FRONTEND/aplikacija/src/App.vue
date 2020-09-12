<template>
  <div id="app">
    <app-header v-if="provjeriPocetni()"></app-header>
    <app-dashboard v-if="provjeriPocetni()"></app-dashboard>
    <div class="content-wrapper2">
    <router-view></router-view>
    </div>
    <app-footer v-if="provjeriPocetni()"></app-footer>
  </div>
</template>

<script>
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './components/Dashboard';

export default {
  name: 'App',
  data() {
    return {
      signUp: false,
      email: '',
      lozinka: '',
    };
  },
  methods: {
    provjeriPocetni() { /* provjeri dal je login screen pa ne renderaj dashboard */
      if (this.$route.path === '/' || this.$route.path === '/loginfail') {
        return false;
      } return true;
    },
    provjeriPocetniUser() { /* ne renderaj komponente za admina */
      if (this.$route.path === '/TicketAdmin' || this.$route.path === '/'
         || this.$route.path === '/sobe' || this.$route.path === '/drzave'
         || this.$route.path === '/useri2' || this.$route.path === '/jedinice'
         || this.$route.path === '/iznosi' || this.$route.path === '/loginfail'
         || this.$route.path === '/predikcije' || this.$route.path === '/hoteli'
         || this.$route.path === '/homeadmin') {
        return false;
      } return true;
    },
  },
  components: {
    'app-footer': Footer,
    'app-dashboard': Dashboard,
    'app-header': Header,
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');
html, body {
  height: 100%;
  margin: 0;
  background-color: #F1F1F1;
}
#app {
  font-family: 'Roboto Condensed', 'Helvetica', sans-serif;
  font-size: 14px;
  font-weight: 300;
  text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #0f8500;
  margin-top: 60px;
  font-size: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
}
.content-wrapper2 {
  flex-grow: 1;
  background-image: url('./assets/Pozadina2.jpg');
  background-size: 150%;
}
#app img {
  width: 50%;
}
#li {
  color: #259345;
}
body {
  font-family: Helvetica Neue, Arial, sans-serif;
  font-size: 14px;
  color: #444;
}
/*table {
  border: hidden;
  border-radius: 2px;
}
th {
  color: rgba(255,255,255,0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
th, td {
  min-width: 120px;
  padding: 10px 20px;
}
th.active {
  color: rgb(133, 131, 131);
}
th.active .arrow {
  opacity: 1;
}*/
footer {
  background: rgb(78, 78, 78);
  background-image: linear-gradient(to right, rgb(47, 107, 36), black);
  color: #ffffff;
  padding: 15px 0px;
  flex-grow: 0;
  opacity: 100%;
  z-index: 1000;
}
.empty {
  height: 50px;
}
.router-view {
  left: 70px;
}
</style>
