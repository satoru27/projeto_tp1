import argparse
import hashlib

from SRCB import SRCB

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="ativa o modo de debug", action="store_true")
args = parser.parse_args()

def main():
    if args.debug:
        print("Rodando SRCB em modo de debug")
        sistema = SRCB(debugCode=1)
    else:
        sistema = SRCB(debugCode=0)

    sistema.interface_principal()

if __name__ == "__main__":
    main()