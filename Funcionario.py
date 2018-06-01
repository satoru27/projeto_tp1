import hashlib as hs
import sqlite3 as sql
from pathlib import Path

from Cidadao import Cidadao
from Endereco import Endereco

DEBUG_FLAG = True

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Funcionario(Cidadao):
    def __init__(self, nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email,
                 profissao, funcionario, recebeuDano, cargo, salario):
        super(Funcionario, self).__init__(nome, cpf, identidade, filiacao, sexo, estadoCivil,
                                          naturalidade, endereco, email, profissao)
        self.codigo = hs.sha224((self.identificador + cargo).encode('utf-8')).hexdigest()
        self.cargo = cargo
        self.salario = salario

    # def inserirCadastroFuncionario(self):
    #     pass

    def modificar_cadastro_funcionario(self):
        pass

    # def removerCadastroFuncionario(self):
    #     pass

    def mostrar_cadastro_funcionario(self):
        super(Funcionario, self).mostrar_cadastro()
        print(f''' <Funcionario>
        Codigo: {self.codigo}
        Cargo: {self.cargo}
        Salario: {self.salario}
        ''')

    def inserir_funcionario_db(self):
        db_cursor.execute("SELECT * FROM funcionario WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO funcionario VALUES(:identificador, :nome, :cpf, :identidade, :filiacao, :sexo,"
                              ":estadoCivil, :naturalidade, :endereco, :email, :profissao, :funcionario, :recebeuDano,"
                              " :codigo, :cargo, :salario)",
                              {'identificador':self.identificador, 'nome': self.nome, 'cpf': self.cpf,
                               'identidade': self.identidade,'filiacao':self.filiacao,'sexo':self.sexo,
                               'estadoCivil': self.estadoCivil, 'naturalidade': self.naturalidade,
                               'endereco': self.endereco.string_endereco(), 'email': self.email,
                               'profissao': self.profissao,'funcionario': int(self.funcionario),
                               'recebeuDano': int(self.recebeuDano),'codigo':self.codigo, 'cargo': self.cargo,
                               'salario': self.salario})

            db_connection.commit()

            if DEBUG_FLAG:
                db_cursor.execute("SELECT * FROM funcionario WHERE identificador = :identificador ",
                                 {'identificador': self.identificador})
                print(db_cursor.fetchall())

            print('>> Novo funcionario adicionado a base de dados!\n')

        else:
            print('>> Funcionario ja cadastrado!')
            if DEBUG_FLAG:
                print(lst)

    def cidadao_atualizado(self,atualizacao):
        self.identificador = atualizacao.identificador
        self.nome = atualizacao.nome
        self.cpf = atualizacao.cpf
        self.identidade = atualizacao.identidade
        self.filiacao = atualizacao.filiacao
        self.sexo = atualizacao.sexo
        self.estadoCivil = atualizacao.estadoCivil
        self.naturalidade = atualizacao.naturalidade
        self.endereco = atualizacao.endereco
        self.email = atualizacao.email
        self.profissao = atualizacao.profissao
        self.funcionario = True
        self.recebeuDano = atualizacao.recebeuDano

        self.codigo = hs.sha224((self.identificador + self.cargo).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE funcionario SET "
                              "identificador = :identificador, nome = :nome, cpf = :cpf, identidade = :identidade,"
                              "filiacao =  :filiacao, sexo = :sexo,"
                              "estadoCivil = :estadoCivil, naturalidade = :naturalidade, endereco = :endereco,"
                              " email = :email, profissao = :profissao, funcionario =  :funcionario,"
                              "recebeuDano =  :recebeuDano,"
                              "codigo = :codigo WHERE identificador = :identificador",
                              {'identificador': self.identificador, 'nome': self.nome, 'cpf': self.cpf,
                               'identidade': self.identidade, 'filiacao': self.filiacao, 'sexo': self.sexo,
                               'estadoCivil': self.estadoCivil, 'naturalidade': self.naturalidade,
                               'endereco': self.endereco.string_endereco(), 'email': self.email,
                               'profissao': self.profissao, 'funcionario': int(self.funcionario),
                               'recebeuDano': int(self.recebeuDano), 'codigo': self.codigo})

    def atualizar_codigo(self):
        novo_identificador = hs.sha224((self.identificador + self.cargo).encode('utf-8')).hexdigest()
        with db_connection:
            db_cursor.execute("UPDATE funcionario SET codigo = :novo_identificador "
                              "WHERE identificador = :identificador",
                              {'novo_identificador': novo_identificador, 'identificador': self.identificador})

        self.codigo = novo_identificador

    def atualizar_cargo(self, novo_valor):
        self.cargo = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE funcionario SET cargo = :cargo WHERE identificador = :identificador",
                              {'cargo': self.cargo, 'identificador': self.identificador})

    def atualizar_salario(self, novo_valor):
        self.salario = novo_valor
        with db_connection:
            db_cursor.execute("UPDATE funcionario SET salario = :salario WHERE identificador = :identificador",
                              {'salario': self.salario, 'identificador': self.identificador})

    # def inserirMaterialDeReparo(self):
    #     pass
    #
    # def modificarMaterialDeReparo(self):
    #     pass
    #
    # def removerMaterialDeReparo(self):
    #     pass
    #
    # def mostrarMaterialDeReparo(self):
    #     pass
    #
    # def inserirEquipamento(self):
    #     pass
    #
    # def modificarEquipamento(self):
    #     pass
    #
    # def removerEquipamento(self):
    #     pass
    #
    # def mostrarEquipament(self):
    #     pass
    #
    # def inserirEquipe(self):
    #     pass
    #
    # def modificarEquipe(self):
    #     pass
    #
    # def removerEquipe(self):
    #     pass
    #
    # def mostrarEquipe(self):
    #     pass
    #
    # def inserirReparo(self):
    #     pass
    #
    # def removerReparo(self):
    #     pass
    #
    # def modificarReparo(self):
    #     pass
    #
    # def mostrarReparo(self):
    #     pass
    #
    # def inserirOrdemDeTrabalho(self):
    #     pass
    #
    # def removerOrdemDeTrabalho(self):
    #     pass
    #
    # def modificarOrdemDeTrabalho(self):
    #     pass
    #
    # def mostrarOrdemDeTrabalho(self):
    #     pass

