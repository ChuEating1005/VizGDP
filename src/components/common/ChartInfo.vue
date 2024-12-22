<template>
    <div>
        <button @click="showHelp = true" class="help-button">
            <div class="bg-white rounded-full p-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="black" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
        </button>

        <!-- Help Modal -->
        <div v-if="showHelp" class="modal-overlay" @click="showHelp = false">
            <div class="modal-content" @click.stop>
                <h2 class="text-2xl font-bold mb-4 text-cyan-500 text-center">{{ title }}</h2>
                <hr class="my-4 border-slate-700">
                <ul class="instruction-list">
                    <slot></slot>
                </ul>
                <button @click="showHelp = false" class="close-button">
                    Close
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['title'],
    data() {
        return {
            showHelp: false,
        }
    }
}
</script>

<style scoped>
.help-button {
    @apply p-2 hover:opacity-80 transition-opacity duration-200;
}

.modal-overlay {
    @apply fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 backdrop-blur-sm;
}

.modal-content {
    @apply bg-white p-6 rounded-lg shadow-xl max-w-xl w-full mx-4 text-black;
    max-height: 80vh;
    overflow-y: auto;
}

.instruction-list {
    @apply space-y-4;
}

.instruction-list :deep(li) {
    @apply pl-4 text-left;
}

.instruction-list :deep(strong) {
    @apply text-lg font-semibold mb-2 block text-center;
}

.instruction-list :deep(strong:contains("Region Selection")) {
    @apply text-emerald-400;
}

.instruction-list :deep(strong:contains("Data Visualization")) {
    @apply text-cyan-400;
}

.instruction-list :deep(strong:contains("Interactive Features")) {
    @apply text-blue-400;
}

.instruction-list :deep(strong:contains("Color Coding")) {
    @apply text-purple-400;
}

.instruction-list :deep(ul) {
    @apply bg-gray-200/50 rounded-lg list-disc p-4 pl-8 space-y-2 mt-2;
}

.close-button {
    @apply mt-4 px-4 py-2 bg-cyan-600 text-white rounded-lg 
           hover:bg-cyan-500 transition-colors duration-200 w-full
           font-semibold tracking-wide;
}

/* Color coding circles */
.instruction-list :deep(.color-dot) {
    @apply w-3 h-3 rounded-full inline-block mr-2;
}

.instruction-list :deep(.region-colors) {
    @apply grid grid-cols-3 gap-3 mt-2;
}

.instruction-list :deep(.region-item) {
    @apply flex items-center gap-2;
}
</style>
