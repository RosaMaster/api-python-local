import json
import os
import sys
import logging
from flask import Blueprint, jsonify, request
from faker import Faker
from app.model.cliente import Cliente
from app.utils.data_utils import ler_dados, salvar_dados

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))   # Adicionar o diretório src ao path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

clientes_bp = Blueprint('clientes', __name__, url_prefix='/api')
fake = Faker('pt_BR')   # Incializar Faker com dados pt-BR


@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """ Obter lista de clientes.
    ---
    responses:
      200:
        description: Uma lista de clientes do arquivo JSON
    """

    try:
        clientes = ler_dados()
        logger.info(f"Listagem de clientes solicitada - Total: {len(clientes)}")
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {str(e)}")
        return jsonify({"erro": "Erro ao listar clientes"}), 500
    

# Rota para obter um cliente específico
@clientes_bp.route('/clientes/<cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """ Obter um cliente específico pelo GUID.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Dados do cliente
      404:
        description: Cliente não encontrado
    """

    try:
        clientes = ler_dados()
        for cliente in clientes:
            if cliente.id == cliente_id:
                logger.info(f"Cliente {cliente_id} consultado")
                return jsonify(cliente.to_dict()), 200
        
        logger.warning(f"Cliente {cliente_id} não encontrado")
        return jsonify({"erro": "Cliente não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar cliente {cliente_id}: {str(e)}")
        return jsonify({"erro": "Erro ao consultar cliente"}), 500


@clientes_bp.route('/clientes', methods=['POST'])     #TODO: Implementar entradade dados via body
def criar_cliente():
    """ Cadastrar novo cliente.
    ---
    responses:
      201:
        description: Cliente salvo com sucesso!
    """

    try:
        novo_cliente = Cliente(
            nome=fake.name(),
            cpf=fake.cpf(),
            email=fake.email(),
            telefone=fake.phone_number(),
            endereco=fake.address()
        )

        clientes = ler_dados()
        clientes.append(novo_cliente)
        salvar_dados(clientes)
        
        logger.info(f"Novo cliente criado: {novo_cliente.id} - {novo_cliente.nome}")
        return jsonify(novo_cliente.to_dict()), 201
    except Exception as e:
        logger.error(f"Erro ao criar cliente: {str(e)}")
        return jsonify({"erro": "Erro ao criar cliente"}), 500


@clientes_bp.route('/clientes/<cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """ Atualizar dados de um cliente pelo GUID.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            email:
              type: string
            telefone:
              type: string
            endereco:
              type: string
    responses:
      200:
        description: Cliente atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Cliente não encontrado
    """

    if not request.json:
        logger.warning(f"Tentativa de atualizar cliente {cliente_id} sem dados")
        return jsonify({"erro": "Dados de atualização não fornecidos"}), 400
    
    clientes = ler_dados()
    for cliente in clientes:
        if cliente.id == cliente_id:
            try:
                cliente.atualizar(**request.json)
                salvar_dados(clientes)
                logger.info(f"Cliente {cliente_id} atualizado com sucesso")
                return jsonify(cliente.to_dict()), 200
            except ValueError as e:
                logger.error(f"Erro ao atualizar cliente {cliente_id}: {str(e)}")
                return jsonify({"erro": str(e)}), 400
    
    logger.warning(f"Cliente {cliente_id} não encontrado para atualização")
    return jsonify({"erro": "Cliente não encontrado"}), 404


@clientes_bp.route('/clientes/<cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """ Deletar um cliente pelo GUID.
    ---
    parameters:
      - name: cliente_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Cliente deletado com sucesso
      404:
        description: Cliente não encontrado
    """

    clientes = ler_dados()
    for i, cliente in enumerate(clientes):
        if cliente.id == cliente_id:
            removido = clientes.pop(i)
            salvar_dados(clientes)
            logger.info(f"Cliente {cliente_id} deletado com sucesso")
            return jsonify({"mensagem": "Cliente deletado com sucesso", "cliente": removido.to_dict()}), 200
    
    logger.warning(f"Cliente {cliente_id} não encontrado para deleção")

    return jsonify({"erro": "Cliente não encontrado"}), 404


@clientes_bp.route('/clientes/seed/<int:quantidade>', methods=['POST'])     #TODO: Implementar entradade dados via body
def seed_clientes(quantidade: int):
    """ Cadastrar múltiplos clientes.
    ---
    parameters:
      - name: quantidade
        in: path
        type: integer
        required: true
        description: Quantidade de clientes a gerar
    responses:
      201:
        description: Clientes gerados com sucesso
      400:
        description: Quantidade inválida
    """
    
    if quantidade <= 0 or quantidade > 1000:
        logger.warning(f"Tentativa de seed com quantidade inválida: {quantidade}")
        return jsonify({"erro": "Quantidade deve estar entre 1 e 1000"}), 400
    
    try:
        clientes_gerados = []
        clientes = ler_dados()
        
        for _ in range(quantidade):
            novo_cliente = Cliente(
                nome=fake.name(),
                cpf=fake.cpf(),
                email=fake.email(),
                telefone=fake.phone_number(),
                endereco=fake.address()
            )
            clientes.append(novo_cliente)
            clientes_gerados.append(novo_cliente.to_dict())
        
        salvar_dados(clientes)
        
        logger.info(f"Seed executado: {quantidade} clientes gerados")
        return jsonify({
            "mensagem": f"{quantidade} clientes gerados com sucesso",
            "quantidade": quantidade,
            "total_clientes": len(clientes),
            "clientes": clientes_gerados
        }), 201
    except Exception as e:
        logger.error(f"Erro durante seed: {str(e)}")
        return jsonify({"erro": "Erro ao gerar clientes fake"}), 500
