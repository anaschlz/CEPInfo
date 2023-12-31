from flask import Flask, render_template, request, jsonify
from controllers.cep_controller import index, buscar_endereco
from models.buscador_cep import BuscadorCEP

app = Flask(__name__)

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
