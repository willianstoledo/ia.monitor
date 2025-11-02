.PHONY: help deploy build start stop restart status logs logs-backend logs-frontend logs-db init-db backup clean

help:
	@echo "Sistema de Monitoria de Atendimento - Comandos Make"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make deploy        - Deploy completo (build + start + init db)"
	@echo "  make build         - Construir imagens Docker"
	@echo "  make start         - Iniciar serviços"
	@echo "  make stop          - Parar serviços"
	@echo "  make restart       - Reiniciar serviços"
	@echo "  make status        - Ver status dos serviços"
	@echo "  make logs          - Ver todos os logs"
	@echo "  make logs-backend  - Ver logs do backend"
	@echo "  make logs-frontend - Ver logs do frontend"
	@echo "  make logs-db       - Ver logs do banco de dados"
	@echo "  make init-db       - Inicializar banco com dados de exemplo"
	@echo "  make backup        - Criar backup do banco de dados"
	@echo "  make clean         - Remover containers e volumes"

deploy:
	./deploy.sh deploy

build:
	./deploy.sh build

start:
	./deploy.sh start

stop:
	./deploy.sh stop

restart:
	./deploy.sh restart

status:
	./deploy.sh status

logs:
	./deploy.sh logs

logs-backend:
	./deploy.sh logs backend

logs-frontend:
	./deploy.sh logs frontend

logs-db:
	./deploy.sh logs database

init-db:
	./deploy.sh init-db

backup:
	./deploy.sh backup

clean:
	./deploy.sh clean
