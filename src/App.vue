<template>
  <div>
    <NavBar
      :selectedComponent="selectedComponent"
      @update:selectedComponent="selectedComponent = $event"
    />
    <div id="content">
      <keep-alive>
        <component 
          :is="selectedComponent"
          @update:selectedComponent="selectedComponent = $event"
        />
      </keep-alive>
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import Home from './components/Home.vue'
import BarChartRace from './components/BarChartRace.vue'
import ChoroplethMap from './components/ChoroplethMap.vue'
import ScatterPlot from './components/ScatterPlot.vue'
import TimeLine from './components/TimeLine.vue'
import Footer from './components/Footer.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    Home,
    BarChartRace,
    ChoroplethMap,
    ScatterPlot,
    TimeLine,
    Footer
  },
  data() {
    return {
      selectedComponent: 'Home'
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
