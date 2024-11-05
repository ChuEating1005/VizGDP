<template>
    <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/20144600">
        <noscript>
            <img src="https://public.flourish.studio/visualisation/20144600/thumbnail" width="100%" alt="bar-chart-race visualization" />
        </noscript>
    </div>
</template>

<script>
export default {
    mounted() {
        const script = document.createElement('script');
        script.src = "https://public.flourish.studio/resources/embed.js";
        script.async = true;
        document.body.appendChild(script);
    }
}
</script>