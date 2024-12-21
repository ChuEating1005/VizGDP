<template>
    <div class="flex items-center justify-center px-4 mt-10 mb-5">
        <h1 class="text-4xl font-bold text-center ">Choropleth Map</h1>
        <ChartInfo title="How to Use?" class="my-auto">
            <li>
                <strong>Highest/Lowest Selection:</strong><br>
                You can choose to display either the top 10 highest values or the lowest values
            </li>
            <li>
                <strong>Playback Control:</strong><br>
                Use the play/pause button to control the animation. The timeline slider allows you to jump to specific points in time
            </li>
            <li>
                <strong>Continent Filter:</strong><br>
                Toggle different continents to filter the data and focus on specific regions
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
                <option value="GDP">GDP</option>
                <option value="GNH">GNH</option>
                <option value="Life">Life Expectancy</option>
                <option value="Population">Population</option>
            </select>
        </div>
        <component :is="selectedMapComponent"></component>
    </div>
</template>

<script setup>
import Gdpmap from '@/components/ChoroplethMap/GdpMap.vue';
import GNHMap from '@/components/ChoroplethMap/GNHMap.vue';
import LifeMap from '@/components/ChoroplethMap/LifeMap.vue';
import PopulationMap from '@/components/ChoroplethMap/PopulationMap.vue';
import ChartInfo from '@/components/common/ChartInfo.vue';
import { ref, computed } from 'vue';

const selectedMap = ref('GDP');
const selectedMapComponent = computed(() => ({
    'GDP': Gdpmap,
    'GNH': GNHMap,
    'Life': LifeMap,
    'Population': PopulationMap
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