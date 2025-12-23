<template>
  <button
    v-if="showButton"
    @click="scrollToTop"
    class="scroll-to-top-btn"
    aria-label="맨 위로 이동"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M18 15l-6-6-6 6"/>
    </svg>
    <span>TOP</span>
  </button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showButton = ref(false)

const handleScroll = () => {
  showButton.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
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
.scroll-to-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  
  width: 56px;
  height: 56px;
  padding: 0.5rem;
  
  background: linear-gradient(135deg, #2F80ED 0%, #FF4757 100%);
  color: #ffffff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(47, 128, 237, 0.3);
  
  cursor: pointer;
  transition: all 0.3s ease;
  
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.scroll-to-top-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
  background: linear-gradient(135deg, #FF4757 0%, #2F80ED 100%);
}

.scroll-to-top-btn:active {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(47, 128, 237, 0.3);
}

.scroll-to-top-btn svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
}

.scroll-to-top-btn span {
  line-height: 1;
  margin-top: -2px;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .scroll-to-top-btn {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 50px;
    height: 50px;
    font-size: 0.65rem;
  }
  
  .scroll-to-top-btn svg {
    width: 18px;
    height: 18px;
  }
}
</style>

