<template>
  <footer class="bg-slate-900 text-gray-300 py-6">
    <div class="container mx-auto px-4">
      <div class="flex flex-col items-center">
        <h3 class="text-xl font-semibold mb-4 text-cyan-400">Authors</h3>
        <div class="flex flex-wrap justify-center gap-8">
          <!-- 作者 1 -->
          <a 
            href="https://github.com/ChuEating1005" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex items-center gap-2 hover:text-cyan-400 transition-colors"
          >
            <img 
              src="https://github.com/ChuEating1005.png" 
              alt="朱驛庭" 
              class="w-8 h-8 rounded-full"
            />
            <span>朱驛庭</span>
          </a>

          <!-- 作者 2 -->
          <a 
            href="https://github.com/Ray-Cheng-11" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex items-center gap-2 hover:text-cyan-400 transition-colors"
          >
            <img 
              src="https://github.com/Ray-Cheng-11.png" 
              alt="鄭睿宏" 
              class="w-8 h-8 rounded-full"
            />
            <span>鄭睿宏</span>
          </a>

          <!-- 作者 3 -->
          <a 
            href="https://github.com/Henry7090" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex items-center gap-2 hover:text-cyan-400 transition-colors"
          >
            <img 
              src="https://github.com/Henry7090.png" 
              alt="陳燁" 
              class="w-8 h-8 rounded-full"
            />
            <span>陳燁</span>
          </a>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          © 2024 NYCU Data Visualization. All rights reserved.
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>