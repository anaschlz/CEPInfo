from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

class BuscadorCEP:
    @staticmethod
    def formatar_resultado(resultado, status_code):
        mensagens_erro = {
            400: "Formato de CEP inválido (deve conter 8 dígitos).",
            404: "CEP não encontrado.",
        }

        resultado_formatado = {
            "endereco": resultado.get('endereco', ""),
            "bairro": resultado.get('bairro', ""),
            "localidade": resultado.get('localidade', ""),
            "uf": resultado.get('uf', ""),
            "cep": BuscadorCEP.formatar_cep(resultado.get('cep', ""))
        }

        resultado_formatado["status_code"] = status_code
        resultado_formatado["mensagem"] = mensagens_erro.get(status_code, "")

        return resultado_formatado

    @staticmethod
    def formatar_cep(cep):
        return f"{cep[:5]}{cep[5:]}"

    @staticmethod
    def validar_cep(cep):
        return bool(cep.isdigit() and len(cep) == 8)

    @staticmethod
    def buscar_endereco(url):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'erro' in data:
                return {"mensagem": "CEP inexistente."}, 404
            endereco = {
                "endereco": data.get('logradouro', ""),
                "bairro": data.get('bairro', ""),
                "localidade": data.get('localidade', ""),
                "uf": data.get('uf', ""),
                "cep": BuscadorCEP.formatar_cep(data.get('cep', ""))
            }
            return endereco, 200
        else:
            return {"endereco": "CEP não encontrado."}, response.status_code

    @staticmethod
    def buscar_endereco_por_CEP(cep):
        if not BuscadorCEP.validar_cep(cep):
            return "Formato de CEP inválido (deve conter 8 dígitos).", 400

        url = f'https://viacep.com.br/ws/{cep}/json/'
        return BuscadorCEP.buscar_endereco(url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_endereco', methods=['GET'])
def buscar_endereco():
    cep_ou_logradouro = request.args.get('cep_ou_logradouro')
    resultado, status_code = BuscadorCEP.buscar_endereco_por_CEP(cep_ou_logradouro)
    resultado_formatado = BuscadorCEP.formatar_resultado(resultado, status_code)
    return jsonify(resultado_formatado), status_code

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
