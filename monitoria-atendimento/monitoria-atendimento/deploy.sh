#!/bin/bash

# Script de Deploy Automatizado - Sistema de Monitoria de Atendimento
# Este script facilita o deploy e gerenciamento da aplicação

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    print_success "Docker e Docker Compose estão instalados"
}

# Verificar arquivo .env
check_env_file() {
    if [ ! -f .env ]; then
        print_warning "Arquivo .env não encontrado. Criando a partir do .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "Por favor, edite o arquivo .env com suas configurações antes de continuar"
            exit 0
        else
            print_error "Arquivo .env.example não encontrado"
            exit 1
        fi
    fi
    print_success "Arquivo .env encontrado"
}

# Build das imagens
build_images() {
    print_info "Construindo imagens Docker..."
    docker-compose build --no-cache
    print_success "Imagens construídas com sucesso"
}

# Iniciar serviços
start_services() {
    print_info "Iniciando serviços..."
    docker-compose up -d
    print_success "Serviços iniciados"
}

# Parar serviços
stop_services() {
    print_info "Parando serviços..."
    docker-compose down
    print_success "Serviços parados"
}

# Reiniciar serviços
restart_services() {
    print_info "Reiniciando serviços..."
    docker-compose restart
    print_success "Serviços reiniciados"
}

# Ver logs
view_logs() {
    SERVICE=${1:-}
    if [ -z "$SERVICE" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$SERVICE"
    fi
}

# Status dos serviços
check_status() {
    print_info "Status dos serviços:"
    docker-compose ps
}

# Inicializar banco de dados
init_database() {
    print_info "Inicializando banco de dados com dados de exemplo..."
    docker-compose exec backend python3 init_db.py
    print_success "Banco de dados inicializado"
}

# Backup do banco de dados
backup_database() {
    BACKUP_DIR="./backups"
    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"
    
    print_info "Criando backup do banco de dados..."
    docker-compose exec -T database pg_dump -U postgres monitoria_atendimento > "$BACKUP_FILE"
    print_success "Backup criado: $BACKUP_FILE"
}

# Restaurar banco de dados
restore_database() {
    if [ -z "$1" ]; then
        print_error "Por favor, especifique o arquivo de backup"
        echo "Uso: $0 restore <arquivo_backup.sql>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Arquivo de backup não encontrado: $1"
        exit 1
    fi
    
    print_warning "ATENÇÃO: Isso irá sobrescrever o banco de dados atual!"
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Operação cancelada"
        exit 0
    fi
    
    print_info "Restaurando banco de dados..."
    docker-compose exec -T database psql -U postgres monitoria_atendimento < "$1"
    print_success "Banco de dados restaurado"
}

# Limpar tudo (incluindo volumes)
clean_all() {
    print_warning "ATENÇÃO: Isso irá remover todos os containers, imagens e volumes!"
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Operação cancelada"
        exit 0
    fi
    
    print_info "Removendo tudo..."
    docker-compose down -v --rmi all
    print_success "Limpeza concluída"
}

# Deploy completo
full_deploy() {
    print_info "Iniciando deploy completo..."
    check_docker
    check_env_file
    build_images
    start_services
    sleep 10
    init_database
    check_status
    print_success "Deploy completo finalizado!"
    print_info "Acesse a aplicação em: http://localhost"
    print_info "API disponível em: http://localhost:5000/api"
}

# Menu de ajuda
show_help() {
    echo "Sistema de Monitoria de Atendimento - Script de Deploy"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  deploy          - Deploy completo (build + start + init db)"
    echo "  build           - Construir imagens Docker"
    echo "  start           - Iniciar serviços"
    echo "  stop            - Parar serviços"
    echo "  restart         - Reiniciar serviços"
    echo "  status          - Ver status dos serviços"
    echo "  logs [serviço]  - Ver logs (opcional: backend, frontend, database)"
    echo "  init-db         - Inicializar banco de dados com dados de exemplo"
    echo "  backup          - Criar backup do banco de dados"
    echo "  restore <file>  - Restaurar banco de dados de um backup"
    echo "  clean           - Remover tudo (containers, imagens, volumes)"
    echo "  help            - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 deploy                    # Deploy completo"
    echo "  $0 logs backend              # Ver logs do backend"
    echo "  $0 restore backups/backup.sql # Restaurar backup"
}

# Processar comando
case "${1:-help}" in
    deploy)
        full_deploy
        ;;
    build)
        check_docker
        build_images
        ;;
    start)
        check_docker
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs "$2"
        ;;
    init-db)
        init_database
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "$2"
        ;;
    clean)
        clean_all
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Comando desconhecido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
