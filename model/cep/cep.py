# -*- coding: iso-8859-1 -*-
from math import sin, cos, acos, radians, degrees
from OFS.SimpleItem import SimpleItem
# from Products.ZSQLMethods.SQL import SQL
# from Globals import package_home
import os
import urllib2
import json


cep2str = lambda x: ('0' * (8 - len(str(x)))) + str(x)[:-3] + '-' + \
                    ('0' * (3 - len(str(x)))) + str(x)[-3:]
cep2int = lambda x: int(x[:5]) * 1000 + int(x[6:])


class CepStatus(object):
    NAO_ATUALIZADO = 0
    IMPRECISO = 1
    ATUALIZADO = 2
    _desc = ['Nunca foi atualizado', 'impreciso', 'atualizado']

    @classmethod
    def getDesc(cls, code):
        return cls._desc[code]


class CepData(SimpleItem):
    """
    Class que busca dados de um Cep via web
    """

    def get_id_cidade_uf(self, data):
        """
        Busca o ID da cidade e UF
        """

        for i in self._zsql_selIdCidade(
                cidade=data['localidade'], uf=data['uf']):
            id_cidade = i.id_cidade
            id_uf = i.id_uf

        try:
            return id_cidade, id_uf
        except:
            raise Exception('Sem cidade ou UF para: ' + str(data))

    def busca_ceps(self):
        """
        Busca um cep aleatorio para atualizar (Ele tem que estar incompleto)
        """

        cep = None
        self.printed = ""

        for i in self._zsql_selCepsToUpdate():
            if i.id_cidade is not None:
                pass
            elif len(str(i.cep)) < 7:
                pass
            else:
                cep = i.cep
                self.printed = "Cep: " + str(cep) + "\n"
                break

        if cep:
            return self.get_cep_data(cep)
        else:
            return "Nenhum cep encontrado."

    def get_cep_data(self, cep):
        """
        Get as infos do cep json
        """

        if len(str(cep)) == 7:
            url = "https://viacep.com.br/ws/0" + str(cep) + "/json/"
        else:
            url = "https://viacep.com.br/ws/" + str(cep) + "/json/"
        response = urllib2.urlopen(url)
        try:
            data = json.loads(response.read())
        except:
            self.printed += "Cep sem informacoes.\n"
            return self.printed

        if 'erro' in data.keys():
            return "Cep " + str(cep) + " nao existe na base\n"
        else:
            self.printed += "Cep data: " + str(data) + "\n"

        return self.update_cep_data(data)

    def update_cep_data(self, data):
        """
        Update os dados do Cep (logradouro, Uf...)
        """

        if data:
            id_cidade_uf = self.get_id_cidade_uf(data)
            id_cidade = id_cidade_uf[0]
            id_uf = id_cidade_uf[1]

            num_cep = data['cep'].replace('-', '')

            self._zsql_updateCepData(
                bairro=data['bairro'],
                logradouro=data['logradouro'],
                id_cidade=id_cidade,
                id_uf=id_uf,
                cep=num_cep)
            self.printed += "Cep atualizado."

            return self.printed

        return "Ocorreu um erro ao atualizar o Cep."


class Cep(object):
    """ Classe que define operacoes com CEPs """
    def __init__(self, num, uf, cidade, logradouro,
                 bairro, lat, lng, idStatus):
        self._num = num
        self._uf = uf
        self._lat = lat
        self._lng = lng
        self._idStatus = idStatus
        self._cidade = cidade
        self._logradouro = logradouro
        self._bairro = bairro

    def __eq__(self, other):
        try:
            return ((self._num == other._num) and
                    (self._lat == other._lat) and
                    (self._lng == other._lng))
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        " Retorna a distância em km entre os dois operandos "
        try:
            return self.calc_dist_geopos(other)
        except AttributeError:
            return -1

    def getNum(self):
        return self._num

    def getUf(self):
        return self._uf

    def getStr(self):
        cepStr = ('0' * (8 - len(str(self._num)))) + str(self._num)
        return cepStr[0:5] + '-' + cepStr[5:8]

    def getLat(self):
        return self._lat

    def getLng(self):
        return self._lng

    def getStatus(self):
        return self._idStatus

    def getCidade(self):
        return self._cidade

    def getLogradouro(self):
        return self._logradouro

    def getBairro(self):
        return self._bairro

    def calc_dist_geopos(self, other):
        """
        Calcula a distancia entre dois ceps usando latitude e longitude.
        """
        try:
            #
            # Constantes
            # raio da terra em km
            rt = 40030

            # Calculo dos arcos a serem usados
            arco_a = radians(float(self.getLng()) - float(other.getLng()))
            arco_b = radians(90.0 - float(other.getLat()))
            arco_c = radians(90.0 - float(self.getLat()))

            # Calculo do arco resultante entre os dois pontos
            arco_r = acos((cos(arco_b) * cos(arco_c)) +
                          (sin(arco_b) * sin(arco_c) * cos(arco_a)))

            # Calculo da extensao do arco resultante em
            extensao = (degrees(arco_r) * rt) / 360
        except ValueError:
            extensao = 0

        print extensao
        return extensao


class BdCepFactory(object):
    def create(self, queryResult):
        return Cep(queryResult['cep'], queryResult['uf'],
                   queryResult['cidade'], queryResult['logradouro'],
                   queryResult['bairro'], queryResult['latitude'],
                   queryResult['longitude'], queryResult['status'])


class CepSearch(SimpleItem):
    " Consultor de CEPs "

    cepFactory = BdCepFactory()

    def getFields(self, cepStr):
        " Retorna um dicionario de dados sobre o CEP "
        cepNum = cep2int(cepStr)
        dec = lambda x: x is not None \
            and x.decode('iso8859-1').encode('utf-8') or ''
        cepStr = ('0' * (8 - len(str(cepNum)))) + str(cepNum)
        cepStr = cepStr[0:5] + '-' + cepStr[5:8]
        results = self._zsql_selCepsByNum(cep=cepNum)
        if len(results):
            fields = {'cep': results[0]['cep'],
                      'logradouro': dec(results[0]['logradouro']),
                      'bairro': dec(results[0]['bairro']),
                      'cidade': dec(results[0]['cidade']),
                      'uf': dec(results[0]['uf']),
                      'id_uf': results[0]['id_uf'],
                      'id_cidade': results[0]['id_cidade']}
        else:
            fields = {}
        return fields

    def getCep(self, cepStr):
        " Retorna um objeto Cep "
        return self.cepFactory.create(
            self._zsql_selCepsByNum(cep=cep2int(cepStr))[0])

    _zsql_selCepsByNum = SQL(
        '_zsql_selCepsByNum', '', 'connection', 'cep',
        open(product_path + 'sql/selCepsByNum.sql').read()
    )
