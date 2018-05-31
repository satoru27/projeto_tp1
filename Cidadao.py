import hashlib as hs
import sqlite3 as sql
from pathlib import Path


database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class Cidadao(object):
    def __init__(self, identificador, nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email,
                 profissao, funcionario, recebeuDano):
        self.identificador = identificador
        self.nome = nome
        self.cpf = cpf
        self.identidade = identidade
        self.filiacao = filiacao
        self.sexo = sexo
        self.estadoCivil = estadoCivil
        self.naturalidade = naturalidade
        self.endereco = endereco # redefinir endereco nao para uma classe e sim para a concatenacao dos campos separado por virgula
        self.email = email
        self.profissao = profissao
        self.funcionario = funcionario
        self.recebeuDano = recebeuDano

    #def inserirCadastro(self):
    #    pass

    #def removerCadastro(self):
    #    pass

    def modificarCadastro(self):
        pass

    def mostrarCadastro(self):
        print(f'''<Informacoes do cidadao>
        Identificador: {self.identificador}
        Nome: {self.nome}
        CPF: {self.cpf}
        Identidade: {self.identidade}
        Filiacao: {self.filiacao}
        Sexo: {self.sexo}
        Estado civil: {self.estadoCivil}
        Naturalidade: {self.naturalidade}
        E-mail: {self.email}
        Profissao: {self.profissao}
        Funcionario: {self.funcionario}
        Recebeu dano: {self.recebeuDano}
        ''')
        self.endereco.mostrarEndereco()


    def inserir_cadastro_db(self):
        db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO cidadao VALUES(:identificador, :nome, :cpf, :identidade, :filiacao, :sexo,"
                              ":estadoCivil, :naturalidade, :endereco, :email, :profissao, :funcionario, :recebeuDano)",
                              {'identificador':self.identificador, 'nome': self.nome, 'cpf': self.cpf,
                               'identidade': self.identidade,'filiacao':self.filiacao,'sexo':self.sexo,
                               'estadoCivil': self.estadoCivil, 'naturalidade': self.naturalidade,
                               'endereco': self.endereco.stringEndereco(), 'email': self.email,
                               'profissao': self.profissao,'funcionario': int(self.funcionario),
                               'recebeuDano': int(self.recebeuDano)})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo usuario adicionado a base de dados!\n')

        else:
            print('>> Cidadao ja cadastrado!')
            #debug
            #print(lst)



    # def consultaArquivoDeDanos(self):
    #     pass
    #
    # def realizaConsultaGeral(self):
    #     pass
    #
    # def geraRelatorio(self):
    #     pass
    #
    # def inserirBuraco(self):
    #     pass
    #
    # def removerBuraco(self):
    #     pass
    #
    # def modificarBuraco(self):
    #     pass
    #
    # def mostrarBuraco(self):
    #     pass
    #
    # def inserirDanoRecebido(self):
    #     pass
    #
    # def removerDanoRecebido(self):
    #     pass
    #
    # def modificarDanoRecebido(self):
    #     pass
    #
    # def mostrarDanoRecebido(self):
    #     pass

class Funcionario(Cidadao):
    def __init__(self, identificador, nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email,
                 profissao, funcionario, recebeuDano, codigo, cargo, salario):
        super(Funcionario, self).__init__(identificador, nome, cpf, identidade, filiacao, sexo, estadoCivil,
                                          naturalidade, endereco, email, profissao, funcionario, recebeuDano)
        self.codigo = codigo
        self.cargo = cargo
        self.salario = salario

    # def inserirCadastroFuncionario(self):
    #     pass

    def modificarCadastroFuncionario(self):
        pass

    # def removerCadastroFuncionario(self):
    #     pass

    def mostrarCadastroFuncionario(self):
        super(Funcionario,self).mostrarCadastro()
        print(f''' <Funcionario>
        Codigo: {self.codigo}
        Cargo: {self.cargo}
        Salario: {self.salario}
        ''')

    def inserir_cadastro_funcionario_db(self):
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
                               'endereco': self.endereco.stringEndereco(), 'email': self.email,
                               'profissao': self.profissao,'funcionario': int(self.funcionario),
                               'recebeuDano': int(self.recebeuDano),'codigo':self.codigo, 'cargo': self.cargo,
                               'salario': self.salario})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo funcionario adicionado a base de dados!\n')

        else:
            print('>> Funcionario ja cadastrado!')
            #debug
            #print(lst)

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

