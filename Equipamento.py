import hashlib as hs
import sqlite3 as sql
from pathlib import Path


database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Equipamento(object):
    def __init__(self, codigo, descricao, fabricante, tamanho, peso):
        self.codigo = codigo
        self.descricao = descricao
        self.fabricante = fabricante
        self.tamanho = tamanho
        self.peso = peso

    def mostrarEquipamento(self):
        print(f''' <Equipamento>
        Codigo: {self.codigo}
        Descricao: {self.descricao}
        Fabricante:{self.fabricante}
        Tamanho: {self.tamanho}
        Peso: {self.peso}
        ''')

    def calculaCustoEquipamento(self):
        pass

    def inserir_equipamento_db(self):
        db_cursor.execute("SELECT * FROM equipemnto WHERE codigo = :codigo ",
                          {'identificador': self.codigo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO equipamento VALUES(:codigo, :descricao, :fabricante, :tamanho, :peso)",
                              {'codigo': self.codigo, 'descricao': self.descricao, 'fabricante': self.fabricante,
                               'tamanho': self.tamanho, 'peso': self.peso})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo equipamento adicionado a base de dados!\n')

        else:
            print('>> Equipamento ja cadastrado!')
            #debug
            #print(lst)
