<template>
  <div class="scanner-container">
    <header class="header">
      <img src="/svg/logo/svoe-vino-logo.svg" alt="Своё Вино" class="logo" />
      <h1>Найти своё вино</h1>
    </header>

    <div class="scan-area" v-if="!isLoading && !wineData">
      <p class="hint">Сфотографируйте этикетку или загрузите фото</p>
      <div class="camera-frame">
        <!-- Здесь будет компонент камеры или input type="file" -->
        <input type="file" accept="image/*" capture="environment" @change="handleUpload" class="upload-btn" />
        <span class="scan-icon">📷 Сканировать</span>
      </div>
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Анализируем этикетку...</p>
    </div>

    <!-- Карточка вина (Результат) -->
    <div v-if="wineData" class="wine-card">
      <img :src="wineData.image_url" :alt="wineData.name" class="wine-img" />
      <div class="wine-info">
        <h2>{{ wineData.name }}</h2>
        <p class="producer">{{ wineData.producer }}</p>
        <div class="rating">
          <span class="star">★</span> {{ wineData.rating }} <span class="roskach">Роскачество</span>
        </div>
        <p class="desc">{{ wineData.description }}</p>
        
        <!-- Кнопка удержания (Retention) -->
        <button class="sommelier-btn" @click="askSommelier">
          🍷 Спросить Цифрового Сомелье
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isLoading = ref(false)
const wineData = ref(null)

const handleUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isLoading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    // 1. Отправка в ML-пайплайн (оценочный эндпоинт)
    const evalRes = await $fetch('http://localhost:8000/api/v1/evaluate', {
      method: 'POST',
      body: formData
    })
    
    // 2. Получение полной карточки по slug
    const cardRes = await $fetch(`http://localhost:8000/api/v1/wine/${evalRes.slug}`)
    wineData.value = cardRes
    
  } catch (error) {
    console.error('Ошибка распознавания', error)
  } finally {
    isLoading.value = false
  }
}

const askSommelier = () => {
  // Открытие модалки с LLM-чатом (YandexGPT / GigaChat)
  alert('Открываем чат с Сомелье: К чему вы планируете подавать это вино?')
}
</script>

<style scoped>
/* Стилистика Своё Вино: темная тема, элегантные шрифты */
.scanner-container { font-family: 'Inter', sans-serif; background: #121212; color: #fff; min-height: 100vh; padding: 20px; }
.header { text-align: center; margin-bottom: 30px; }
.logo { height: 40px; margin-bottom: 10px; }
.camera-frame { border: 2px dashed #d4af37; border-radius: 16px; padding: 40px; text-align: center; position: relative; }
.upload-btn { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
.scan-icon { font-size: 24px; color: #d4af37; }
.wine-card { background: #1e1e1e; border-radius: 20px; overflow: hidden; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.wine-img { width: 100%; height: 300px; object-fit: cover; }
.wine-info { padding: 20px; }
.rating { color: #d4af37; font-weight: bold; margin: 10px 0; }
.sommelier-btn { width: 100%; padding: 15px; background: #8b0000; color: white; border: none; border-radius: 12px; font-size: 16px; margin-top: 20px; font-weight: 600; }
</style>