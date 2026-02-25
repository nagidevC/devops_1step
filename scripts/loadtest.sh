#!/bin/bash
# Нагрузочный тест для Task Manager
URL="http://localhost:5000/api/tasks"
echo "Начинаем нагрузку на $URL. Для остановки нажми Ctrl+C."
while true; do
    # Создаём задачу со случайным заголовком
    TITLE="load_$RANDOM"
    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"title\":\"$TITLE\",\"description\":\"test\"}" $URL > /dev/null
    # Получаем список задач
    curl -s $URL > /dev/null
    # Небольшая пауза, чтобы не перегрузить систему
    sleep 0.1
done
