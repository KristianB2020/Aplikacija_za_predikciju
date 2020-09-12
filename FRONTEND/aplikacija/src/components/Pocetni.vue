<template>
      <article>
        <div class="row">
        <div class="container" :class="{'sign-up-active' : signUp}">
        <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-left">
            <h2>Dobrodošli natrag!</h2>
            <p>Ulogirajte se svojim podacima</p>
            <button class="invert" id="signIn" @click="signUp = !signUp">Prijava</button>
          </div>
          <div class="overlay-right">
            <h2>Dobrodošli na FORECAST!</h2>
            <p>Za nove korisnike</p>
            <button class="invert" id="signUp" @click="signUp = !signUp">Registracija</button>
          </div>
        </div>
      </div>
      <form class="sign-up" action="#">
        <h2>Registriraj se</h2>
        <div>Unesite adresu e-pošte za registraciju</div>
        <input type="text" v-model="imeUser" placeholder="ime"/>
        <input type="text" v-model="prezimeUser" placeholder="prezime"/>
        <input type="email" v-model="emailUser" placeholder="email"
          pattern="[a-zA-Z0-9.!#$%’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/"/>
        <input type="text" v-model="mobUser" placeholder="mob"/>
        <input type="password" v-model="lozinkaUser" placeholder="lozinka"/>
        <button @click.prevent="registrirajMe()" value="submit">Registracija</button>
      </form>
      <form class="sign-in" action="#">
        <h2>Prijavi se</h2>
        <div>Unesite svoje podatke</div>
        <div></div>
        <div></div>
        <div class="wrong-input"><p>Upisali ste netočne podatke</p></div>
        <input type="email" class="user-validate validate-login"
        v-model="emailUser" placeholder="email"
        pattern="[a-zA-Z0-9.!#$%’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" required/>
        <input type="password" class="user-validate validate-pass" name="mail"
        v-model="lozinkaUser" placeholder="lozinka" required />
        <button type="submit" @click.prevent="completeLogin(emailUser, lozinkaUser)" >
        Prijava</button>
      </form>
    </div>
    </div>
  </article>
</template>

<script>
/* eslint-disable */
import axios from 'axios';

export default {
  name: 'Pocetni',
  data() {
    return {
      signUp: false,
      email: '',
      lozinka: '',
      idUser: null,
      imeUser: null,
      prezimeUser: null,
      emailUser: 'test@test',
      mobUser: null,
      lozinkaUser: '123',
    };
  },
  methods: {
    provjeriPodatke(email, pass) {
      console.log(email, pass);
      axios.post('http://127.0.0.1:8080/useri/login', {
        data: {
          email,
          pass,
        },
      }).then((response) => {
        // console.log(response.data);
        // console.log('Upisao si pravi mail');
        const validate = document.querySelectorAll('.user-validate');
        const wrongInputText = document.querySelector('.wrong-input');
        wrongInputText.style.display = 'none';
        let i;
        // console.log(validate);
        for (i = 0; i < validate.length; i += 1) {
          validate[i].style.border = '2px solid green';
        }
        localStorage.setItem('ulaz', 'OK');
      })
        .catch((e) => {
          // console.log('Upsss, probaj ponovno, nešto nije ispravno!!');
          const validate = document.querySelectorAll('.user-validate');
          const wrongInputText = document.querySelector('.wrong-input');
          let i;
          console.log(wrongInputText);
          wrongInputText.style.display = 'block';
          wrongInputText.style.color = 'red';
          for (i = 0; i < validate.length; i += 1) {
            validate[i].style.border = '1px solid red';
          }
          console.error(e);
        });
    },
    emitMethod () {
      EventBus.$emit('logged-in', 'loggedin')
    },
    registrirajMe() {
      axios.post('http://127.0.0.1:8080/useri', {
        ime: this.imeUser,
        prezime: this.prezimeUser,
        email: this.emailUser,
        mob: this.mobUser,
        rola: 'user',
        lozinka: this.lozinkaUser,
      }).then((response) => {
        console.log(response.data);
      })
        .catch((e) => {
          console.error(e);
        });
    },
    zapamtiPodatkeTrenutnog(email, pass) {
      axios
        .post('http://127.0.0.1:8080/useri/ulogiran', {
          data: {
            email,
            pass,
          },
        }).then((response) => {
          console.log(response.data);
          localStorage.setItem('detalji', response.data);
          this.$router.push({ name: 'DetaljiUser' });
        });
    },
    completeLogin(mail, loz){
      this.provjeriPodatke(mail, loz);
      this.zapamtiPodatkeTrenutnog(mail, loz);
    },
  },
};
</script>


<style lang="scss" scoped>
  .user-validate{
    border:none;
  }
  .wrong-input{
    display:none;
    color:'red'!important;
  }
  .container {
    position: relative;
    width: 768px;
    height: 480px;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 15px 30px rgba(0, 0, 0, .2),
                0 10px 10px rgba(0, 0, 0, .2);
    background: lightgrey;
    .overlay-container {
      position: absolute;
      top: 0;
      left: 50%;
      width: 50%;
      height: 100%;
      overflow: hidden;
      transition: transform .5s ease-in-out;
      z-index: 100;
    }
    .overlay {
      position: relative;
      left: -100%;
      height: 100%;
      width: 200%;
      background: linear-gradient(to bottom right, #cfd4ca, #32ac6b);
      color: #fff;
      transform: translateX(0);
      transition: transform .5s ease-in-out;
    }
    @mixin overlays($property) {
      position: absolute;
      top: 0;
      display: flex;
      align-items: center;
      justify-content: space-around;
      flex-direction: column;
      padding: 70px 40px;
      width: calc(50% - 80px);
      height: calc(100% - 140px);
      text-align: center;
      transform: translateX($property);
      transition: transform .5s ease-in-out;
    }
    .overlay-left {
      @include overlays(-20%);
    }
    .overlay-right {
      @include overlays(0);
      right: 0;
    }
  }
  h2 {
    margin: 0;
  }
  p {
    margin: 20px 0 30px;
  }
  a {
    color: #222;
    text-decoration: none;
    margin: 15px 0;
    font-size: 1rem;
  }
  button {
    border-radius: 20px;
    border: 1px solid #009345;
    background-color: #009345;
    color: #fff;
    font-size: 1rem;
    font-weight: bold;
    padding: 10px 40px;
    letter-spacing: 1px;
    text-transform: uppercase;
    cursor: pointer;
    transition: transform .1s ease-in;
    &:active {
      transform: scale(.9);
    }
    &:focus {
      outline: none;
    }
  }
  button.invert {
    background-color: transparent;
    border-color: #fff;
  }
  form {
    position: absolute;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-direction: column;
    padding: 90px 60px;
    width: calc(50% - 120px);
    height: calc(100% - 180px);
    text-align: center;
    background: lightgrey;
    transition: all .5s ease-in-out;
    div {
      font-size: 1rem;
    }
    input {
      background-color: #eee;
      border: none;
      padding: 8px 15px;
      margin: 6px 0;
      width: calc(100% - 30px);
      border-radius: 15px;
      border-bottom: 1px solid #ddd;
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, .4),
                        0 -1px 1px #fff,
                        0 1px 0 #fff;
      overflow: hidden;
      &:focus {
        outline: none;
        background-color: #fff;
      }
    }
  }
  .sign-in {
    left: 0;
    z-index: 2;
    margin-left: 9%;
    margin-top: 10%;
    width: 44%;
    height:63%;
  }
  .sign-up {
    left: 0;
    z-index: 1;
    opacity: 0;
    margin-left: 11%;
    margin-top: 10%;
  }
  .sign-up-active {
    background: lightgrey;
    .sign-in {
      transform: translateX(100%);
    }
    .sign-up {
      transform: translateX(100%);
      opacity: 1;
      z-index: 5;
      animation: show .5s;
      width: 44%;
    }
    .overlay-container {
      transform: translateX(-100%);
    }
    .overlay {
      transform: translateX(50%);
    }
    .overlay-left {
      transform: translateX(0);
    }
    .overlay-right {
      transform: translateX(20%);
    }
  }
  @keyframes show {
    0% {
      opacity: 0;
      z-index: 1;
    }
    49% {
      opacity: 0;
      z-index: 1;
    }
    50% {
      opacity: 1;
      z-index: 10;
    }
  }
  .centar {
    justify-content: center;
  }

  .slika {
    width: 100%;
    height: 50%;
    opacity: .8;
    border-color: #009345;
    border: solid 2px;

  }
</style>
