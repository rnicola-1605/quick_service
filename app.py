from flask import Flask, request, current_app, render_template, jsonify
from model.usuarios import UsuariosPersistencia
from model.BuscaServicos.buscaServicos import BuscaServicos
from model.DB.BancoDB import Banco
import json
import time

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1 style='color: red'>Primeira funcao app QuickServices</h1>"


@app.route('/usuarios')
def gusuarios():
    return None


@app.route('/usuarios')
def cadastra_cliente():
    return None


@app.route('/cadastra')
def cadastra():
    return None


@app.route('/atualiza_ceps')
def atualiza_ceps():
    uPersistencia = UsuariosPersistencia()
    atualizados = []

    for user in uPersistencia.buscaListaUsuarios():
        user.atualizar_cep(cep_novo=user.getCep())
        print user.getToString()
        print '\n'
        time.sleep(5)
        atualizados.append({'id_usuario': user.getId(),
                            'nome': user.getNome(),
                            'cep': user.getCep()})
    return jsonify({'atualizados': atualizados})


@app.route('/localiza/<int:id_usuario>/<int:lista_servicos>')
@app.route('/localiza/<float:latitude>/<float:longitude>')
@app.route('/localiza/<float:latitude>/<float:longitude>/<int:lista_servicos>')
def localiza_servicos(id_usuario=None, latitude=None,
                      longitude=None, lista_servicos=[1, 2, 8]):
    sPersistencia = BuscaServicos()
    uPersistencia = UsuariosPersistencia()
    resultado = []

    if isinstance(lista_servicos, int):
        lista_servicos = [lista_servicos]

    for srv in sPersistencia.buscarServicoProximo(
            usuario=uPersistencia.
            buscarUsuario(id_usuario=id_usuario),
            servicos=lista_servicos):

        resultado.append({
            'nome': srv['nome'],
            'id_servico': srv['id_servico'],
            'servico': srv['servico'].decode('iso-8859-1').
            encode('utf-8')})

    return jsonify({'servicos': resultado})


@app.route('/bd')
def bd():
    bd = Banco()
    bd.conectar()
    if bd.testar_conexao():
        return "Funcionou"
    else:
        return "Nao funcionou (estou chorando)"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
