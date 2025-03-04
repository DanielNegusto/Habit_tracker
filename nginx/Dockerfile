# Используем официальный образ nginx
FROM nginx:alpine

# Копируем файл конфигурации
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем содержимое директории html в nginx
COPY html /usr/share/nginx/html