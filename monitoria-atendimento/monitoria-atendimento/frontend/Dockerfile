# Dockerfile para Frontend React (Multi-stage build)

# Estágio 1: Build
FROM node:22-alpine AS builder

WORKDIR /app

# Copiar arquivos de dependências
COPY package.json pnpm-lock.yaml ./

# Instalar pnpm e dependências
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copiar código fonte
COPY . .

# Argumento de build para URL da API
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Build da aplicação para produção
RUN pnpm build

# Estágio 2: Servidor Nginx
FROM nginx:alpine

# Copiar arquivos buildados do estágio anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta 80
EXPOSE 80

# Comando padrão do Nginx
CMD ["nginx", "-g", "daemon off;"]
