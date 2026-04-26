import uuid
from typing import Dict, Optional
from datetime import datetime


class Cliente:
    """
    Classe que representa um Cliente
    """

    def __init__(
        self,
        nome: str,
        cpf: str,
        email: str,
        telefone: str,
        endereco: str,
        cliente_id: Optional[str] = None,
        data_cadastro: Optional[datetime] = None,
        data_atualizacao: Optional[datetime] = None
    ):
        """
        Inicializa um novo cliente

        Args:
            nome: Nome do cliente
            cpf: CPF do cliente
            email: Email do cliente
            telefone: Telefone do cliente
            endereco: Endereço do cliente
            cliente_id: ID do cliente (gerado automaticamente se não fornecido)
            data_cadastro: Data de cadastro do cliente (atual se não fornecido)
            data_atualizacao: Data de atualização do cliente (atual se não fornecido)
        """
        self.id = cliente_id or str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.data_cadastro = data_cadastro or datetime.now()
        self.data_atualizacao = data_atualizacao or datetime.now()


    def to_dict(self) -> Dict:
        """ Converte o cliente para dicionário.
        Returns:
            Type: Dicionário com os dados do cliente: {id, nome, cpf, email, telefone, endereco, data_cadastro, data_atualizacao}
        """

        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }


    @classmethod
    def from_dict(cls, dados: Dict) -> 'Cliente':
        """ Cria um cliente a partir de um dicionário.
        Args:
            dados: Dicionário com os dados do cliente
        Returns:
            Instância da classe Cliente
        """
        
        data_cadastro_val = dados.get('data_cadastro')
        data_cadastro = datetime.fromisoformat(data_cadastro_val) if isinstance(data_cadastro_val, str) else data_cadastro_val
        
        data_atualizacao_val = dados.get('data_atualizacao')
        data_atualizacao = datetime.fromisoformat(data_atualizacao_val) if isinstance(data_atualizacao_val, str) else data_atualizacao_val
        
        return cls(
            cliente_id=dados.get('id'),
            nome=dados.get('nome'),
            cpf=dados.get('cpf'),
            email=dados.get('email'),
            telefone=dados.get('telefone'),
            endereco=dados.get('endereco'),
            data_cadastro=data_cadastro,
            data_atualizacao=data_atualizacao
        )


    def __repr__(self) -> str:
        """ Representação em string do cliente
        Returns:
            String representando o cliente
        """

        data_cadastro_str = self.data_cadastro.isoformat() if self.data_cadastro else None
        data_atualizacao_str = self.data_atualizacao.isoformat() if self.data_atualizacao else None
        
        return f"Cliente(id='{self.id}', nome='{self.nome}', cpf='{self.cpf}', email='{self.email}', telefone='{self.telefone}', endereco='{self.endereco}', data_cadastro='{data_cadastro_str}', data_atualizacao='{data_atualizacao_str}')"


    def __eq__(self, outro: object) -> bool:
        """ Verifica se dois clientes são iguais.
        Args:
            outro: Outro objeto para comparação
        Returns:
            True se os clientes forem iguais, False caso contrário.
        """

        if not isinstance(outro, Cliente):
            return False
        
        return self.id == outro.id
    

    def atualizar(self, **kwargs) -> None:
        """ Atualiza os dados do cliente.
        Args:
            **kwargs: Atributos a serem atualizados
        Returns:
            None
        """

        atributos_permitidos = {'nome', 'email', 'telefone', 'endereco'}

        for chave, valor in kwargs.items():
            if chave in atributos_permitidos:
                setattr(self, chave, valor)
            else:
                raise ValueError(f"Atributo '{chave}' não permitido")
        
        self.data_atualizacao = datetime.now()
