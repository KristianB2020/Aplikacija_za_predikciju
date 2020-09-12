<template>
    <footer>
      <p>{{msg}}</p>
    </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      msg: 'FORECAST - footer',
    };
  },
};
</script>

<style>

footer {
  background: #000000;
  font-family: fantasy;
  font-weight: bold;
  font-style: italic;
  font-size: 35px;
  color: aquamarine;
}
</style>
