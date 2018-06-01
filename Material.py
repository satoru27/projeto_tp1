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


class Material(object):
    def __init__(self, descricao, valor, quantidade, tipo):
        self.codigo = hs.sha224((descricao + tipo).encode('utf-8')).hexdigest()
        self.descricao = descricao
        self.valor = valor
        self.quantidade = quantidade
        self.tipo = tipo

    def calcula_custo_material(self):
        pass

    def mostrar_material(self):
        print(f'''<Informacoes do material>
          Codigo: {self.codigo}
          Descricao: {self.descricao}
          Valor:v{self.valor}
          Quantidade: {self.quantidade}
          Tipo: {self.tipo}''')

    def inserir_material_db(self):
        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                          {'codigo': self.codigo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO material VALUES(:codigo, :descricao, :valor, :quantidade, :tipo)",
                              {'codigo': self.codigo, 'descricao': self.descricao, 'valor': self.valor,
                               'quantidade': self.quantidade, 'tipo': self.tipo})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                                  {'codigo': self.codigo})
                print(db_cursor.fetchall())

            print('>> Novo  material adicionado a base de dados!\n')

        else:
            print('>> Material  ja cadastrado!\n')

            if DEBUG_FLAG:
                print(lst)

    def remover_material_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM material WHERE codigo = :codigo", {'codigo': self.codigo})


#Atualiza cada campo no objeto e no banco de dados

    def atualizar_codigo(self):
        novo_codigo = hs.sha224((self.descricao + self.tipo).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE material SET codigo = :novo_codigo WHERE codigo = :codigo",
                              {'novo_codigo': novo_codigo, 'codigo': self.codigo})

        self.codigo = novo_codigo

    def atualizar_descricao(self, novo_valor):
        self.descricao = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE material SET descricao = :descricao WHERE codigo = :codigo",
                              {'descricao': self.descricao, 'codigo': self.codigo})

        self.atualizar_codigo()

    def atualizar_valor(self, novo_valor):
        self.valor = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE material SET valor = :valor WHERE codigo = :codigo",
                              {'valor': self.valor, 'codigo': self.codigo})

    def atualizar_quantidade(self, novo_valor):
        self.quantidade = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE material SET quantidade = :quantidade WHERE codigo = :codigo",
                              {'quantidade': self.quantidade, 'codigo': self.codigo})

    def atualizar_tipo(self, novo_valor):
        self.tipo = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE material SET tipo = :tipo WHERE codigo = :codigo",
                              {'tipo': self.tipo, 'codigo': self.codigo})

        self.atualizar_codigo()








