from flask import Flask, request, current_app, render_template
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
        print '\n\r'
        time.sleep(5)
        atualizados.append({'id_usuario': user.getId(),
                            'nome': user.getNome(),
                            'cep': user.getCep()})
    return 'funcionou'


@app.route('/localiza/<int:id_usuario>')
def localiza_servicos(id_usuario, lista_servicos=[1, 2, 8]):
    sPersistencia = BuscaServicos()
    uPersistencia = UsuariosPersistencia()

    print 'Segue lista de funcionarios proximos a voce:'

    for srv in sPersistencia.buscarServicoProximo(
            usuario=uPersistencia.
            buscarUsuario(id_usuario=id_usuario),
            servicos=lista_servicos):

        print srv
        print '\n\r'


@app.route('/bd')
def bd():
    bd = Banco()
    bd.conectar()
    if bd.testar_conexao():
        return "Funcionou"
    else:
        return "estou chorando"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
