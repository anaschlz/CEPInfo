from flask import jsonify, render_template, request
from models.buscador_cep import BuscadorCEP

def index():
    return render_template('index.html')

def buscar_endereco():
    cep_ou_logradouro = request.args.get('cep_ou_logradouro')
    resultado, status_code = BuscadorCEP.buscar_endereco_por_CEP(cep_ou_logradouro)
    resultado_formatado = BuscadorCEP.formatar_resultado(resultado, status_code)
    return jsonify(resultado_formatado), status_code
