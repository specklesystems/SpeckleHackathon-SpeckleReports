<template>
  <v-btn small :loading="loading" :disabled="disabled" color="success" v-if="!pendingConfirm" block @click="pendingConfirm = true">Merge</v-btn>
  <div v-else>
    <div>Please confirm:</div>
    <v-btn small color="error" @click="pendingConfirm = false">Cancel</v-btn>
    <v-btn small color="success" @click="confirmClicked">Merge!</v-btn>
  </div>
</template>

<script>
export default {
  name: "ConfirmButton",
  props: ["loading", "disabled"],
  data(){
    return {
      pendingConfirm: false
    }
  },
  methods:{
    confirmClicked(){
      this.pendingConfirm = false
      this.$emit('update:loading', true)
      this.$emit('confirm')
    }
  }
}
</script>

<style scoped>

</style>