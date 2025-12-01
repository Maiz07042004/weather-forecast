# base image
FROM node:20

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

# serve static files using nginx
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
