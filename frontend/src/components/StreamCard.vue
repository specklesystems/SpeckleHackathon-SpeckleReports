<template>
  <v-card id="stream-card" outlined style="z-index: 2; min-width: 350px" class="d-flex flex-column">
    <v-card-title>{{ name }}</v-card-title>
    <v-card-subtitle>
      <v-btn x-small color="primary" target="_blank" :href="streamUrl" >
        Go to Stream page
        <v-icon class="pl-1" size="small">mdi-open-in-new</v-icon>
      </v-btn>
    </v-card-subtitle>
    <v-card-text>
      <p class="mb-0">Choose branches to view:</p>
      <v-checkbox v-for="branch in branches" :key="branch.name" :label="branch.name"
                  v-model="selectedBranches[branch.name]" @change="selectionChanged" dense hide-details class="ml-2"
                  :disabled="branch.commits.items.length == 0"></v-checkbox>
      <!--      <v-divider class="ma-2"></v-divider>-->
      <!--      <p>Merge selection into branch:</p>-->
      <!--      <v-select class="mb-4" v-model="mergeTarget" dense hide-details :loading="!branches" :items="branches ? Object.values(branches) : []" item-text="name"></v-select>-->
      <!--      <confirm-button @confirm="mergeSelectedToTarget" :loading.sync="loading" :disabled="false"></confirm-button>-->
    </v-card-text>
  </v-card>
</template>

<script>
import {getStreamBranches} from "@/speckleUtils";
import ConfirmButton from "@/components/ConfirmButton";

export default {
  name: "StreamCard",
  components: {},
  props: ["streamId"],
  data() {
    return {
      name: null,
      branches: null,
      selectedBranches: {},
    }
  },
  methods: {
    selectionChanged() {
      console.log("selection changed")
      let res = []
      this.branches?.forEach(branch => {
        if (this.selectedBranches[branch.name]) {
          res.push(branch.commits.items[0])
        }
      })
      this.$emit('load-objects', res)
    }
  },
  computed: {
    streamUrl() {
      return process.env.VUE_APP_SERVER_URL + "/streams/" + this.streamId
    }
  },
  watch: {
    streamId: {
      deep: true,
      immediate: true,
      handler: async function (val, oldVal) {
        if (!val) {
          this.branches = null
          this.selectedBranches = {}
        }
        var stream = await getStreamBranches(val)
        console.log(stream, val)
        stream.branches.items.forEach(branch => {
          this.selectedBranches[branch.name] = false
        })
        this.branches = stream.branches.items
        this.name = stream.name
      }
    }
  }
}
</script>

<style scoped lang="scss">
#stream-card {
  max-height: 100% !important;
  overflow: hidden;
}
</style>