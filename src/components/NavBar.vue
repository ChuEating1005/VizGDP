<template>
  <nav class="bg-slate-800 py-4">
    <ul class="flex gap-5 items-center max-w-7xl mx-3 pl-5">
      <li 
        v-for="item in navItems" 
        :key="item.name"
        :class="[
          'flex justify-center items-center gap-2 cursor-pointer text-white px-4 py-2 transition-all duration-100 hover:text-cyan-300 ',
          selectedComponent === item.component ? 'font-bold text-xl text-cyan-300' : 'text-base text-lg'
        ]"
        @click="updateComponent(item.component)"
      >
        <component :is="item.icon" class="w-5 h-5" />
        {{ item.name }}
      </li>
    </ul>
  </nav>
</template>

<script>
import { 
  HomeIcon,
  ChartBarIcon, 
  GlobeAmericasIcon, 
  ChartPieIcon,
  ClockIcon 
} from '@heroicons/vue/24/outline'

export default {
  name: 'NavBar',
  components: {
    HomeIcon,
    ChartBarIcon,
    GlobeAmericasIcon,
    ChartPieIcon,
    ClockIcon
  },
  props: {
    selectedComponent: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      navItems: [
        { 
          name: 'Home', 
          component: 'Home',
          icon: 'HomeIcon'
        },
        { 
          name: 'Bar Chart Race', 
          component: 'BarChartRace',
          icon: 'ChartBarIcon'
        },
        { 
          name: 'Choropleth Map', 
          component: 'ChoroplethMap',
          icon: 'GlobeAmericasIcon'
        },
        { 
          name: 'Scatter Plot', 
          component: 'ScatterPlot',
          icon: 'ChartPieIcon'
        },
        { 
          name: 'Time Line', 
          component: 'TimeLine',
          icon: 'ClockIcon'
        }
      ]
    }
  },
  emits: ['update:selectedComponent'],
  methods: {
    updateComponent(component) {
      this.$emit('update:selectedComponent', component)
    }
  }
}
</script>