#!/usr/bin/env python
"""
Arquivo para executar a aplicação Flask
"""
import os
import sys

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.main import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
