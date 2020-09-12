<template>
  <div class="container" :class="{'show': showSidebar}">
    <div class="control">
      <i><font-awesome-icon :icon="['fas', 'angle-double-right']" @click="showNav" /></i>
    </div>
    <div class="navigation-icons">
      <i class='probaj'><font-awesome-icon :icon="['fas', 'user']" @click.prevent="vratiNaHome()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'users']" @click.prevent="idiNaUsere2()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'flag-checkered']" @click.prevent="idiNaDrzave()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'dungeon']" @click.prevent="idiNaSobe()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'bed']" @click.prevent="idiNaHotele()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'indent']" @click.prevent="idiNaPredikcije()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'university']" @click.prevent="idiNaJedinice()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'credit-card']" @click.prevent="idiNaIznose()" /></i>
      <i class='probaj'><font-awesome-icon :icon="['fas', 'sign-out-alt']" @click.prevent="idiVan()" /></i>
    </div>
    <div class="navigation-links">
      <transition-group name="fade">
        <div v-show="showLink" key="1" @click.prevent="vratiNaHome()">Home</div>
        <div v-show="showLink" key="2" @click.prevent="idiNaUsere2()">Korisnici</div>
        <div v-show="showLink" key="3" @click.prevent="idiNaDrzave()">Države</div>
        <div v-show="showLink" key="4" @click.prevent="idiNaSobe()">Sobe</div>
        <div v-show="showLink" key="5" @click.prevent="idiNaHotele()">Hoteli</div>
        <div v-show="showLink" key="6" @click.prevent="idiNaPredikcije()">Predikcije</div>
        <div v-show="showLink" key="7" @click.prevent="idiNaJedinice()">Jedinice</div>
        <div v-show="showLink" key="8" @click.prevent="idiNaIznose()">Iznosi</div>
        <div v-show="showLink" key="9" @click.prevent="idiVan()">Odjava</div>
      </transition-group>
    </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      showSidebar: false,
      showLink: false,
    };
  },
  methods: {
    idiVan() {
      localStorage.clear();
      this.$router.push({ name: 'Pocetni' });
    },
    vratiNaHome() {
      this.$router.push({ name: 'DetaljiUser' });
    },
    idiNaUsere2() {
      this.$router.push({ name: 'Useri2' });
    },
    idiNaDrzave() {
      this.$router.push({ name: 'Drzave' });
    },
    idiNaPredikcije() {
      this.$router.push({ name: 'Predikcije' });
    },
    idiNaJedinice() {
      this.$router.push({ name: 'Jedinice' });
    },
    idiNaIznose() {
      this.$router.push({ name: 'Iznosi' });
    },
    idiNaSobe() {
      this.$router.push({ name: 'Sobe' });
    },
    idiNaHotele() {
      this.$router.push({ name: 'Hoteli' });
    },
    showNav() {
      if (this.showSidebar) {
        this.showLink = false;
        setTimeout(() => {
          this.showSidebar = false;
        }, 500);
      } else {
        this.showSidebar = true;
        setTimeout(() => {
          this.showLink = true;
        }, 500);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
  .probaj {
    height: 49px;
  }
  .container {
    position: fixed;
    background-image: linear-gradient(to bottom, black, rgb(47, 107, 36));
    top: 80px;
    left: 0;
    width: 70px;
    padding: 10px 0;
    padding-top: 10px;
    min-height: 900px; /* min-height: calc(100vh - 20px); */
    /*background-image: url("../../src/assets/sidebar-1.jpg");
    border: hidden; /* border: solid rgb(12, 12, 12); */
    border-width: 0 1px 0 0;
    z-index: 1;
    transition: all .5s ease-in-out;
    opacity: 1;
    flex-grow: 1;
    margin-left: auto;
    .control {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 50px;
      margin-bottom: 10px;
      margin-left: auto;
      i {
        font-size: 2rem;
        cursor: pointer;
        transition: all .5s ease-in-out;
      }
    }
    &.show { /* strelica back*/
      width: 180px;
      .control > i {
        color: rgb(15, 161, 105);
        transform: rotateZ(-180deg);
      }
      .navigation-icons { /* boja ikona*/
        color: rgb(15, 161, 105);
      }
    }
    .navigation-icons {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 50px;
      float: left;
      i {
        font-size: 2rem;
        padding: 10px 0;
        cursor: pointer;
        transition: all .5s ease-in-out;
        &:hover { /* mouseover ikone*/
          color: rgb(169, 219, 123);
        }
      }
    }
    .navigation-links {
      padding-top: 14px;
      float: left;
      div {
        font-size: 1.35rem;
        padding-left: 10px;
        margin-bottom: 18px;
        cursor: pointer;
        color: rgb(15, 161, 105); /* font boja natpisi */
        &:hover { /* mouseover natpisi*/
          color: rgb(169, 219, 123);
        }
      }
    }
  }
  @mixin nav-childs($values...) {
    @each $var in $values {
      &:nth-child(#{$var}) {
        transition: transform linear calc(.1s * #{$var}), display .5s;
      }
    }
  }
  .fade-enter-active, .fade-leave-active {
    @include nav-childs(1,2,3,4,5);
  }
  .fade-enter, .fade-leave-to {
    transform: scale(0);
  }

 .column {
  float: left;
  padding: 10px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>
