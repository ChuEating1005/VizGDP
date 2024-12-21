<template>
    <div class="flex flex-col">
        <h1 class="text-2xl font-bold text-center">Choropleth Map</h1>
        <Gdpmap />
    </div>
</template>

<script setup>
import Gdpmap from '@/components/ChoroplethMap/GdpMap.vue';
</script>

<style scoped></style>