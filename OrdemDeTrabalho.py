from Buraco import Buraco
#from Reparo import Reparo

import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Endereco import Endereco

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()


class OrdemDeTrabalho(Buraco):
    def __init__(self, endereco, tamanho, localizacao, prioridade, registradoPor, descricao,
                 situacao, equipeDeReparo, equipamentos, horasAplicadas):
        super(OrdemDeTrabalho, self).__init__(endereco, tamanho, localizacao, prioridade, registradoPor)
        self.codigo = hs.sha224((self.identificador + descricao).encode('utf-8')).hexdigest()
        self.descricao = descricao
        self.situacao = situacao
        self.equipeDeReparo = equipeDeReparo  #recebe o identificador da equipe de reparo
        self.equipamentos = equipamentos  #recebe uma lista com os codigos dos equipamentos
        self.horasAplicadas = horasAplicadas

    def mostrar_ordem_de_trabalho(self):
        print(f''' <Ordem de Trabalho>
        Codigo: {self.codigo}
        Descricao: {self.descricao}
        Situacao: {self.situacao}
        Equipe de reparo: {self.equipeDeReparo}
        Equipamentos: {self.equipamentos}
        Horas aplicadas: {self.horasAplicadas}
        ''')
        self.mostrar_buraco()

    # def gerar_reparo(self, descricaoReparo, status, materialUtilizado):
    #     reparo = Reparo(self.endereco, self.tamanho, self.localizacao, self.prioridade, self.registradoPor,
    #                     self.descricao, self.situacao,self.equipeDeReparo, self.equipamentos, self.horasAplicadas,
    #                     descricaoReparo, status, materialUtilizado)
    #     return reparo

    def inserir_ordem_de_trabalho_db(self):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()
        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO ordemDeTrabalho VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas)",
                              {'identificador': self.identificador, 'endereco': self.endereco.string_endereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': ','.join(self.equipamentos), 'horasAplicadas': self.horasAplicadas})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Nova ordem de trabalho adicionada na base de dados!\n')

        else:
            print('>> Ordem de trabalho ja cadastrada!')
            if DEBUG_FLAG:
                print(lst)

    def remover_ordem_de_trabalho_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM ordemDeTrabalho WHERE identificador = :identificador",
                              {'identificador': self.identificador})

    #caso haja mudanca no buraco pai, atualizar a ordem referente a ele
    def buraco_atualizado(self, atualizacao):
        self.remover_ordem_de_trabalho_db()

        self.identificador = atualizacao.identificador
        self.endereco = atualizacao.endereco
        self.tamanho = atualizacao.tamanho
        self.localizacao = atualizacao.localizacao
        self.prioridade = atualizacao.prioridade
        self.registradoPor = atualizacao.registradoPor

        self.codigo = hs.sha224((self.identificador + self.descricao).encode('utf-8')).hexdigest()

        self.inserir_ordem_de_trabalho_db()


    def atualizar_codigo(self):
        novo_codigo = hs.sha224((self.identificador + self.descricao).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET codigo = :novo_codigo WHERE identificador = :identificador",
                              {'novo_codigo': novo_codigo, 'identificador': self.identificador})

        self.codigo = novo_codigo

    # atualizar descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
    def atualizar_descricao(self, novo_valor):
        self.descricao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET descricao = :descricao WHERE identificador = :identificador",
                              {'descricao': self.descricao, 'identificador': self.identificador})

        self.atualizar_codigo()

    def atualizar_situacao(self, novo_valor):
        self.situacao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET situacao = :situacao WHERE identificador = :identificador",
                              {'situacao': self.situacao, 'identificador': self.identificador})

    def atualizar_equipeDeReparo(self, novo_valor):
        self.equipeDeReparo = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET equipeDeReparo = :equipeDeReparo WHERE identificador = :identificador",
                              {'equipeDeReparo': self.equipeDeReparo, 'identificador': self.identificador})

    def atualizar_equipamentos(self, novo_valor):
        self.equipamentos = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET equipamentos = :equipamentos WHERE identificador = :identificador",
                              {'equipamentos': ','.join(self.equipamentos), 'identificador': self.identificador})

    def atualizar_horasAplicadas(self, novo_valor):
        self.horasAplicadas = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE ordemDeTrabalho SET horasAplicadas = :horasAplicadas WHERE identificador = :identificador",
                              {'horasAplicadas': self.horasAplicadas, 'identificador': self.identificador})
