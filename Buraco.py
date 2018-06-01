import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from OrdemDeTrabalho import OrdemDeTrabalho
from Endereco import Endereco

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()


class Buraco(object):
    def __init__(self, endereco, tamanho, localizacao, prioridade, registradoPor):
        self.identificador = hs.sha224((endereco.string_endereco() + localizacao).encode('utf-8')).hexdigest()
        self.endereco = endereco
        self.tamanho = tamanho
        self.localizacao = localizacao
        self.prioridade = prioridade
        self.registradoPor = registradoPor

    def mostrar_buraco(self):
        print(f''' <Buraco>
        Identificador: {self.identificador}
        Endereco: {self.endereco}
        Tamanho: {self.tamanho}
        Localizacao: {self.localizacao}
        Prioridade: {self.prioridade}
        Registrado por: {self.registradoPor}
        ''')

    def gerar_ordem_de_trabalho(self, descricao, situacao, equipeDeReparo, equipamentos, horasAplicadas):
        ordem = OrdemDeTrabalho(self.endereco, self.tamanho, self.localizacao, self.prioridade, self.registradoPor,
                                descricao, situacao, equipeDeReparo, equipamentos, horasAplicadas)
        return ordem

    def inserir_buraco_db(self):
        db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO buraco VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor)",
                              {'identificador': self.identificador, 'endereco': self.endereco.string_endereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Novo buraco adicionado na base de dados!\n')

        else:
            print('>> Buraco ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)

    def remover_buraco_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM buraco WHERE identificador = :identificador",
                              {'identificador': self.identificador})

#atualizadores
#endereco, tamanho, localizacao, prioridade, registradoPor
    def atualizar_identificador(self):
        novo_identificador = hs.sha224((self.endereco.string_endereco() + self.localizacao).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE buraco SET identificador = :novo_identificador "
                              "WHERE identificador = :identificador",
                              {'novo_identificador': novo_identificador, 'identificador': self.identificador})

        self.identificador = novo_identificador

    def atualizar_endereco(self, novo_valor):
        self.endereco = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE buraco SET endereco = :endereco WHERE identificador = :identificador",
                              {'endereco': self.endereco, 'identificador': self.identificador})

    def atualizar_tamanho(self, novo_valor):
        self.tamanho = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE buraco SET tamanho = :tamanho WHERE identificador = :identificador",
                              {'tamanho': self.tamanho, 'identificador': self.identificador})

    def atualizar_localizacao(self, novo_valor):
        self.localizacao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE buraco SET localizacao = :localizacao WHERE identificador = :identificador",
                              {'localizacao': self.localizacao, 'identificador': self.identificador})

        self.atualizar_identificador()

    def atualizar_prioridade(self, novo_valor):
        self.prioridade = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE buraco SET prioridade = :prioridade WHERE identificador = :identificador",
                              {'prioridade': self.prioridade, 'identificador': self.identificador})


    def atualizar_registradoPor(self, novo_valor):
        self.registradoPor = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE buraco SET registradoPor = :registradoPor WHERE identificador = :identificador",
                              {'registradoPor': self.registradoPor, 'identificador': self.identificador})


