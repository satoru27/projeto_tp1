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

    def gerar_reparo(self, descricaoReparo, status, materialUtilizado):
        reparo = Reparo(self.endereco, self.tamanho, self.localizacao, self.prioridade, self.registradoPor,
                        self.descricao, self.situacao,self.equipeDeReparo, self.equipamentos, self.horasAplicadas,
                        descricaoReparo, status, materialUtilizado)
        return reparo

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
