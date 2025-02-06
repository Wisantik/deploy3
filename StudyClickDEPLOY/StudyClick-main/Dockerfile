# так же берём готовый контейнер с node на основе alpine
FROM node:18-alpine as build
# Задаем рабочий каталог
WORKDIR /usr/src/app
# Копируем туда наши json файлы
ADD *.json ./
# Устанавливаем все пакеты и зависимости указанные в json
RUN npm install

ADD ./public ./public
ADD ./src ./src

# FROM ngnix:stable-alpine

# COPY --from=build /dist /usr/share/nginx/html
# COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 3000
# CMD ["nginx", "-g", "daemon off;"]