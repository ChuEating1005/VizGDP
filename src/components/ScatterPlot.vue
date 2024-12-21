<template>
    <div class="flex flex-col px-4 mt-10 mb-5">
        <div class="flex justify-center">
            <h1 class="text-4xl font-bold">Scatterplot</h1>
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
        <h2 class="text-xl font-bold text-center mt-2 text-gray-500">Life Ladder vs Log GDP per Capita</h2>
        <ScatterPlot />
    </div>
</template>

<script setup>
import ScatterPlot from '@/components/ScatterPlot/ScatterPlot.vue';
import ChartInfo from '@/components/common/ChartInfo.vue';
</script>

<style scoped></style>