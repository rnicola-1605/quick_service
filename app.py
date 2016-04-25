from flask import Flask, request, current_app, render_template
from controller.usuarios import Usuarios
from model.DB.BancoDB import Banco

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1 style='color: red'>Primeira funcao app QuickServices</h1>"

@app.route('/gusuarios')
def gusuarios():
    modulo = Usuarios(app)
    return modulo

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