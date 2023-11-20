from flask import Flask, render_template, request, jsonify
import requests
import re

class BuscadorCEP:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/buscar_endereco', methods=['GET'])
        def buscar_endereco():
            cep_ou_logradouro = request.args.get('cep_ou_logradouro')

            if len(cep_ou_logradouro) == 8 and cep_ou_logradouro.isdigit():
                resultado, status_code = self.buscar_endereco_por_cep(cep_ou_logradouro)
            else:
                resultado, status_code = self.buscar_endereco_por_logradouro(cep_ou_logradouro)

            if isinstance(resultado, dict):
                resultado_formatado = {
                    "endereco": resultado['endereco'],
                    "bairro": resultado['bairro'],
                    "localidade": resultado['localidade'],
                    "uf": resultado['uf'],
                    "cep": resultado['cep'],
                }
            else:
                resultado_formatado = {"endereco": resultado, "bairro": "", "localidade": "", "uf": "", "cep": ""}

            resultado_formatado["status_code"] = status_code

            return jsonify(resultado_formatado)

    @staticmethod
    def formatar_cep(cep):
        return f"{cep[:5]}-{cep[5:]}"

    @staticmethod
    def validar_cep(cep):
        return bool(cep.isdigit() and len(cep) == 8)

    @staticmethod
    def buscar_endereco(url):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'erro' in data:
                return {"endereco": "CEP inexistente.", "status_code": 200}
            endereco = {
                "endereco": f"{data['logradouro']}",
                "bairro": data['bairro'],
                "localidade": data['localidade'],
                "uf": data['uf'],
                "cep": BuscadorCEP.formatar_cep(data['cep'])
            }
            return endereco, 200
        else:
            return {"endereco": "CEP não encontrado.", "status_code": response.status_code}

    @staticmethod
    def buscar_endereco_por_cep(cep):
        if not BuscadorCEP.validar_cep(cep):
            return "Formato de CEP inválido (deve conter 8 dígitos).", 400

        url = f'https://viacep.com.br/ws/{cep}/json/'
        return BuscadorCEP.buscar_endereco(url)

    @staticmethod
    def buscar_endereco_por_logradouro(logradouro):
        url = f'https://viacep.com.br/ws/{logradouro}/json/'
        return BuscadorCEP.buscar_endereco(url)

    def run(self):
        self.app.run(debug=True, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    buscador_cep = BuscadorCEP()
    buscador_cep.run()
