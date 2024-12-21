<template>
    <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/20144600">
        <noscript>
            <img src="https://public.flourish.studio/visualisation/20144600/thumbnail" width="100%" alt="bar-chart-race visualization" />
        </noscript>
    </div>
</template>

<script>
export default {
    data() {
        return {
            flourishScript: null
        }
    },
    methods: {
        loadFlourishEmbed() {
            // 移除舊的 script 如果存在
            if (this.flourishScript) {
                this.flourishScript.remove();
            }
            
            // 創建並加載新的 script
            this.flourishScript = document.createElement('script');
            this.flourishScript.src = "https://public.flourish.studio/resources/embed.js";
            this.flourishScript.async = true;
            document.body.appendChild(this.flourishScript);
        }
    },
    mounted() {
        this.loadFlourishEmbed();
    },
    activated() {
        // 當組件被 keep-alive 重新激活時調用
        this.loadFlourishEmbed();
    },
    deactivated() {
        // 當組件被 keep-alive 停用時調用
        if (this.flourishScript) {
            this.flourishScript.remove();
        }
    }
}
</script>