import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

import {
  APP_NAME,
  TOKEN,
  exchangeAccessCode,
  getStreamCommits,
  getUserData,
  goToSpeckleAuthPage,
  speckleLogOut
} from "@/speckleUtils";
import router from "@/router";

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
  key: `${APP_NAME}.vuex`
})

export default new Vuex.Store({
  plugins: [vuexLocal.plugin],
  state: {
    user: null,
    serverInfo: null,
    currentStream: null,
  },
  getters: {
    isAuthenticated: (state) => state.user != null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setServerInfo(state, info) {
      state.serverInfo = info
    },
    setCurrentStream(state, stream) {
      state.currentStream = stream
    }
  },
  actions: {
    logout(context) {
      // Wipe the state
      context.commit("setUser", null)
      context.commit("setServerInfo", null)
      context.commit("setCurrentStream", null)
      // Wipe the tokens
      speckleLogOut()
      router.push("/login")
    },
    exchangeAccessCode(context, accessCode) {
      // Here, we could save the tokens to the store if necessary.
      return exchangeAccessCode(accessCode)
    },
    async getUser(context) {
      try {
        var json = await getUserData()
        var data = json.data
        context.commit("setUser", data.user)
        context.commit("setServerInfo", data.serverInfo)
      } catch (err) {
        console.error(err)
      }
    },
    redirectToAuth() {
      goToSpeckleAuthPage()
    },
    async handleStreamSelection(context, stream) {
      context.commit("setCurrentStream", stream)
      router.push(`/streams/${stream.id}`)
    },
    clearStreamSelection(context){
      context.commit("setCurrentStream", null)
    }
  },
  modules: {}
})
