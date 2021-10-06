<template>
  <v-app>
    <v-app-bar
        app
        color="primary"
        dark
        dense
    >
      <div class="d-flex align-center">
        <v-img
            alt="Speckle Logo"
            class="shrink mr-2"
            contain
            :src="require(`@/assets/img.png`)"
            transition="scale-transition"
            width="40"
            height="24"
        />
        <h3>Speckle</h3>
      </div>

      <v-spacer></v-spacer>

      <stream-search v-if="$store.getters.isAuthenticated" @selected="$store.dispatch('handleStreamSelection', $event)"/>

      <v-spacer></v-spacer>

      <div v-if="isAuthenticated && user" class="mr-1">
        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-avatar color="white" size="28" v-bind="attrs" v-on="on">
              <v-img v-if="user.avatar" :src="user.avatar"></v-img>
              <span v-else class="text--secondary">{{initials}}</span>
            </v-avatar>
          </template>
          <span>You are logged in as <b>{{user.name}}</b></span>
        </v-tooltip>
      </div>

      <v-btn
          outlined
          small
          v-if="!isAuthenticated"
          @click="$store.dispatch('redirectToAuth')"
      >
        <span>Login with Speckle</span>
      </v-btn>
      <v-btn small outlined v-else @click="$store.dispatch('logout')">
        Log out
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import StreamSearch from "@/components/StreamSearch";

export default {
  name: 'App',
  components: {StreamSearch},
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    },
    user(){
      return this.$store.state.user
    },
    initials(){
      if(!this.user?.name) return ""
      return this.user.name.split(" ").map(part => part[0]).join("").toUpperCase()
    }
  }
};
</script>
