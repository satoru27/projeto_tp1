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


class Endereco(object):
    """classe de suporte para armazenar o endereco de forma estruturada
    no banco de dados ele e armazenado como uma concatenacao
    de cidade,uf e bairro separados por virgula
    """
    def __init__(self, cidade, uf, bairro):
        self.cidade = cidade
        self.uf = uf
        self.bairro = bairro

    def mostrarEndereco(self):
        print(f''' <Endereco>
        Cidade: {self.cidade}
        UF: {self.uf}
        Bairro: {self.bairro}
        ''')

    def stringEndereco(self):
        return ",".join([self.cidade, self.uf, self.bairro])


class Dano(object):
    def __init__(self, idDano, tipoDeDano, pagamento, idBuraco, idCidadao):
        self.idDano = idDano
        self.tipoDeDano = tipoDeDano
        self.pagamento = pagamento
        self.idBuraco = idBuraco
        self.idCidadao = idCidadao

    def mostrarDano(self):
        print(f'''<Dano> 
        Identificador do Dano: {self.idDano}
        Tipo de Dano: {self.tipoDeDano}
        Pagamento: {self.pagamento}
        Identificador do Buraco: {self.idBuraco}
        Cidadao que recebeu o dano: {self.idCidadao}
        ''')


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


class Buraco(object):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor):
        self.identificador = identificador
        self.endereco = endereco
        self.tamanho = tamanho
        self.localizacao = localizacao
        self.prioridade = prioridade
        self.registradoPor = registradoPor

    def mostrarBuraco(self):
        print(f''' <Buraco>
        Identificador: {self.identificador}
        Endereco: {self.endereco}
        Tamanho: {self.tamanho}
        Localizacao: {self.localizacao}
        Prioridade: {self.prioridade}
        Registrado por: {self.registradoPor}
        ''')

    def inserir_buraco_db(self):
        db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO buraco VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo buraco adicionado na base de dados!\n')

        else:
            print('>> Buraco ja cadastrado!')
            #debug
            #print(lst)

class OrdemDeTrabalho(Buraco):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor, codigo, descricao,
                 situacao, equipeDeReparo, equipamentos, horasAplicadas):
        super(OrdemDeTrabalho, self).__init__(identificador, endereco, tamanho, localizacao, prioridade,
                                              registradoPor)
        self.codigo = codigo
        self.descricao = descricao
        self.situacao = situacao
        self.equipeDeReparo = equipeDeReparo
        self.equipamentos = equipamentos
        self.horasAplicadas = horasAplicadas

    def mostrarOrdemDeTrabalho(self):
        print(f''' <Ordem de Trabalho>
        Codigo: {self.codigo}
        Descricao: {self.descricao}
        Situacao: {self.situacao}
        Equipe de reparo: {self.equipeDeReparo}
        Equipamentos: {self.equipamentos}
        Horas aplicadas: {self.horasAplicadas}
        ''')

    def inserir_ordem_de_trabalho_db(self):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()
##VERIFICAR SE AS CLASSES BURACO, ORDEM DE TRABALHO E ETC SÃO NECESSARIAS A HERANCA
##POR UM LADO COLOCAR A HERANCA FACILITARIA A BUSCA POIS TODAS AS INFORMCOES
        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO ordemDeTrabalho VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': self.equipamentos, 'horasAplicadas': self.horasAplicadas})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Nova ordem de trabalho adicionada na base de dados!\n')

        else:
            print('>> Ordem de trabalho ja cadastrada!')
            #debug
            #print(lst)

class Reparo(OrdemDeTrabalho):
    def __init__(self, identificador, endereco, tamanho, localizacao, prioridade, registradoPor, codigo, descricao, situacao,
                 equipeDeReparo, equipamentos, horasAplicadas, codigoReparo, descricaoReparo, status, materialUtilizado,
                 custo):
        super(Reparo, self).__init__(identificador, endereco, tamanho, localizacao, prioridade, registradoPor,
                                     codigo, descricao, situacao, equipeDeReparo, equipamentos, horasAplicadas)
        self.codigoReparo = codigoReparo
        self.descricaoReparo = descricaoReparo
        self.status = status
        self.materialUtilizado = materialUtilizado
        self.custo = custo

    def mostraReparo(self):
        print(f'''<Reparo>
        Codigo: {self.codigoReparo}
        Descricao: {self.descricaoReparo}
        Status: {self.status}
        Material: {self.materialUtilizado}
        Custo: {self.custo}
        ''')

    def calculaReparo(self):
        pass

    def inserir_reparo_db(self):
        db_cursor.execute("SELECT * FROM reparo WHERE reparo = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO reparo VALUES(:identificador, :endereco, :tamanho, :localizacao,"
                              " :prioridade, :registradoPor, :codigo, :descricao,:situacao, :equipeDeReparo,"
                              " :equipamentos, :horasAplicadas, :codigoReparo, :descricaoReparo, :status,"
                              " :materialUtilizado,:custo)",
                              {'identificador': self.identificador, 'endereco': self.endereco.stringEndereco(),
                               'tamanho': self.tamanho, 'localizacao': self.localizacao, 'prioridade': self.prioridade,
                               'registradoPor': self.registradoPor, 'codigo': self.codigo, 'descricao': self.descricao,
                               'situacao': self.situacao, 'equipeDeReparo': self.equipeDeReparo,
                               'equipamentos': self.equipamentos, 'horasAplicadas': self.horasAplicadas,
                               'codigoReparo': self.codigoReparo, 'descricaoReparo': self.descricaoReparo,
                               'status': self.status, 'materialUtilizado': self.materialUtilizado,
                               'custo': self.custo
                               })

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo reparo adicionado na base de dados!\n')

        else:
            print('>> Reparo ja cadastrado!')
            #debug
            #print(lst)

class EquipeDeReparo(object):
    def __init__(self, identificador, numeroDePessoas, funcionarios):
        self.identificador = identificador
        self.numeroDePessoas = numeroDePessoas
        self.funcionarios = funcionarios

    def mostrarEquipeDeReparo(self):
        print(f''' <Equipe de reparo>
        Identificador: {self.identificador}
        Numero de pessoas: {self.numeroDePessoas}
        Funcionarios: {self.funcionarios}
        ''')

    def inserir_equipe_de_reparo_db(self):
        db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador ",
                          {'identificador': self.identificador})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO equipeDeReparo VALUES(:identificador, :numeroDePessoas, :funcionarios)",
                              {'identificador':self.identificador, 'numeroDePessoas': self.numeroDePessoas,
                               'funcionario': self.funcionarios})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo  adicionado a base de dados!\n')

        else:
            print('>>  ja cadastrado!')
            #debug
            #print(lst)

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


class Material(object):
    def __init__(self, codigo, descricao, valor, quantidade, tipo):
        self.codigo = codigo
        self.descricao = descricao
        self.valor = valor
        self.quantidade = quantidade
        self.tipo = tipo

    def calculaCustoMaterial(self):
        pass

    def mostraMaterial(self):
        print(f'''<Informacoes do material>
          Codigo: {self.codigo}
          Descricao: {self.descricao}
          Valor:v{self.valor}
          Quantidade: {self.quantidade}
          Tipo: {self.tipo}''')

    def inserir_material_db(self):
        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                          {'identificador': self.codigo})

        lst = db_cursor.fetchall()

        if not lst:  # se nao encontrarmos o registro o colocamos na database
            db_cursor.execute("INSERT INTO material VALUES(:codigo, :descricao, :valor, :quantidade, :tipo)",
                              {'codigo':self.codigo, 'descricao':self.descricao, 'valor':self.valor, 'quantidade':self.quantidade, 'tipo':self.tipo})

            db_connection.commit()

            #debug
            #db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
            #                  {'identificador': self.identificador})
            #print(db_cursor.fetchall())

            print('>> Novo  material adicionado a base de dados!\n')

        else:
            print('>> Material  ja cadastrado!')
            #debug
            #print(lst)


class SRCB(object):

    def __init__(self,debugCode=0):
        self.debugCode = debugCode

    def interfacePrincipal(self):

        selection = {
            '1': 'interfaceUsuario',

            '2': 'interfaceFuncionario',

            '3': 'interfaceCadastroUsuario'
        }

        print(''' Bem vindo ao sistema
        1) Painel de usuario
        2) Painel de funcionario
        3) Cadastrar novo usuario
        4) Sair
        ''')

        while(1):
            option = input("> ")

            if(option != '4'):
                try:
                    getattr(self,selection[option])()
                except KeyError:
                    print('Opcao invalida')
            else:
                break

        print('Saindo...')

    def login(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        if(self.debugCode == 1):
            nome = "Admin"
            cpf = "919.231.890-85"
            identidade = "45.772.060-8"
            filiacao = "UNB"
            sexo = "ND"
            estadoCivil = "Solteiro"
            naturalidade = "Brasilia"
            endereco = Endereco(cidade="Brasilia", uf= "DF", bairro="Asa Norte")
            email = "admin@thissite.com"
            profissao = "Website Admin"
            funcionario = True
            recebeuDano = False
            codigo = "000"
            cargo = "Administrator"
            salario = "999"
            identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()

            temp = Funcionario(identificador, nome, cpf, identidade, filiacao,
                           sexo, estadoCivil, naturalidade, endereco, email,
                           profissao, funcionario, recebeuDano, codigo, cargo, salario)

            return temp

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificadorUsuario = input("> ")

        #inserir o procedimento de busca no banco de dados

        return user

    def interfaceUsuario(self):
        user = self.login()

        print(''' [ Bem vindo ao painel de usuario ]
         1) Consultar cadastro
         2) Modificar cadastro
         3) Realizar consulta geral
         4) Consultar arquivos de dano
         5) Menu Buraco
         6) Menu Dano Recebido
         7) Gerar relatorio 
         8) Sair
         ''')

        selection = {
            '1': 'mostrarCadastro',
            '2': 'modificarCadastro',#
            '3': 'realizarConsultaGeral',#
            '4': 'consultaArquivosDeDano',#
            '5': 'interfaceBuraco',#
            '6': 'interfaceDanoRecebido',#
            '7': 'gerarRelatorio',#
        }

        while (1):
            option = input("> ")

            if(option == '8'):
                break
            elif(option == '1' or option == '2'):
                getattr(user, selection[option])()
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')



        print('Saindo do painel de usuario...')

    def interfaceFuncionario(self):
        user = self.login()

        print(''' [ Bem vindo ao painel de funcionario ]
         1) Consultar cadastro
         2) Cadastrar novo funcionário
         3) Modificar cadastro
         4) Excluir cadastro
         5) Menu Material de Reparo
         6) Menu Ordem de Trabalho
         7) Menu Equipamento
         8) Menu Equipe de Reparo
         9) Menu Reparo
         10) Sair
         ''')

        selection = {
            '1': 'consultaCadastroFuncionario',
            '2': 'cadastroFuncionario',
            '3': 'modificarCadastroFuncionario',
            '4': 'excluirCadastroFuncionario',
            '5': 'interfaceMaterialDeReparo',
            '6': 'interfaceOrdemDeTrabalho',
            '7': 'interfaceEquipamento',
            '8': 'interfaceEquipeDeReparo',
            '9': 'interfaceReparo',
        }

        while (1):
            option = input("> ")

            if(option == '10'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')



        print('Saindo do painel de funcionario...')


    def interfaceCadastroUsuario(self):
        print(''' [ Bem vindo ao painel de cadastro ]:
        ''')

        novoUsuario = self.inserirCadastro()


    def inserirCadastro(self):
        nome = input('>> Insira o nome: ')
        cpf = input('>> Insira o cpf: ')
        identidade = input('>> Insira a identidade: ')
        filiacao = input('>> Insira a filiacao: ')
        sexo = input('>> Insira o sexo: ')
        estadoCivil = input('>> Insira o estado civil: ')
        naturalidade = input('>> Insira a naturalidade: ')
        endereco = self.novoEndereco()
        email = input('>> Insira o email: ')
        profissao = input('>> Insira a profissao:')
        funcionario = False
        recebeuDano = False

        identificador = hs.sha224((nome + cpf).encode('utf-8')).hexdigest()

        novoUsuario = Cidadao(identificador, nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email, profissao, funcionario, recebeuDano)

        if(self.debugCode == 1):
            novoUsuario.mostrarCadastro()

        return novoUsuario

    def novoEndereco(self):
        cidade = input('>> Insira a cidade: ')
        uf = input('>> Insira a UF: ')
        bairro = input('>> Insira o bairro: ')

        enderecoUsuario = Endereco(cidade,uf,bairro)

        return enderecoUsuario

    def realizarConsultaGeral(self):
        pass

    def consultaArquivosDeDano(self):
        pass

    def interfaceBuraco(self):
        pass

    def interfaceDanoRecebido(self):
        pass

    def gerarRelatorio(self):
        pass

    def consultaCadastroFuncionario(self):
        pass

    def cadastroFuncionario(self):
        pass

    def modificarCadastroFuncionario(self):
        pass

    def excluirCadastroFuncionario(self):
        pass

    def interfaceMaterialDeReparo(self):
        pass

    def interfaceOrdemDeTrabalho(self):
        pass

    def interfaceEquipamento(self):
        pass

    def interfaceEquipeDeReparo(self):
        pass

    def interfaceReparo(self):
        pass