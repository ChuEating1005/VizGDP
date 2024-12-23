<template>
  <div class="flex flex-col">
    <div class="flex justify-center px-4 mt-10 mb-5">
      <h1 class="text-4xl font-bold">Scatterplot</h1>
      <ChartInfo title="How to Use?">
        <li>
          <strong>Region Selection</strong>
          <div>Click on the colored blocks next to region names to toggle visibility of countries from that region.</div>
        </li>
        
        <li>
          <strong>Data Visualization</strong>
          <div>
            <ul>
              <li>X-axis shows Log GDP per capita</li>
              <li>Y-axis shows Life Ladder (happiness score)</li>
              <li>Bubble size represents country population</li>
            </ul>
          </div>
        </li>
        
        <li>
          <strong>Interactive Features</strong>
          <div>
            <ul>
              <li>Hover over bubbles to see detailed country information</li>
              <li>Labels automatically show for countries with large populations</li>
              <li>Points will enlarge on hover for better visibility</li>
            </ul>
          </div>
        </li>
        
        <li>
          <strong>Color Coding</strong>
          <div>
            Each region has a distinct color gradient:
            <div class="region-colors">
              <div class="region-item">
                <span class="color-dot" style="background-color: #10B981;"></span>
                <span>Oceania</span>
              </div>
              <div class="region-item">
                <span class="color-dot" style="background-color: #1F2937;"></span>
                <span>Africa</span>
              </div>
              <div class="region-item">
                <span class="color-dot" style="background-color: #3B82F6;"></span>
                <span>Europe</span>
              </div>
              <div class="region-item">
                <span class="color-dot" style="background-color: #EF4444;"></span>
                <span>Americas</span>
              </div>
              <div class="region-item">
                <span class="color-dot" style="background-color: #F59E0B;"></span>
                <span>Asia</span>
              </div>
            </div>
          </div>
        </li>
      </ChartInfo>
    </div>
    <div class="selector mb-4">
      <label for="mapSelector" class="mr-2">Select Plot:</label>
      <select
        id="mapSelector"
        v-model="selectedMap"
        @change="switchMap"
        class="map-selector"
      >
        <option value="GNH">GNH</option>
        <option value="Life">Life Expectancy</option>
      </select>
    </div>
    <component :is="selectedMapComponent"></component>
  </div>
</template>

<script setup>
import GNHPlot from "@/components/ScatterPlot/Scatter_GNH.vue";
import LifePlot from "@/components/ScatterPlot/Scatter_Life.vue";
import ChartInfo from "@/components/common/ChartInfo.vue";
import { ref, computed } from "vue";

const selectedMap = ref("GNH");
const selectedMapComponent = computed(
  () =>
    ({
      GNH: GNHPlot,
      Life: LifePlot,
    }[selectedMap.value])
);

const switchMap = () => {
  // This method is triggered when the select value changes
};
</script>

<style scoped>
.selector {
  margin-top: 0.3rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

select {
  padding: 0.5rem 2rem 0.5rem 1rem;
  border-radius: 0.25rem;
  border: 2px solid #e2e8f0;
  background-color: white;
  font-size: 1rem;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1em;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

select:hover {
  border-color: #cbd5e0;
}

select:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.selector label {
  margin-right: 12px;
  font-weight: 500;
  color: #4a5568;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>
