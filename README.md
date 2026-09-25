# svoe-vino-scanner
Платформа «Своё Вино» — Модуль CV-сканера


🚀 Пошаговая инструкция запуска (Предварительный просмотр)
Чтобы протестировать этот код прямо сейчас на вашей машине:
Создайте файлы: Скопируйте код выше в соответствующие файлы в пустой папке svoe-vino-scanner.
Запустите инфраструктуру:
Откройте терминал в корне папки и выполните:
bash
1 docker-compose up --build
docker-compose up --build
Docker скачает образ pgvector, соберет FastAPI и Nuxt, и применит SQL-дамп.
Проверка UI (Frontend):
Откройте браузер (лучше в режиме эмуляции мобильного устройства через DevTools -> Toggle Device Toolbar) по адресу: http://localhost:3000.
Загрузите любую картинку. Вы увидите лоадер, а затем карточку вина «Винные краски, Шардоне» в стилистике портала.
Проверка API для оценочного скрипта (Backend):
В другом терминале выполните curl запрос, имитирующий работу Bash-скрипта кейсодержателя:
bash
1 curl -X POST http://localhost:8000/api/v1/evaluate \
2     -F "file=@./test_image.jpg"
curl -X POST http://localhost:8000/api/v1/evaluate \     -F "file=@./test_image.jpg"
Ожидаемый ответ (JSON):
1 {
2  "slug": "vinnye-kraski-shardone",
3  "confidence": 0.94,
4  "time_ms": 145.2
5 }
