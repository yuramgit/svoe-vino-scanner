from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import numpy as np
from ml_pipeline import preprocess_image, SigLIPMock

app = FastAPI(title="Своё Вино Scanner API")

# CORS для Nuxt Frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ml_model = SigLIPMock()

@app.post("/api/v1/evaluate")
async def evaluate_image(file: UploadFile = File(...)):
    """
    Эндпоинт для Bash-скрипта оценки кейсодержателя.
    Возвращает плоский JSON с slug.
    """
    start_time = time.time()
    
    # 1. Чтение и препроцессинг
    image_bytes = await file.read()
    processed_img = preprocess_image(image_bytes)
    
    # 2. Извлечение эмбеддинга
    embedding = ml_model.get_embedding(processed_img)
    
    # 3. Поиск в pgvector (Mock-логика для демонстрации)
    # В реальности: SELECT slug FROM wines ORDER BY embedding <-> %s LIMIT 1
    # Для теста возвращаем первый slug из БД
    mock_slug = "vinnye-kraski-shardone" 
    
    # Имитация отрыва Top-1 от Top-2 (Confidence)
    confidence = 0.94 
    
    process_time = (time.time() - start_time) * 1000
    
    # Требуемый формат для скрипта оценки
    return {
        "slug": mock_slug,
        "confidence": confidence,
        "time_ms": round(process_time, 2)
    }

@app.get("/api/v1/wine/{slug}")
async def get_wine_card(slug: str):
    """Получение данных для карточки вина (UI)"""
    # Mock response
    return {
        "slug": slug,
        "name": "Винные краски, Шардоне",
        "producer": "Дом Крымских Вин",
        "rating": 5.00,
        "description": "Свежее белое вино с нотами цитрусовых и белых цветов.",
        "pairing": ["Рыба", "Птица", "Сыры"]
    }