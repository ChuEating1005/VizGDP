<template>
  <div class="timeline-container w-full min-h-screen relative py-20 bg-fixed bg-cover transition-all duration-300" 
       :style="{ backgroundImage: `url(${currentImage})` }">
    <!-- 增加背景模糊和透明度 -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-md"></div>
    
    <!-- Header -->
    <div class="timeline-header w-full text-center mb-20 relative">
      <h2 class="text-white text-4xl font-normal font-cardo m-0">Global GDP Shaping Events</h2>
      <h3 class="text-white/50 font-pathway text-base tracking-wider mt-2.5 font-normal">Crises and Transformations</h3>
    </div>

    <!-- Timeline -->
    <div class="timeline flex flex-wrap flex-col max-w-[1000px] mx-auto relative before:absolute before:left-1/2 before:w-0.5 before:h-full before:content-[''] before:-ml-[1px] before:bg-white/10">
      <div v-for="(item, index) in timelineItems" 
           :key="index"
           :class="[
             'timeline-item p-10 transition-all duration-500 w-[calc(60%-40px)] flex relative',
             isActive(index) ? 'opacity-100 translate-y-0 blur-none' : 'opacity-30 -translate-y-20 blur-sm',
             index % 2 !== 0 ? 'self-end' : ''
           ]"
           :data-text="item.text">
        <div class="timeline__content relative p-8 rounded-lg mx-10">
          <img :src="item.image" :alt="item.title" 
               class="w-full h-auto shadow-[0_20px_25px_-5px_rgba(0,0,0,0.5)] mb-6">
          <h2 class="font-pathway font-normal text-6xl text-white absolute -mt-14 left-20 -ml-10 border-b-2 border-white/50" style="text-shadow: 0 0 10px rgba(0,0,0,0.8);">
            {{ item.title }}
          </h2>
          <p class="text-white/70 font-cardo text-lg text-left leading-relaxed mt-16 pl-4">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const timelineItems = ref([
  {
    text: 'Oil Crisis',
    image: 'timeline/node1.png',
    title: '1973',
    description: 'Triggered by an OPEC oil embargo, this crisis led to soaring oil prices, causing economic recessions in many countries.'
  },
  {
    text: 'Oil Crisis',
    image: 'timeline/node2.png',
    title: '1979',
    description: 'Stemming from the Iranian Revolution, this event resulted in reduced oil output and further price hikes, exacerbating global economic challenges.'
  },
  {
    text: 'Debt Crisis',
    image: 'timeline/node3.png',
    title: '1980s',
    description: 'Numerous developing nations faced unsustainable debt levels, leading to economic slowdowns and the need for international financial interventions.'
  },
  {
    text: 'Asian Financial Crisis',
    image: 'timeline/node4.png',
    title: '1997',
    description: 'Originating in Thailand, this crisis spread across East Asia, causing significant economic contractions in affected countries.'
  },
  {
    text: 'Global Financial Crisis',
    image: 'timeline/node5.png',
    title: '2007–2008',
    description: 'Sparked by the collapse of the housing bubble in the United States, this crisis led to a severe worldwide economic downturn, known as the Great Recession.'
  },
  {
    text: 'European Debt Crisis',
    image: 'timeline/node6.png',
    title: '2010',
    description: 'Several European nations, notably Greece, faced sovereign debt challenges, leading to austerity measures and economic contractions within the Eurozone.'
  },
  {
    text: 'COVID-19 Pandemic',
    image: 'timeline/node7.png',
    title: '2020',
    description: 'The global outbreak of COVID-19 resulted in unprecedented economic disruptions, with worldwide GDP contracting by approximately 3.1% in 2020.'
  },
  {
    text: 'Global Economic Slowdown',
    image: 'timeline/node8.png',
    title: '2022–2023',
    description: 'Post-pandemic recovery faced obstacles due to supply chain disruptions, inflationary pressures, and geopolitical tensions, leading to sluggish growth.'
  }
])

const currentImage = ref(timelineItems.value[0].image)
const activeIndex = ref(0)

const isActive = (index) => {
  return index === activeIndex.value
}

const handleScroll = () => {
  const items = document.querySelectorAll('.timeline-item')
  const pos = window.scrollY

  items.forEach((item, i) => {
    const min = item.offsetTop
    const max = item.offsetTop + item.offsetHeight

    if (pos <= max - 40 && pos >= min) {
      activeIndex.value = i
      currentImage.value = timelineItems.value[i].image
    }
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Cardo|Pathway+Gothic+One');

.font-cardo {
  font-family: 'Cardo', serif;
}

.font-pathway {
  font-family: 'Pathway Gothic One', sans-serif;
}

.timeline__content {
  width: 100%;
}

.timeline-item {
  margin-bottom: 2rem;
}

@media only screen and (max-width: 767px) {
  .timeline::before {
    left: 40px;
  }

  .timeline-item {
    align-self: baseline !important;
    width: 100%;
    padding: 0 30px 150px 80px;
  }

  .timeline-item:before {
    left: 10px !important;
    padding: 0 !important;
    top: 50px;
    text-align: center !important;
    width: 60px;
    border: none !important;
  }

}

.timeline-item:last-child {
  margin-bottom: 20vh;
}
</style>