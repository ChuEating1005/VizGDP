<template>
  <div class="timeline-container w-full min-h-screen relative py-20 bg-fixed bg-cover transition-all duration-300" 
       :style="{ backgroundImage: `url(${currentImage})` }">
    <!-- 增加背景模糊和透明度 -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-md"></div>
    
    <!-- Header -->
    <div class="timeline-header w-full text-center mb-20 relative">
      <h2 class="text-white text-4xl font-normal font-cardo m-0">Global GDP Shaping Events</h2>
      <h3 class="text-white/50 font-pathway text-base tracking-widest mt-2.5 font-normal">Crises and Transformations</h3>
    </div>

    <!-- Timeline -->
    <div class="timeline flex flex-wrap flex-col max-w-[1000px] mx-auto relative before:absolute before:left-1/2 before:w-0.5 before:h-full before:content-[''] before:-ml-[1px] before:bg-white/10">
      <div v-for="(item, index) in timelineItems" 
           :key="index"
           :class="[
             'timeline-item py-10 transition-all duration-500 w-[calc(50%)] flex relative',
             isActive(index) ? 'opacity-100 translate-y-0 blur-none' : 'opacity-30 -translate-y-20 blur-sm',
             index % 2 !== 0 ? 'self-end' : ''
           ]">
        
        <!-- 添加左側或右側的小字 -->
        <div :class="[
          'absolute top-1/2 transform -translate-y-1/2 text-2xl text-white/70 w-1/2 font-pathway tracking-widest',
          index % 2 === 0 ? 'left-[105%]' : 'right-[105%]'
        ]" style="text-shadow: 0 0 10px rgba(0,0,0,0.8);">
          {{ item.text }}
        </div>

        <div :class="[
          'absolute w-4 h-4 bg-white/70 top-1/2 -translate-y-1/2 transform rotate-45',
          index % 2 === 0 ? 'right-0 translate-x-1/2' : 'left-0 -translate-x-1/2'
        ]"></div>

        <div class="timeline__content relative p-8 rounded-lg mx-10">
          <img :src="item.image" :alt="item.title" 
               class="w-full h-auto shadow-[0_20px_25px_-5px_rgba(0,0,0,0.5)] mb-6">
          <h2 class="font-pathway font-normal text-6xl text-white absolute -mt-14 left-20 -ml-10 border-b-2 border-white/50" style="text-shadow: 0 0 10px rgba(0,0,0,0.8);">
            {{ item.title }}
          </h2>
          <p class="text-white/70 font-cardo text-lg text-left leading-relaxed mt-16 pl-4">
            {{ item.description }}
          </p>
          <p class="text-white/70 font-cardo text-sm text-left leading-relaxed mt-2 pl-4">
            Image source: <a :href="item.src" class="text-blue-200 underline">link</a>
          </p>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import timeline1 from '@/assets/timeline/node1.png'
import timeline2 from '@/assets/timeline/node2.png'
import timeline3 from '@/assets/timeline/node3.png'
import timeline4 from '@/assets/timeline/node4.png'
import timeline5 from '@/assets/timeline/node5.png'
import timeline6 from '@/assets/timeline/node6.png'
import timeline7 from '@/assets/timeline/node7.png'
import timeline8 from '@/assets/timeline/node8.png'

const timelineItems = ref([
  {
    text: '1973 Oil Crisis',
    image: timeline1,
    title: '1973',
    description: 'Triggered by an OPEC oil embargo, this crisis led to soaring oil prices, causing economic recessions in many countries.',
    src: 'https://www.federalreservehistory.org/essays/oil-shock-of-1973-74'
  },
  {
    text: '1979 Oil Crisis',
    image: timeline2,
    title: '1979',
    description: 'Stemming from the Iranian Revolution, this event resulted in reduced oil output and further price hikes, exacerbating global economic challenges.',
    src: 'https://www.federalreservehistory.org/essays/oil-shock-of-1978-79'
  },
  {
    text: 'Debt Crisis',
    image: timeline3,
    title: '1980s',
    description: 'Numerous developing nations faced unsustainable debt levels, leading to economic slowdowns and the need for international financial interventions.',
    src: 'https://arthagyaipcw.wordpress.com/2023/02/21/the-lost-decade-latin-america-debt-crisis-1980/'
  },
  {
    text: 'Asian Financial Crisis',
    image: timeline4,
    title: '1997',
    description: 'Originating in Thailand, this crisis spread across East Asia, causing significant economic contractions in affected countries.',
    src: 'https://ohmyecon.org/journal/the-1997-asian-financial-crisis'
  },
  {
    text: 'Global Financial Crisis',
    image: timeline5,
    title: '2007–2008',
    description: 'Sparked by the collapse of the housing bubble in the United States, this crisis led to a severe worldwide economic downturn, known as the Great Recession.',
    src: 'https://medium.com/@shashankacharya4/global-financial-crisis-2007-2009-analyzing-through-the-keynesian-is-lm-framework-3ea9935b0748'
  },
  {
    text: 'European Debt Crisis',
    image: timeline6,
    title: '2010',
    description: 'Several European nations, notably Greece, faced sovereign debt challenges, leading to austerity measures and economic contractions within the Eurozone.',
    src: 'https://www.nytimes.com/2010/11/16/business/global/16euro.html'
  },
  {
    text: 'COVID-19 Pandemic',
    image: timeline7,
    title: '2020',
    description: 'The global outbreak of COVID-19 resulted in unprecedented economic disruptions, with worldwide GDP contracting by approximately 3.1% in 2020.',
    src: 'https://www.cdc.gov/museum/timeline/covid19.html'
  },
  {
    text: 'Global Economic Slowdown',
    image: timeline8,
    title: '2022–2023',
    description: 'Post-pandemic recovery faced obstacles due to supply chain disruptions, inflationary pressures, and geopolitical tensions, leading to sluggish growth.',
    src: 'https://www.foxbusiness.com/economy/bank-america-still-forecasting-2023-recession-fed-action-not-enough-exec-warns'
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