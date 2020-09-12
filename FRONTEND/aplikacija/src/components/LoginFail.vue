<template>
  <article>
    <div class="container">
      <div class="prazan"></div>
        <p>Niste ulogirani, kliknite na link ispod da biste se prijavili i
          nastavili koristiti aplikaciju</p>
         <button @click.prevent="vratiNaHome()" ><font-awesome-icon :icon="['fas', 'home']"/>
        LOGIN
        </button>
    </div>
  </article>
</template>

<script>
export default {
  name: 'LoginFail',
  data() {
    return {
    };
  },
  methods: {
    vratiNaHome() {
      this.$router.push({ name: 'Pocetni' });
    },
  },
};
</script>


<style lang="scss" scoped>
.prazan {
  height: 100px;
}
</style>
