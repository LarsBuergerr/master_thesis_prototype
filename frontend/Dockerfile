# Frontend image — Vite build served by nginx, which also proxies /api to the
# backend service (same-origin, so no CORS setup needed).
# Build context is the frontend/ directory.
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Baked into the bundle at build time: route API calls through the nginx proxy.
ARG VITE_API_BASE=/api
ENV VITE_API_BASE=$VITE_API_BASE
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
