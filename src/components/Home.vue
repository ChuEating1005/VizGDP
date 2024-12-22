<template>
  <div class="min-h-screen relative py-20 px-4 text-white">
    <!-- 背景圖片 -->
    <div
      class="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-80"
      :style="{ backgroundImage: `url(${backgroundImage})` }"
    >
      <!-- 暗色遮罩 -->
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>
    </div>

    <!-- 內容區域 -->
    <div class="max-w-4xl mx-auto relative z-10">
      <!-- 標題部分 -->
      <div class="text-center mb-16">
        <h1
          class="text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-emerald-400"
        >
          Global GDP Visualization
        </h1>
        <p class="text-2xl text-cyan-300">
          Exploring Economic Trends Through Interactive Data Visualization
        </p>
      </div>

      <!-- 功能介紹卡片 -->
      <div class="grid md:grid-cols-2 gap-8 mb-16">
        <div
          class="bg-slate-900/50 p-8 rounded-lg backdrop-blur-sm border border-slate-700/50"
        >
          <h2 class="text-2xl font-bold mb-4 text-cyan-300">Features</h2>
          <ul class="space-y-3 text-gray-300">
            <li class="flex items-center gap-4">
              <span class="w-2 h-2 bg-cyan-400 rounded-full"></span>
              <span class="flex-1 text-left">Bar Chart Race: GDP, GNH, Population, Life Expectancy</span>
            </li>
            <li class="flex items-center gap-4">
              <span class="w-2 h-2 bg-cyan-400 rounded-full"></span>
              Interactive Choropleth Maps with Time Series
            </li>
            <li class="flex items-center gap-4">
              <span class="w-2 h-2 bg-cyan-400 rounded-full"></span>
              GDP vs GNH and GDP vs Life Expectancy Scatter Plot
            </li>
            <li class="flex items-center gap-4">
              <span class="w-2 h-2 bg-cyan-400 rounded-full"></span>
              Historical Economic Events Timeline
            </li>
          </ul>
        </div>

        <div
          class="bg-slate-900/50 p-8 rounded-lg backdrop-blur-sm border border-slate-700/50"
        >
          <h2 class="text-2xl font-bold mb-4 text-cyan-300">About</h2>
          <p class="text-gray-300 leading-relaxed text-justify">
            This project provides comprehensive visualizations of global
            development indicators from 1960 to 2022. Beyond GDP, it explores
            the relationships between economic growth, population dynamics, life
            expectancy, and happiness indices (GNH), offering multiple
            interactive ways to understand how these factors shape our world.
          </p>
        </div>
      </div>

      <!-- 開始按鈕 -->
      <div class="text-center">
        <button
          @click="$emit('update:selectedComponent', 'BarChartRace')"
          class="px-8 py-3 bg-gradient-to-r from-cyan-500 to-emerald-500 rounded-full text-lg font-semibold hover:from-cyan-600 hover:to-emerald-600 transition-all duration-300 shadow-lg"
        >
          Start Exploring
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import backgroundImage from '@/assets/home.jpg'

export default {
  name: "Home",
  emits: ["update:selectedComponent"],
  data() {
    return {
      backgroundImage
    }
  }
};
</script>
