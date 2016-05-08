from flask import Flask, request, current_app, render_template, jsonify, make_response, json
from model.usuarios import UsuariosPersistencia
from model.BuscaServicos.buscaServicos import BuscaServicos
from model.DB.BancoDB import Banco
from controller.usuarios import Usuarios as UsuariosController
from controller.servicos import Servicos as ServicosController
import json as pyjson
import time

app = Flask(__name__)

# instancia controller usuarios
usuarios = UsuariosController()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}))


@app.route('/')
def index():
    return "<h1 style='color: red'>webservice online.</h1>"


@app.route('/cadastra', methods=["PUT", "POST", "GET"])
def cadastra():
    """
    REQUISICAO APENAS EM JSON

    adiciona um novo tipo de usuario
    """

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
        dados = json.loads(request.data.replace("\"", "\'").
                           replace("\'", "\""))

        for c in campos_obrigatorios:
            if c not in dados.keys():
                return jsonify(
                    {'status': 0,
                     'msg': 'REQUEST INVALIDA, PARAM ' +
                     'INVALIDOS OU FALTANTES',
                     'data': [nc for nc in campos_obrigatorios if
                              nc not in dados.keys()]})

        res = usuarios.cadastrar_usuario(dados=dados)

        if res['status'] is True:
            # tudo ocorreu ok
            return jsonify({'status': 1,
                            'msg': res['msg'],
                            'data': res['dados']})
        else:
            return jsonify({'status': 0,
                            'msg': res['msg'],
                            'data': res['dados']})


@app.route('/adiciona_servico', methods=["PUT", "POST", "GET"])
def adiciona_servico():
    """
    REQUISICAO APENAS JSON

    adiciona um servico que um prestador pode prestar.
    apenas usuarios do tipo = 1 (prestador) podem utilizar esse metodo
    """

    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'erro': 'Necessario a requisicao ser em json'})
    else:
        campos_obrigatorios = ['id_usuario', 'id_servico']

        # recebemos informacao em json
        dados = json.loads(request.data.replace("\"", "\'").
                           replace("\'", "\""))

        for c in campos_obrigatorios:
            if c not in dados.keys():
                return jsonify(
                    {'status': 0,
                     'msg': 'REQUEST INVALIDA, PARAM ' +
                     'INVALIDOS OU FALTANTES',
                     'data': [nc for nc in campos_obrigatorios if
                              nc not in dados.keys()]})

        res = usuarios.adiciona_servico(dados=dados)

        if res['status'] is True:
            # tudo ocorreu ok
            return jsonify({'status': 1,
                            'msg': res['msg'],
                            'data': res['dados']})
        else:
            return jsonify({'status': 0,
                            'msg': res['msg'],
                            'data': res['dados']})


@app.route('/deleta_servico', methods=["PUT", "POST", "GET"])
def deleta_servico():
    """
    REQUISICAO APENAS JSON

    deleta um servico que um prestador pode prestar.
    apenas usuarios do tipo = 1 (prestador) podem utilizar esse metodo
    """

    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'erro': 'Necessario a requisicao ser em json'})
    else:
        campos_obrigatorios = ['id_usuario', 'id_servico']

        # recebemos informacao em json
        dados = json.loads(request.data.replace("\"", "\'").
                           replace("\'", "\""))

        for c in campos_obrigatorios:
            if c not in dados.keys():
                return jsonify(
                    {'status': 0,
                     'msg': 'REQUEST INVALIDA, PARAM ' +
                     'INVALIDOS OU FALTANTES',
                     'data': [nc for nc in campos_obrigatorios if
                              nc not in dados.keys()]})

        res = usuarios.deleta_servico(dados=dados)

        if res['status'] is True:
            # tudo ocorreu ok
            return jsonify({'status': 1,
                            'msg': res['msg'],
                            'data': res['dados']})
        else:
            return jsonify({'status': 0,
                            'msg': res['msg'],
                            'data': res['dados']})


@app.route('/lista_servicos')
@app.route('/lista_servicos/<int:id_tipo_servico>')
def lista_servicos(id_tipo_servico=None):
    """
    Lista todos os servicos disponiveis
    """

    # instancia controller de servicos
    servs = ServicosController()

    res = servs.buscar_servicos(id_tipo_servico=id_tipo_servico)
    if res and len(res) > 0:
        return jsonify({'status': 1,
                        'lista': res})
    else:
        return jsonify({'status': 0,
                        'lista': res})


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
