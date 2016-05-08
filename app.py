from flask import Flask, request, current_app, render_template, jsonify, make_response, json
from model.usuarios import UsuariosPersistencia
from model.BuscaServicos.buscaServicos import BuscaServicos
from model.DB.BancoDB import Banco
from controller.usuarios import Usuarios as UsuariosController
import json as pyjson
import time

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}))


@app.route('/')
def index():
    return "<h1 style='color: red'>webservice online.</h1>"


@app.route('/cadastra', methods=["PUT", "POST"])
def cadastra():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'erro': 'Necessario a requisicao ser em json'})
    else:
        campos_obrigatorios = ['id_tipo_usuario',
                               'nome',
                               'email',
                               'senha',
                               'latitude',
                               'longitude']

        # recebemos informacao em json
        print request.data
        dados = json.loads(request.data.replace("\"", "\'").
                           replace("\'", "\""))

        for c in campos_obrigatorios:
            if c not in dados.keys():
                return jsonify({'status': 0,
                                'msg': 'REQUEST INVALIDA.',
                                'data': request.data})

        self.usuarios = UsuariosController()

        res = self.usuarios.cadastrar_usuario(dados=dados)

        if res['status'] is True:
            # tudo ocorreu ok
            return jsonify({'status': 1,
                            'msg': 'Usuario cadastrado com sucesso.',
                            'data': res['dados']})
        else:
            return jsonify({'status': 0,
                            'msg': 'Parametros faltantes, dados nao gravados.',
                            'data': res['dados']})


@app.route('/atualiza_ceps')
def atualiza_ceps():
    uPersistencia = UsuariosPersistencia()
    atualizados = []

    for user in uPersistencia.buscaListaUsuarios():
        user.atualizar_cep(cep_novo=user.getCep())
        atualizados.append({'id_usuario': user.getId(),
                            'nome': user.getNome(),
                            'cep': user.getCep()})
        time.sleep(3)
    return jsonify({'atualizados': atualizados})


@app.route('/atualiza_localizacao/<int:id_usuario>/<float:latitude>/<float:longitude>')
def atualiza_localizacao(id_usuario, latitude, longitude):
    uPersistencia = UsuariosPersistencia()
    atualizados = []

    for user in uPersistencia.buscarUsuario(
            id_usuario=id_usuario):
        r = user.atualizar_cep_by_lat_long(lat_novo=latitude,
                                           long_novo=longitude)
        if r:
            atualizados.append({
                'status': 1,
                'id_usuario': user.getId(),
                'nome': user.getNome(),
                'cep': user.Cep(),
                'latitude': user.getLatitude(),
                'longitude': user.getLongitude()})
        else:
            atualizados.append({
                'status': 0,
                'id_usuario': user.getId()})

    if not atualizados:
        # se lista vazia, significa que nao foi encontrato usuario
        atualizados.append({'status': 0,
                            'id_usuario': 0})

    return jsonify({'atualizada': atualizados})


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


@app.route('/usuarios')
def gusuarios():
    return None


@app.route('/usuarios')
def cadastra_cliente():
    return None


@app.route('/bd')
def bd():
    bd = Banco()
    bd.conectar()
    if bd.testar_conexao():
        return "Banco conectado."
    else:
        return "N&atilde;o foi poss&iacute;vel se conectar ao banco."

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
