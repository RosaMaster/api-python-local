import os
import sys
from flask import Flask
from flasgger import Swagger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Adicionar o diretório pai ao path para importações absolutas

from app.controller.cadastrar_cliente import clientes_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(clientes_bp)   # Registrar blueprints

# Criar diretório de dados se não existir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)


@app.route('/home', methods=['GET'])
def home():
    # """ ROTA HOME DA API
    # ---
    # responses:
    #   200:
    #     description: BEM-VINDO À MINHA API
    # """
    return {"mensagem": "BEM-VINDO A MINHA PRIMEIRA API LOCAL"}, 200


if __name__ == '__main__':
    app.run(debug=True)
