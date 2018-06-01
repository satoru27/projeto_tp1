from OrdemDeTrabalho import OrdemDeTrabalho

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

class Reparo(OrdemDeTrabalho):
    def __init__(self, endereco, tamanho, localizacao, prioridade, registradoPor, descricao, situacao,
                 equipeDeReparo, equipamentos, horasAplicadas, descricaoReparo, status, materialUtilizado):
        super(Reparo, self).__init__(endereco, tamanho, localizacao, prioridade, registradoPor, descricao, situacao,
                                     equipeDeReparo, equipamentos, horasAplicadas)
        self.codigoReparo = hs.sha224((self.codigo + descricaoReparo).encode('utf-8')).hexdigest()
        self.descricaoReparo = descricaoReparo
        self.status = status
        self.materialUtilizado = materialUtilizado  # recebe uma lista
        # uma possibilidade para definir um custo para o material eh pegar os ultimos dois digitos do codigo do
        # material e usar como custo
        self.custo = 0  # custo deve ser definido por calcula custo

    def mostra_reparo(self):
        print(f'''<Reparo>
        Codigo: {self.codigoReparo}
        Descricao: {self.descricaoReparo}
        Status: {self.status}
        Material: {self.materialUtilizado}
        Custo: {self.custo}
        ''')

    def calcula_custo(self):
        pass

    def inserir_reparo_db(self):
        db_cursor.execute("SELECT * FROM reparo WHERE codigoReparo = :codigoReparo ",
                          {'codigoReparo': self.codigoReparo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO reparo VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas, :codigoReparo, :descricaoReparo, :status,"
                              " :materialUtilizado,:custo)",
                              {'identificador': self.identificador, 'endereco': self.endereco.string_endereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': ','.join(self.equipamentos), 'horasAplicadas': self.horasAplicadas,
                               'codigoReparo': self.codigoReparo, 'descricaoReparo': self.descricaoReparo,
                               'status': self.status, 'materialUtilizado': ','.join(self.materialUtilizado),
                               'custo': self.custo
                               })

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Novo reparo adicionado na base de dados!\n')

        else:
            print('>> Reparo ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)

    def remover_reparo_db(self):
        with db_connection:
            db_cursor.execute("DELETE FROM reparo WHERE identificador = :identificador",
                              {'identificador': self.identificador})

    def ordem_atualizada(self,atualizacao):
        self.identificador = atualizacao.identificador
        self.endereco = atualizacao.endereco
        self.tamanho = atualizacao.tamanho
        self.localizacao = atualizacao.localizacao
        self.prioridade = atualizacao.prioridade
        self.registradoPor = atualizacao.registradoPor

        self.codigo = atualizacao.codigo
        self.descricao = atualizacao.descricao
        self.situacao = atualizacao.situacao
        self.equipeDeReparo = atualizacao.equipeDeReparo  # recebe o identificador da equipe de reparo
        self.equipamentos = atualizacao.equipamentos  # recebe uma lista com os codigos dos equipamentos
        self.horasAplicadas = atualizacao.horasAplicadas

        self.codigoReparo = hs.sha224((self.codigo + self.descricaoReparo).encode('utf-8')).hexdigest()

        with db_connection:
            db_cursor.execute("UPDATE reparo SET identificador = :identificador, endereco = :endereco,"
                              "tamanho = :tamanho, localizacao =:localizacao,"
                              "prioridade = :prioridade, registradoPor = :registradoPor, codigo = :codigo,"
                              "descricao = :descricao, situacao = :situacao, equipeDeReparo = :equipeDeReparo,"
                              "equipamentos = :equipamentos, horasAplicadas = :horasAplicadas,"
                              "codigoReparo = :codigoReparo WHERE identificador = :identificador",
                              {'identificador': self.identificador, 'endereco': self.endereco.string_endereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo,'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': ','.join(self.equipamentos), 'horasAplicadas': self.horasAplicadas,
                               'codigoReparo': self.codigoReparo})

    #descricaoReparo, status, materialUtilizado

    def atualizar_codigoReparo(self):
        novo_codigo = hs.sha224((self.codigo + self.descricaoReparo).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE reparo SET codigoReparo = :novo_codigo WHERE identificador = :identificador",
                              {'novo_codigo': novo_codigo, 'identificador': self.identificador})

        self.codigoReparo = novo_codigo

    def atualizar_descricaoReparo(self, novo_valor):
        self.descricaoReparo = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE reparo SET descricaoReparo = :descricaoReparo WHERE identificador = :identificador",
                              {'descricaoReparo': self.descricaoReparo, 'identificador': self.identificador})

        self.atualizar_codigoReparo()

    def atualizar_status(self, novo_valor):
        self.status = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE reparo SET status = :status WHERE identificador = :identificador",
                              {'status': self.status, 'identificador': self.identificador})

    def atualizar_materialUtilizado(self, novo_valor):
        self.materialUtilizado = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE reparo SET materialUtilizado = :materialUtilizado WHERE identificador = :identificador",
                              {'materialUtilizado': ','.join(self.materialUtilizado), 'identificador': self.identificador})

    def atualizar_custo(self):
        with db_connection:
            db_cursor.execute("UPDATE reparo SET custo = : custo WHERE identificador = :identificador",
                              {'custo': self.custo, 'identificador': self.identificador})
