<template>
  <v-container v-if="hasCarbonReport">
    <v-row>
      <v-col>
        <v-card v-if="projectInfo">
          <v-card-title>{{projectInfo.name}} {{projectInfo.number}}<span class="d-flex align-center text-body-2 grey--text border pl-2"> <v-icon size="medium" color="grey" class="pr-1">mdi-home-circle-outline</v-icon>{{projectInfo.address}}</span></v-card-title>
          <v-card-subtitle class="d-flex aling-center">
            <v-icon size="small" class="pr-1">mdi-account-circle-outline</v-icon>{{projectInfo.author}}
            <v-icon size="small" class="pr-1 pl-2">mdi-calendar-check-outline</v-icon>{{projectInfo.status}}
          </v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="6" class="pa-1 d-flex align-center justify-end"><p>Total carbon cost</p></v-col>
              <v-col cols="6" class="pa-1"><p><v-chip>{{carbonCost.toLocaleString()}}</v-chip> Kg</p></v-col>
            <v-row>
            </v-row>
              <v-col cols="6" class="pa-1 d-flex align-center justify-end">The equivalent of taking</v-col>
              <v-col cols="6" class="pa-1"><v-chip>{{carbonEquivalentFlight.toLocaleString()}}</v-chip> international flights</v-col>
            <v-row>
            </v-row>
              <v-col cols="6" class="pa-1 d-flex align-center justify-end">The equivalent of driving</v-col>
              <v-col cols="6" class="pa-1"><v-chip>{{carbonEquivalentCar.toLocaleString()}}</v-chip> kilometres by car</v-col>
            <v-row>
            </v-row>
              <v-col cols="6" class="pa-1 d-flex align-center justify-end">The equivalent of burning</v-col>
              <v-col cols="6" class="pa-1"><v-chip>{{carbonEquivalentGas.toLocaleString()}}</v-chip> litres of natural gas</v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>3D Viewer</v-card-title>
          <v-card-text>
            <renderer :object-urls="objectUrls" :auto-load="true"></renderer>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="col-6">
        <v-card>
          <v-card-title>Volume</v-card-title>
          <v-card-text>
            <doughnut-chart v-if="volumeData" :chart-data="volumeData"></doughnut-chart>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="col-6">
        <v-card>
          <v-card-title>Carbon</v-card-title>
          <v-card-text>
            <doughnut-chart v-if="carbonData" :chart-data="carbonData"></doughnut-chart>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else>
    <div v-if="!webhooksSet">
      <p>This stream does not have a carbon report!</p>
      <v-btn :loading="loading" @click="createWebhook">Setup webhook on this stream!</v-btn>
    </div>
    <div v-else>
      <p>Report will be generated next time data is sent to this stream.</p>
    </div>
  </v-container>
</template>

<script>
import Renderer from "@/components/Renderer";
import {createWebhook, getStreamBranches, getStreamObject} from "@/speckleUtils";
import DoughnutChart from "@/components/charts/DoughnutChart";
import interpolate from "color-interpolate"

export default {
  name: "StreamCarbonReport",
  components: { DoughnutChart, Renderer},
  async mounted() {
    this.fetchReport()
  },
  data() {
    return {
      carbonReport: null,
      objectUrls: [ ],
      stream: null,
      volumeData: null,
      carbonData: null,
      palette: interpolate(["blue", "green"]),
      carbonCost: 5000,
      commitObj: null,
      projectInfo: null,
      loading: false,
    }
  },
  computed: {
    webhooksSet(){
      var isSet = false
      this.stream?.webhooks?.items.forEach(hook => {
        if(hook.url === process.env.VUE_APP_WEBHOOK_URL)
          isSet = true
      })
      return isSet
    },
    hasCarbonReport(){
      return this.stream?.carbonBranch != null
    },
    carbonEquivalentCar(){
      var eq = this.carbonCost / 0.258
      return Math.round(eq)
    },
    carbonEquivalentFlight(){
      var eq = this.carbonCost / 986
      return Math.round(eq)
    },
    carbonEquivalentGas(){
      var eq = this.carbonCost / 2.2252
      return Math.round(eq)
    }
  },
  watch: {
    "$route.params": {
      handler: function(val, oldVal){
        console.log("params changed!!!")
        this.carbonData = null
        this.volumeData = null
        this.commitObj = null
        this.projectInfo = null
        this.stream = null
        this.objectUrls = []
        this.carbonCost = 0
        this.fetchReport()
      }
    }
  },
  methods: {
    async createWebhook(){
      console.log("create webhook for stream!")
      this.loading = true
      var res = await createWebhook(this.$route.params.id, process.env.VUE_APP_WEBHOOK_URL, ["commit_create"]).catch(e =>  console.error(e))
      console.log(res)
      await this.fetchReport()
      this.loading = false

    },
    objectUrl(objId){
      return `${process.env.VUE_APP_SERVER_URL}/streams/${this.$route.params.id}/objects/${objId}`
    },
    async fetchReport(){
      this.stream = await getStreamBranches(this.$route.params.id)
      console.log(this.stream)

      if(this.hasCarbonReport) {
        this.commitObj = await getStreamObject(this.$route.params.id, this.stream?.branch.commits.items[0].referencedObject)
        try {
          console.log("proj info", this.commitObj["@Project Information"][0])
          this.projectInfo = await getStreamObject(this.$route.params.id, this.commitObj["@Project Information"][0].referencedId)
          this.objectUrls = [this.objectUrl(this.stream?.branch.commits.items[0].referencedObject)]
        } catch (e) {
          console.warn("Project info fetch failed", e)
        }
        this.carbonReport = await getStreamObject(this.$route.params.id, this.stream.carbonBranch.commits.items[0].referencedObject)
        console.log("CARBON REPORT", this.carbonReport)
        this.computeDatasets()
      }
    },
    computeDatasets(){
      var materialNames = Object.keys(this.carbonReport.results)
      var materialColors = materialNames.map((value,index) => this.palette(index/materialNames.length))
      var carbonData = []
      var volumeData = []
      this.carbonCost = 0
      materialNames.forEach(material => {
        console.warn("material", material)
        var carbonTotal = 0
        var volumeTotal = 0
        for (const objId in this.carbonReport.results[material]) {
          var objData = this.carbonReport.results[material][objId]
          carbonTotal += objData.carbon
          volumeTotal += objData.volume
        }
        carbonData.push(carbonTotal)
        this.carbonCost += carbonTotal
        volumeData.push(volumeTotal)
      })

      var carbon = {
        labels: materialNames,
        datasets: [
          {
            label: "Carbon emissions",
            backgroundColor: materialColors,
            data: carbonData
          }
        ]
      }
      var volume = {
        labels: materialNames,
        datasets: [
          {
            label: "Volume",
            backgroundColor: materialColors,
            data: volumeData
          }
        ]
      }
      this.carbonData = carbon
      this.volumeData = volume
    }
  }
}
</script>

<style scoped>

</style>