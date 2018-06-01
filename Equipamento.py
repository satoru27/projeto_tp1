import hashlib as hs
import sqlite3 as sql
from pathlib import Path

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Equipamento(object):
    def __init__(self, descricao, fabricante, tamanho, peso):
        self.codigo = hs.sha224((descricao + fabricante).encode('utf-8')).hexdigest()
        self.descricao = descricao
        self.fabricante = fabricante
        self.tamanho = tamanho
        self.peso = peso

    def mostrar_equipamento(self):
        print(f''' <Equipamento>
        Codigo: {self.codigo}
        Descricao: {self.descricao}
        Fabricante:{self.fabricante}
        Tamanho: {self.tamanho}
        Peso: {self.peso}
        ''')

    def calcula_custo_equipamento(self):
        pass

    def inserir_equipamento_db(self):
        db_cursor.execute("SELECT * FROM equipamento WHERE codigo = :codigo ",
                          {'codigo': self.codigo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO equipamento VALUES(:codigo, :descricao, :fabricante, :tamanho, :peso)",
                              {'codigo': self.codigo, 'descricao': self.descricao, 'fabricante': self.fabricante,
                               'tamanho': self.tamanho, 'peso': self.peso})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM equipamento WHERE codigo = :codigo ",
                                  {'codigo': self.codigo})
                print(db_cursor.fetchall())

            print('>> Novo equipamento adicionado a base de dados!\n')

        else:
            print('>> Equipamento ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)

    def remover_equipamento_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM equipamento WHERE codigo = :codigo", {'codigo': self.codigo})

#  atualiza
#  descricao, fabricante, tamanho, peso

    def atualizar_codigo(self):
        novo_codigo = hs.sha224((self.descricao + self.fabricante).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE equipamento SET codigo = :novo_codigo WHERE codigo = :codigo",
                              {'novo_codigo': novo_codigo, 'codigo': self.codigo})

        self.codigo = novo_codigo

    def atualizar_descricao(self, novo_valor):
        self.descricao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE equipamento SET descricao = :descricao WHERE codigo = :codigo",
                              {'descricao': self.descricao, 'codigo': self.codigo})

        self.atualizar_codigo()

    def atualizar_fabricante(self, novo_valor):
        self.fabricante = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE equipamento SET fabricante = :fabricante WHERE codigo = :codigo",
                              {'fabricante': self.fabricante, 'codigo': self.codigo})

        self.atualizar_codigo()

    def atualizar_tamanho(self, novo_valor):
        self.tamanho = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE equipamento SET tamanho = :tamanho WHERE codigo = :codigo",
                              {'tamanho': self.tamanho, 'codigo': self.codigo})


    def atualizar_peso(self, novo_valor):
        self.peso = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE equipamento SET peso = :peso WHERE codigo = :codigo",
                              {'peso': self.peso, 'codigo': self.codigo})

