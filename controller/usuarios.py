from flask import Flask, request, current_app, render_template

class Usuarios(object):
    """
    Classe controller para usuarios
    """
    def __init__(self, app):
        self.app = app

    def busca_usuario(self, user, password):

        return "Usuario da busca %s e senha %s" % (user, password)