<template>
    <header>
      <p>{{msg}}</p>
    </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      msg: 'Aplikacija za predikciju',
    };
  },
};
</script>

<style>
header {
  background: #3B3B3B;
  background-image: linear-gradient(to right, black, rgb(53, 141, 92));
  color: #ffffff;
  padding: 15px 0px;
  flex-grow: 0;
  /*opacity: .95;*/
  top: 0px;
  width: 100%;
  height: 80px;
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  font-family: fantasy;
  font-weight: bold;
  font-style: italic;
  font-size: 35px;
  color: aquamarine;
}


</style>
