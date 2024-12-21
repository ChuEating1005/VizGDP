<template>
    <div>
        <button @click="showHelp = true" class="help-button">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        </button>

        <!-- Help Modal -->
        <div v-if="showHelp" class="modal-overlay" @click="showHelp = false">
            <div class="modal-content" @click.stop>
                <h2 class="text-2xl font-bold mb-4">{{ title }}</h2>
                <hr class="my-4">
                <ul class="list-disc pl-6 space-y-3 text-left">
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
    @apply p-2 text-gray-600 hover:text-gray-800 transition-colors duration-200;
}

.modal-overlay {
    @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
    @apply bg-white p-6 rounded-lg shadow-xl max-w-md w-full mx-4;
}

.close-button {
    @apply mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors duration-200 w-full;
}
</style>
