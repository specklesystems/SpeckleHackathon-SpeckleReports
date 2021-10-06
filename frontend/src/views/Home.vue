<template lang="html">
  <v-container fill-height class="home flex-column justify-center align-center primary--text">
    <div class="d-flex justify-center align-center">
      <v-img src="@/assets/logo.png" max-height="140" max-width="140" min-width="100"></v-img>
    </div>
    <h1>👋 Hi {{user.name}}!!</h1>
    <h3>Search for a stream using the top menu to get started ☝</h3>
  </v-container>
</template>

<script>

export default {
  name: 'Home',
  data(){
    return {

    }
  },
  computed: {
    user(){
      return this.$store.state.user
    }
  }
}
</script>

<style lang="scss">
.v-data-footer__select {
  display: none !important;
}
.home {
  position: relative;
  height: 100%;
}
#corner-right{
  position: absolute;
  top: 1em;
  left: 1em;
  z-index: 3;
}
#bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
</style>