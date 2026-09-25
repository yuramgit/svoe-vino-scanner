CREATE EXTENSION IF NOT EXISTS vector;

-- Таблица каталога вин
CREATE TABLE wines (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    producer VARCHAR(255),
    region VARCHAR(100),
    color VARCHAR(50),
    rating_roskachestvo DECIMAL(3,2),
    image_url TEXT,
    description TEXT
);

-- Векторная таблица для эмбеддингов SigLIP (размерность 768 или 1024)
CREATE TABLE wine_embeddings (
    id SERIAL PRIMARY KEY,
    wine_id INTEGER REFERENCES wines(id),
    embedding vector(768), 
    model_version VARCHAR(50) DEFAULT 'siglip-v1'
);

CREATE INDEX ON wine_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Тестовые данные (из парсинга HTML)
INSERT INTO wines (slug, name, producer, region, color, rating_roskachestvo, image_url) VALUES
('vinnye-kraski-shardone', 'Винные краски, Шардоне', 'Дом Крымских Вин', 'Крым', 'Белое', 5.00, 'https://api.vino-svoe.ru/v1/img/str-api/.../H4122_Vinnye_kraski_Shardone_2024_DKV_aa038d6d04.webp'),
('vinnye-kraski-sovignon-blan', 'Винные краски, Совиньон Блан', 'Дом Крымских Вин', 'Крым', 'Белое', 5.00, 'https://api.vino-svoe.ru/v1/img/str-api/.../H4121_Vinnye_kraski_Sovinon_Blan_2024_DKV_c067db407c.webp'),
('ulybka-vetra-merlo', 'Улыбка ветра, Мерло', 'Дом Крымских Вин', 'Крым', 'Красное', 5.00, 'https://api.vino-svoe.ru/v1/img/str-api/.../H4120_Ulybka_vetra_Merlo_2024_DKV_426a5f1726.webp');