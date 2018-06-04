import hashlib as hs
import sqlite3 as sql
from pathlib import Path
import os
#os.system('cls' if os.name == 'nt' else 'clear')
if os.name == 'nt':
    CLEAR = 'cls'
else:
    CLEAR = 'clear'
from random import randint

from Buraco import Buraco
from Cidadao import Cidadao
from Endereco import Endereco
from Dano import Dano
from Equipamento import Equipamento
from EquipeDeReparo import EquipeDeReparo
from Funcionario import Funcionario
from Material import Material
from OrdemDeTrabalho import OrdemDeTrabalho
from Reparo import Reparo

database = 'srcb.db'
#myFile = Path(database)
#if myFile.is_file():
    #run the script to create the db

db_connection = sql.connect(database)
db_cursor = db_connection.cursor()

class SRCB(object):

    def __init__(self,debugCode=0):
        self.debugCode = debugCode

    def interface_principal(self):

        selection = {
            '1': 'interface_cidadao',

            '2': 'interface_funcionario',

            '3': 'interface_cadastro_usuario'
        }

        while(1):
            print(''' [ Bem vindo ao sistema ]
            1) Painel de usuario
            2) Painel de funcionario
            3) Cadastrar novo usuario
            4) Sair
            ''')

            option = input("> ")

            if(option != '4'):
                try:
                    getattr(self,selection[option])()
                except KeyError:
                    print('Opcao invalida')
            else:
                break

        print('Saindo...')
        db_connection.close()

    def login_cidadao(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificador_usuario = input("> ")

        user = self.retorna_cidadao_bd(identificador_usuario)

        return user
    
    def login_funcionario(self):
        """ Realiza o login do usuario por meio do seu identificador, pegando as informacoes
        no banco de dados e retornando o objeto de usuario """

        user = None

        print("[*] Realize o login informando o identificador do seu usuario: ")
        identificador_usuario = input("> ")

        user = self.retorna_funcionario_bd(identificador_usuario)

        return user

    def interface_cidadao(self):
        user = self.login_cidadao()
        
        if user == None:
            print('>> Falha no login!')
            return

        selection = {
            '1': 'mostrar_cadastro',
            '2': 'modificar_cadastro_cidadao',#
            '3': 'realizar_consulta_geral',#
            '4': 'consultar_arquivos_de_dano',#
            '5': 'interface_buraco',#
            '6': 'interface_dano_recebido',#
            '7': 'gerar_relatorio',#
        }

        while (1):
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

            option = input("> ")

            if(option == '8'):
                break
            elif(option == '1'):
                getattr(user, selection[option])()
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de usuario...')

    def interface_funcionario(self):
        user = self.login_funcionario()

        selection = {
            '1': 'consultar_cadastro_funcionario',
            '2': 'modificar_cadastro_funcionario',
            '3': 'excluir_cadastro_funcionario',
            '4': 'cadastrar_funcionario',
            '5': 'interface_material_de_reparo',
            '6': 'interface_ordem_de_trabalho',
            '7': 'interface_equipamento',
            '8': 'interface_equipe_de_reparo',
            '9': 'interface_reparo',
        }

        while 1:
            print(''' [ Bem vindo ao painel de funcionario ]
                     1) Consultar cadastro
                     2) Modificar cadastro
                     3) Excluir cadastro
                     4) Cadastrar novo funcionário
                     5) Menu Material de Reparo
                     6) Menu Ordem de Trabalho
                     7) Menu Equipamento
                     8) Menu Equipe de Reparo
                     9) Menu Reparo
                     10) Sair
                     ''')

            option = input("> ")

            if(option == '10'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de funcionario...')


    def interface_cadastro_cidadao(self):
        print(''' [ Bem vindo ao painel de cadastro ]:
        ''')

        novoUsuario = self.inserir_cadastro_cidadao()


    def inserir_cadastro_cidadao(self):
        nome = input('>> Insira o nome: ')
        cpf = input('>> Insira o cpf: ')
        identidade = input('>> Insira a identidade: ')
        filiacao = input('>> Insira a filiacao: ')
        sexo = input('>> Insira o sexo: ')
        estadoCivil = input('>> Insira o estado civil: ')
        naturalidade = input('>> Insira a naturalidade: ')
        endereco = self.novo_endereco()
        email = input('>> Insira o email: ')
        profissao = input('>> Insira a profissao:')

        novoUsuario = Cidadao(nome, cpf, identidade, filiacao, sexo, estadoCivil, naturalidade, endereco, email, profissao)

        novoUsuario.inserir_cidadao_db()
        
        if(self.debugCode == 1):
            novoUsuario.mostrar_cadastro()

        return novoUsuario

    def novo_endereco(self):
        cidade = input('>> Insira a cidade: ')
        uf = input('>> Insira a UF: ')
        bairro = input('>> Insira o bairro: ')

        enderecoUsuario = Endereco(cidade, uf, bairro)

        return enderecoUsuario

    def retorna_obj_endereco(self, str):
        lst = str.split(',')

        if len(lst) != 3:
            print('>> Algo de errado nao esta certo')
            return None

        endereco = Endereco(lst[0], lst[1], lst[2])

        return endereco

    def retorna_cidadao_bd(self,identificador):
        cidadao = None

        db_cursor.execute("SELECT * FROM cidadao WHERE identificador = :identificador ",
                          {'identificador': identificador})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Cidadao nao encontrado")
            return cidadao

        lst = lst[0]
        #print(lst)

        cidadao = Cidadao(lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], self.retorna_obj_endereco(lst[8]), lst[9], lst[10])
        cidadao.funcionario = bool(lst[11])
        cidadao.recebeuDano = bool(lst[12])

        #cidadao.mostrar_cadastro()

        return cidadao

    def retorna_funcionario_bd(self,identificador):
        funcionario = None

        db_cursor.execute("SELECT * FROM funcionario WHERE identificador = :identificador ",
                          {'identificador': identificador})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Funcionario nao encontrado")
            return funcionario

        lst = lst[0]
        # print(lst)

        funcionario = Funcionario(lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7],
                                  self.retorna_obj_endereco(lst[8]),lst[9], lst[10],lst[14],lst[15])

        # funcionario.mostrar_cadastro_funcionario()
        funcionario.funcionario = bool(lst[11])
        funcionario.recebeuDano = bool(lst[12])

        return funcionario

    def retorna_dano_bd(self,idDano):
        dano = None

        db_cursor.execute("SELECT * FROM dano WHERE idDano = :idDano ", {'idDano': idDano})

        lst = db_cursor.fetchall()

        if not lst:
            print(">> Dano nao encontrado")
            return dano

        lst = lst[0]
        #print(lst)

        dano = Dano(lst[1], lst[2], lst[3], lst[4])

        #dano.mostrar_dano()

        return dano

    def retorna_equipamento_bd(self, codigo):
        obj = None

        db_cursor.execute("SELECT * FROM equipamento WHERE codigo = :codigo ",
                          {'codigo': codigo})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Equipamento nao encontrado")
            return obj

        lst = lst[0]
        print(lst)

        obj = Equipamento(lst[1], lst[2], lst[3], lst[4])

        obj.mostrar_equipamento()

        return obj

    def retorna_material_bd(self, codigo):
        obj = None

        db_cursor.execute("SELECT * FROM material WHERE codigo = :codigo ",
                          {'codigo': codigo})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Material nao encontrado")
            return obj

        lst = lst[0]
        print(lst)
#descricao, valor, quantidade, tipo
        obj = Material(lst[1], lst[2], lst[3], lst[4])

        obj.mostrar_material()

        return obj

    def retorna_equipe_de_reparo_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM equipeDeReparo WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Equipe nao encontrada")
            return obj

        lst = lst[0]
        print(lst)
        # numeroDePessoas, funcionarios
        obj = EquipeDeReparo(int(lst[1]), lst[2].split(','))

        obj.mostrar_equipe_de_reparo()

        return obj

    def retorna_buraco_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM buraco WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Buraco nao encontrado")
            return obj

        lst = lst[0]
        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor
        obj = Buraco(self.retorna_obj_endereco(lst[1]),int(lst[2]),lst[3],int(lst[4]),lst[5])

        #obj.mostrar_buraco()

        return obj

    def retorna_ordem_de_trabalho_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Ordem de trabalho nao encontrada")
            return obj

        lst = lst[0]
        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        obj = OrdemDeTrabalho(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7],lst[8],lst[9],lst[10],int(lst[11]))

        #obj.mostrar_ordem_de_trabalho()

        return obj

    def retorna_reparo_bd(self, identificador):
        obj = None

        db_cursor.execute("SELECT * FROM reparo WHERE identificador = :identificador ",
                          {'identificador': identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Reparo nao encontrado")
            return obj

        lst = lst[0]
        #print(lst)
        # endereco, tamanho, localizacao, prioridade, registradoPor,
        #     descricao,situacao, equipeDeReparo, equipamentos, horasAplicadas
        # descricaoReparo, status, materialUtilizado
        obj = Reparo(self.retorna_obj_endereco(lst[1]), int(lst[2]), lst[3], int(lst[4]), lst[5],
                              lst[7], lst[8], lst[9], lst[10], int(lst[11]),
                              lst[13],lst[14],lst[15])

        #obj.mostrar_reparo()

        return obj
    #
    # def retorna__bd(self, identificador):
    #     pass

    # def consultar_arquivos_de_dano(self,user):
    #     obj = None
    #
    #     db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :idCidadao ",
    #                       {'idCidadao': user.identificador})
    #     lst = db_cursor.fetchall()
    #
    #     if not lst:
    #         print('>> Nao existem danos registrados para esse usuario')
    #         return
    #
    #     for item in lst:
    #         obj = self.retorna_dano_bd(item[0])
    #         obj.mostrar_dano()

    def interface_buraco(self,user):

        selection = {
            '1': 'consultar_buracos',
            '2': 'registrar_buraco',  #
            '3': 'modificar_buraco',  #
            '4': 'excluir_buraco',  #
        }

        while (1):
            print(''' [ Bem vindo ao painel de buracos ]
                             1) Consultar buracos registrados pelo seu usuario
                             2) Registrar buraco
                             3) Modificar buraco
                             4) Excluir buraco
                             5) Sair
                             ''')

            option = input("> ")

            if (option == '5'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de buracos...')

    def consultar_buracos(self, user):

        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :registradoPor ",
                          {'registradoPor': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum buraco encontrado")
            return

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            buraco.mostrar_buraco()

    def registrar_buraco(self,user):#endereco, tamanho, localizacao, prioridade, registradoPor
        endereco = self.novo_endereco()
        tamanho = int(input('>> Insira o tamanho: '))
        localizacao = input('>> Insira a localizacao :')
        prioridade = randint(0,9)
        print(f'>> Prioridade: {prioridade}')
        registradoPor = user.identificador

        buraco = Buraco(endereco, tamanho, localizacao, prioridade, registradoPor)

        buraco.inserir_buraco_db()

    def modificar_buraco(self,user):
        idBuraco = input('>> Insira o identificador do buraco:\n> ')
        buraco = self.retorna_buraco_bd(idBuraco)
        if buraco is None:
            print('>> Buraco nao encontrado')
            return

        selection = {
            '1': 'atualizar_endereco',
            '2': 'atualizar_tamanho',
            '3': 'atualizar_localizacao',
            '4': 'atualizar_prioridade',
            '5': 'atualizar_registradoPor',
        }

        identificador_old = buraco.identificador

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de buraco ]\n [ Selecione o atributo a ser atualizado: ]
                                     1) Endereco
                                     2) Tamanho
                                     3) Localizacao
                                     4) Prioridade
                                     5) Por quem foi registrado
                                     6) Sair
                                     ''')

            option = input("> ")

            if option == '6':
                break
            elif option == '1':
                novo_endereco = self.novo_endereco()
                getattr(buraco, selection[option])(novo_endereco)

            elif option == '2' or option == '4':
                print('>> Insira o novo valor do atributo: ')
                novo_valor = int(input('> '))
                try:
                    getattr(buraco, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = int(input('> '))
                try:
                    getattr(buraco, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        self.buraco_modificado_atualiza_ordem_e_reparo(buraco, identificador_old)

        print('Saindo do painel de atualizacao de buraco...')

    def excluir_buraco(self,user):
        idBuraco = input('>> Insira o identificador do buraco:\n> ')
        confirm = input('>> Deseja realmente excluir o buraco ? [S/s]')
        if confirm == 'S' or confirm == 's':
            buraco = self.retorna_buraco_bd(idBuraco)
            buraco.remover_buraco_db()

        print('Voltando...')
        return

    def modificar_cadastro_cidadao(self, user):

        selection = {
            '1': 'atualizar_nome',
            '2': 'atualizar_cpf',
            '3': 'atualizar_identidade',
            '4': 'atualizar_filiacao',
            '5': 'atualizar_sexo',
            '6': 'atualizar_estadoCivil',
            '7': 'atualizar_naturalidade',
            '8': 'atualizar_endereco',
            '9': 'atualizar_email',
            '10': 'atualizar_profissao'
        }

        identificador_old = user.identificador

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de usuario ]\n [ Selecione o atributo a ser atualizado: ]
                             1) Nome
                             2) CPF
                             3) Identidade
                             4) Filiacao
                             5) Sexo
                             6) Estado Civil
                             7) Naturalidade
                             8) Endereco
                             9) Email
                             10) Profissao
                             11) Sair
                             ''')

            option = input("> ")

            if (option == '11'):
                break
            elif option == '8':
                novo_endereco = self.novo_endereco()
                getattr(user, selection[option])(novo_endereco)

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = input('> ')
                try:
                    getattr(user, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        if user.funcionario:
            funcionario = self.retorna_funcionario_bd(identificador_old)
            #funcionario.mostrar_cadastro_funcionario()
            funcionario.cidadao_atualizado(user)
            #funcionario.mostrar_cadastro_funcionario()
            print('>> Cadastro de funcionario atualizado!')

        if identificador_old != user.identificador:
            self.cidadao_modificado_atualiza_dano(user, identificador_old)  # tem que atualizar o identificador
            self.cidadao_modificado_atualiza_buraco(user, identificador_old)  # ja deve conter a atualizacao de ordem de trabalho e reparo

        print('Saindo do painel de atualizacao de usuario...')

    def cidadao_modificado_atualiza_dano(self,user,identificador_old):
        db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :id_usuario ",
                          {'id_usuario': identificador_old})

        lst = db_cursor.fetchall()

        print(lst)

        for entry in lst:
            dano = self.retorna_dano_bd(entry[0])
            dano.mostrar_dano()
            dano.atualizar_idCidadao(user.identificador)
            dano.mostrar_dano()

    def cidadao_modificado_atualiza_buraco(self,user,identificador_old):
        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :id_usuario ",
                         {'id_usuario': identificador_old})

        lst = db_cursor.fetchall()

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            buraco.atualizar_registradoPor(user.identificador)
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            if ordem is not None:
                ordem.buraco_atualizado(buraco)
                reparo = self.retorna_reparo_bd(entry[0])
                if reparo is not None:
                    reparo.ordem_atualizada(ordem)

    def buraco_modificado_atualiza_ordem_e_reparo(self,buraco,identificador_old):
        db_cursor.execute("SELECT * FROM ordemDeTrabalho WHERE identificador = :identificador ",
                          {'identificador': identificador_old})

        lst = db_cursor.fetchall()

        for entry in lst:
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            if ordem is not None:
                ordem.buraco_atualizado(buraco)
                reparo = self.retorna_reparo_bd(entry[0])
                if reparo is not None:
                    reparo.ordem_atualizada(ordem)

    def interface_dano_recebido(self,user):

        selection = {
            '1': 'consultar_danos',
            '2': 'registrar_dano',  #
            '3': 'modificar_dano',  #
            '4': 'excluir_dano',  #
        }

        while (1):
            print(''' [ Bem vindo ao painel de danos recebidos ]
                                 1) Consultar danos registrados pelo seu usuario
                                 2) Registrar dano recebido
                                 3) Modificar dano recebido
                                 4) Excluir dano recebido
                                 5) Sair
                                 ''')

            option = input("> ")

            if (option == '5'):
                break
            else:
                try:
                    getattr(self, selection[option])(user)
                except KeyError:
                    print('Opcao invalida')

        print('Saindo do painel de danos recebidos...')

    def consultar_danos(self, user):

        db_cursor.execute("SELECT * FROM dano WHERE idCidadao = :idCidadao ",
                          {'idCidadao': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum dano encontrado")
            return

        for entry in lst:
            dano = self.retorna_dano_bd(entry[0])
            dano.mostrar_dano()

    def registrar_dano(self, user):  # tipoDeDano, pagamento, idBuraco, idCidadao
        tipoDeDano = input('>> Informe o tipo de dano:')
        pagamento = randint(0,9999)
        idBuraco = input('>> Insira o identificador do buraco causador do dano :')
        idCidadao = user.identificador

        dano = Dano(tipoDeDano,pagamento,idBuraco,idCidadao)

        dano.inserir_dano_db()

    def modificar_dano(self, user):
        idDano = input('>> Insira o identificador do dano:\n> ')
        dano = self.retorna_dano_bd(idDano)
        if dano is None:
            print('>> Dano nao encontrado')
            return

        selection = {
            '1': 'atualizar_tipoDeDano',
            '2': 'atualizar_pagamento',
            '3': 'atualizar_idBuraco',
            '4': 'atualizar_idCidadao',
        }

        identificador_old = dano.idDano

        while 1:
            print(''' [ Bem vindo ao painel de atualizacao de dano ]\n [ Selecione o atributo a ser atualizado: ]
                                         1) Tipo de dano
                                         2) Pagamento
                                         3) Buraco que causou o dano
                                         4) Cidadao que recebeu o dano
                                         5) Sair
                                         ''')

            option = input("> ")

            if option == '5':
                break
            elif option == '2' :
                print('>> Insira o novo valor do atributo: ')
                novo_valor = int(input('> '))
                dano.atualizar_pagamento(novo_valor)
                print('> Valor atualizado!')

            else:
                print('>> Insira o novo valor do atributo: ')
                novo_valor = int(input('> '))
                try:
                    getattr(dano, selection[option])(novo_valor)
                    print('> Valor atualizado!')
                except KeyError:
                    print('Opcao invalida')

        #verificar se mudancas em dano repercutem em mudancas em outros registros

        print('Saindo do painel de atualizacao de buraco...')

    def excluir_dano(self, user):
        idDano = input('>> Insira o identificador do dano:\n> ')
        confirm = input('>> Deseja realmente excluir o dano ? [S/s]')
        if confirm == 'S' or confirm == 's':
            dano = self.retorna_dano_bd(idDano)
            dano.remover_dano_db()

        print('Voltando...')
        return

    def realizar_consulta_geral(self, user):
        print('[ Consulta geral ]')
        self.consultar_danos(user)

        db_cursor.execute("SELECT * FROM buraco WHERE registradoPor = :registradoPor ",
                          {'registradoPor': user.identificador})
        lst = db_cursor.fetchall()

        if not lst:
            print(">> Nenhum buraco encontrado")
            return

        for entry in lst:
            buraco = self.retorna_buraco_bd(entry[0])
            ordem = self.retorna_ordem_de_trabalho_bd(entry[0])
            reparo = self.retorna_reparo_bd(entry[0])
            if ordem is not None:
                if reparo is not None:
                    reparo.mostrar_reparo()
                else:
                    ordem.mostrar_ordem_de_trabalho()
            else:
                buraco.mostrar_buraco()

    def consultar_arquivos_de_dano(self, user):
        print('[ Arquivo de danos do usuario ]')
        self.consultar_danos(user)

    def gerar_relatorio(self,user):
        self.realizar_consulta_geral(user)
        #por enquanto assim ate definir a forma do relatorio
        #fazer o mesmo retorno porem em um arquivo ?

    def consultar_cadastro_funcionario(self, user):
        while 1:
            print('''[ Painel de consulta de cadastro ]
                        1) Consultar o proprio cadastro
                        2) Consultar outro cadastro
                        3) Sair
            ''')
            option = input('> ')
            if option == '1':
                user.mostrar_cadastro_funcionario()
            elif option == '2':
                identificador = input('>> Insira o identificador do usuario: \n> ')
                other_user = self.retorna_funcionario_bd(identificador)
                if other_user is None:
                    other_user = self.retorna_cidadao_bd(identificador)
                    other_user.mostrar_cadastro()
                else:
                    other_user.mostrar_cadastro_funcionario()
            elif option == '3':
                print('Saindo...')
                return
            else:
                print('>> Opcao invalida')


    def modificar_cadastro_funcionario(self, user):
        pass
    #deseja modificar o proprio cadastro ou de algum cidadao?
    #se cidadao self.modificar_cadastro_cidadao(cidadao)

    def excluir_cadastro_funcionario(self, user):
        pass

    def cadastrar_funcionario(self, user):
        print('''[ Painel de cadastro de funcionario ]''')
        identificador = input('>> Insira o identificador do cidadao a ser cadastrado como funcionario: \n> ')

        cidadao = self.retorna_cidadao_bd(identificador)

        if cidadao is None:
            print('>> Cidadao nao encontrado')
            return
        else:
            cargo = input('> Insira o cargo:')
            salario = input('> Insira o salario')
            funcionario = Funcionario(cidadao.nome, cidadao.cpf, cidadao.identidade, cidadao.filiacao, cidadao.sexo,
                                      cidadao.estadoCivil, cidadao.naturalidade, cidadao.endereco, cidadao.email,
                                      cidadao.profissao, cargo, salario)
            cidadao.atualizar_funcionario(True)
            funcionario.inserir_funcionario_db()


    def interface_material_de_reparo(self, user):
        pass

    def interface_ordem_de_trabalho(self, user):
        pass

    def interface_equipamento(self, user):
        pass

    def interface_equipe_de_reparo(self, user):
        pass

    def interface_reparo(self, user):
        pass

