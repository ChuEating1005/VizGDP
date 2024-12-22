<template>
    <div class="flex flex-col px-4 mt-10 mb-5">
        <div class="flex justify-center">
            <h1 class="text-4xl font-bold">Scatterplot</h1>
            <ChartInfo title="How to Use?" class="my-auto">
                <li>
                    <strong>Region Selection:</strong><br>
                    Click on the colored blocks next to region names to toggle visibility of countries from that region.
                </li>
                <li>
                    <strong>Data Visualization:</strong><br>
                    - X-axis shows Log GDP per capita
                    - Y-axis shows Life Ladder (happiness score)
                    - Bubble size represents country population
                </li>
                <li>
                    <strong>Interactive Features:</strong><br>
                    - Hover over bubbles to see detailed country information
                    - Labels automatically show for countries with large populations
                    - Points will enlarge on hover for better visibility
                </li>
                <li>
                    <strong>Color Coding:</strong><br>
                    Each region has a distinct color gradient:
                    - Oceania: Green
                    - Africa: Black
                    - Europe: Blue
                    - Americas: Red
                    - Asia: Yellow
                </li>
            </ChartInfo>
        </div>
        <div>
        <div class="selector mb-4">
            <label for="mapSelector" class="mr-2">Select Map:</label>
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

    </div>
</template>

<script setup>
import GNHPlot from '@/components/ScatterPlot/Scatter_GNH.vue';
import LifePlot from '@/components/ScatterPlot/Scatter_Life.vue';
import ChartInfo from '@/components/common/ChartInfo.vue';
import { ref, computed } from 'vue';

const selectedMap = ref('GNH');
const selectedMapComponent = computed(() => ({
    'GNH': GNHPlot,
    'Life': LifePlot ,
}[selectedMap.value]));

const switchMap = () => {
    // This method is triggered when the select value changes
};
</script>

<style scoped>
.selector {
    margin-top: .3rem;
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