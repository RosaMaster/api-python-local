#!/usr/bin/env python
"""
Script para gerar dados fake e popular o banco de dados
"""
import os
import sys
import json
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.model.cliente import Cliente
from app.utils.data_utils import ler_dados, salvar_dados, DATA_FILE
from faker import Faker

fake = Faker('pt_BR')


def gerar_clientes_fake(quantidade=10):
    """
    Gera e salva múltiplos clientes fake
    
    Args:
        quantidade: Número de clientes a gerar
    """
    print(f"🔄 Gerando {quantidade} clientes fake...")
    
    clientes = ler_dados()
    clientes_novos = []
    
    for i in range(quantidade):
        cliente = Cliente(
            nome=fake.name(),
            cpf=fake.cpf(),
            email=fake.email(),
            telefone=fake.phone_number(),
            endereco=fake.address()
        )
        clientes.append(cliente)
        clientes_novos.append(cliente)
        print(f"  ✓ Cliente {i+1}/{quantidade} gerado: {cliente.nome}")
    
    salvar_dados(clientes)
    print(f"\n✅ {quantidade} clientes salvos com sucesso!")
    print(f"📁 Arquivo: {DATA_FILE}")
    print(f"📊 Total de clientes: {len(clientes)}")
    
    return clientes_novos


def limpar_dados():
    """Limpa todos os dados"""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        print("🗑️  Dados removidos com sucesso!")
    else:
        print("❌ Nenhum arquivo de dados encontrado")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerar dados fake para a API')
    parser.add_argument('-q', '--quantidade', type=int, default=10, 
                        help='Quantidade de clientes a gerar (padrão: 10)')
    parser.add_argument('-l', '--limpar', action='store_true',
                        help='Limpar todos os dados')
    
    args = parser.parse_args()
    
    if args.limpar:
        limpar_dados()
    else:
        if args.quantidade < 1 or args.quantidade > 1000:
            print("❌ Quantidade deve estar entre 1 e 1000")
            sys.exit(1)
        
        gerar_clientes_fake(args.quantidade)
