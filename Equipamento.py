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
