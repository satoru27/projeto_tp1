from myClassFile import *
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="ativa o modo de debug", action="store_true")
args = parser.parse_args()

def main():
    #admin = Funcionario(identificador = 000, nome = 'admin', cpf = '000.000.000.00', identidade = '123456789', filiacao = 'nenhuma', sexo = 'N', estadoCivil = 'solteiro', naturalidade ='Brasileira',
    #                    endereco = 'Lugar Nenhum', email = 'admin@meusite.com', profissao = 'administrador', funcionario = True, recebeuDano = False, codigo = '000', cargo = 'admin', salario = '00000')

    #admin.mostrarCadastroFuncionario()

    if args.debug:
        print("Rodando SRCB em modo de debug")
        sistema = SRCB(debugCode=1)
    else:
        sistema = SRCB(debugCode=0)

    sistema.interfacePrincipal()

if __name__ == "__main__":
    main()