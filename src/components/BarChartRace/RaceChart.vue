<template>
    <div class="flourish-embed flourish-bar-chart-race" :data-src="`visualisation/${chartId}`">
        <noscript>
            <img :src="`https://public.flourish.studio/visualisation/${chartId}/thumbnail`" width="100%" alt="bar-chart-race visualization" />
        </noscript>
    </div>
</template>

<script>
export default {
    props: ['chartId'],
    data() {
        return {
            flourishScript: null,
        }
    },
    methods: {
        loadFlourishEmbed() {
            // 移除舊的 script 如果存在
            if (this.flourishScript) {
                this.flourishScript.remove();
            }
            
            // 移除舊的 Flourish 實例
            if (window.FlourishLoaded) {
                delete window.FlourishLoaded;
            }
            
            // 創建並加載新的 script
            this.flourishScript = document.createElement('script');
            this.flourishScript.src = "https://public.flourish.studio/resources/embed.js";
            this.flourishScript.async = true;
            document.body.appendChild(this.flourishScript);
        }
    },
    watch: {
        chartId: {
            handler() {
                this.$nextTick(() => {
                    this.loadFlourishEmbed();
                });
            },
            immediate: true
        }
    },
    mounted() {
        this.loadFlourishEmbed();
    },
    beforeUnmount() {
        if (this.flourishScript) {
            this.flourishScript.remove();
        }
        if (window.FlourishLoaded) {
            delete window.FlourishLoaded;
        }
    }
}
</script>