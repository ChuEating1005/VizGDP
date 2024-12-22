<template>
    <div class="flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-center px-4 mt-10 mb-5">
            <h1 class="text-4xl font-bold text-center ">Bar Chart Race</h1>
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
        <div class="selector mb-4">
            <label for="chartSelector" class="mr-2">Select Chart:</label>
            <select id="chartSelector" v-model="selectedChartId">
                <option value="20144600">GDP per capita</option>
                <option value="20895787">GNH per capita</option>
                <option value="20897395">World Population</option>
                <option value="20897358">Life Expectancy</option>
            </select>
        </div>
        <RaceChart 
            :key="selectedChartId"
            :chartId="selectedChartId"
        />
    </div>
</template>

<script setup>
import RaceChart from '@/components/BarChartRace/RaceChart.vue';
import ChartInfo from '@/components/common/ChartInfo.vue';
import { ref } from 'vue';

const selectedChartId = ref("20144600"); // 預設值
</script>

<style scoped>
.selector {
    display: flex;
    justify-content: center;
    align-items: center;
}

select {
    padding: 0.5rem;
    border-radius: 0.25rem;
    border: 1px solid #ccc;
}
</style>