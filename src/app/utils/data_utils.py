import json
import os
from app.model.cliente import Cliente

# Definir caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # src
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'dados.json')

os.makedirs(DATA_DIR, exist_ok=True)

def ler_dados() -> list:
    """
    Lê dados do arquivo JSON e retorna lista de objetos Cliente

    Returns:
        Lista de clientes
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        dados_json = json.load(f)
        return [Cliente.from_dict(cliente) for cliente in dados_json]

def salvar_dados(clientes: list) -> None:
    """
    Salva lista de objetos Cliente no arquivo JSON

    Args:
        clientes: Lista de clientes a serem salvos
    """
    dados_json = [cliente.to_dict() for cliente in clientes]
    with open(DATA_FILE, 'w') as f:
        json.dump(dados_json, f, indent=4)

__all__ = ['ler_dados', 'salvar_dados', 'DATA_FILE']