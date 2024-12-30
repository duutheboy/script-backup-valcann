import os
import shutil
from datetime import datetime, timedelta
import time

def get_file_info(filepath):
    """Obtém informações detalhadas de um arquivo."""
    stats = os.stat(filepath)
    created = datetime.fromtimestamp(stats.st_ctime)
    modified = datetime.fromtimestamp(stats.st_mtime)
    size = stats.st_size
    return {
        'name': os.path.basename(filepath),
        'size': size,
        'created': created,
        'modified': modified
    }

def log_file_info(file_info, log_file):
    """Registra as informações do arquivo no arquivo de log."""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Nome: {file_info['name']}\n")
        f.write(f"Tamanho: {file_info['size']} bytes\n")
        f.write(f"Data de Criação: {file_info['created'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Última Modificação: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")

def process_backups():
    """Função principal para processar os backups."""
    # Definindo caminhos
    source_dir = "/home/valcann/backupsFrom"
    dest_dir = "/home/valcann/backupsTo"
    source_log = "/home/valcann/backupsFrom.log"
    dest_log = "/home/valcann/backupsTo.log"

    # Criando diretório de destino se não existir
    os.makedirs(dest_dir, exist_ok=True)

    # Limpando logs anteriores
    for log_file in [source_log, dest_log]:
        if os.path.exists(log_file):
            os.remove(log_file)

    # Data limite para manter arquivos (3 dias atrás)
    cutoff_date = datetime.now() - timedelta(days=3)

    # Processando arquivos
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        
        # Ignorar se não for arquivo
        if not os.path.isfile(filepath):
            continue

        # Obtendo informações do arquivo
        file_info = get_file_info(filepath)
        
        # Registrando no log de origem
        log_file_info(file_info, source_log)

        # Verificando idade do arquivo
        if file_info['created'] > cutoff_date:
            # Arquivo é mais recente que 3 dias - copiar para destino
            dest_path = os.path.join(dest_dir, filename)
            shutil.copy2(filepath, dest_path)
            
            # Registrando no log de destino
            log_file_info(file_info, dest_log)
        else:
            # Arquivo é mais antigo que 3 dias - remover
            os.remove(filepath)

def main():
    try:
        process_backups()
        print("Processamento de backup concluído com sucesso!")
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
