<template>
  <div>
    <nav>
      <ul>
        <li :class="{ active: selectedComponent === 'BarChartRace' }" @click="selectedComponent = 'BarChartRace'">Bar Chart Race</li>
        <li :class="{ active: selectedComponent === 'ChoroplethMap' }" @click="selectedComponent = 'ChoroplethMap'">Choropleth Map</li>
      </ul>
    </nav>
    <div id="content">
      <component :is="selectedComponent"/>
    </div>
  </div>
</template>

<script>
import BarChartRace from './components/BarChartRace.vue'
import ChoroplethMap from './components/ChoroplethMap.vue';

export default {
  name: 'App',
  components: {
    ChoroplethMap,
    BarChartRace
  },
  data() {
    return {
      selectedComponent: 'BarChartRace'
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

nav {
  background-color: #2c3e50;
  padding: 1%;
}

nav ul {
  list-style-type: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 20px;
  cursor: pointer;
  color: white;
}

nav ul li.active {
  font-weight: bold;
  font-size: larger
}
</style>
