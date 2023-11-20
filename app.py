from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

class BuscadorCEP:
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
                return "CEP inexistente.", 200
            endereco = f"{data['logradouro']} - {data['bairro']}, {data['localidade']} - {data['uf']}, {BuscadorCEP.formatar_cep(data['cep'])}"
            return endereco, 200
        else:
            return "CEP não encontrado.", response.status_code

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_endereco', methods=['GET'])
def buscar_endereco():
    cep_ou_logradouro = request.args.get('cep_ou_logradouro')

    if len(cep_ou_logradouro) == 8 and cep_ou_logradouro.isdigit():
        resultado, status_code = BuscadorCEP.buscar_endereco_por_cep(cep_ou_logradouro)
    else:
        resultado, status_code = BuscadorCEP.buscar_endereco_por_logradouro(cep_ou_logradouro)
        
    resultado = re.sub(r'(\d{5})-+(\d{3})', r'\1-\2', resultado)

    return jsonify({"resultado": resultado, "status_code": status_code})

if __name__ == '__main__':
    app.run(debug=True)
