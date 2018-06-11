import sqlite3

conn = sqlite3.connect('srcb.db')

c = conn.cursor()

c.execute("""CREATE TABLE cidadao (
identificador text,
nome text,
cpf text,
identidade text,
filiacao text,
sexo text,
estadoCivil text,
naturalidade text,
endereco text,
email text,
profissao text,
funcionario integer,
recebeuDano integer
)""")

c.execute("""CREATE TABLE funcionario(
identificador TEXT,
nome TEXT,cpf TEXT, identidade TEXT, filiacao TEXT,
 sexo TEXT, estadoCivil TEXT, naturalidade TEXT, endereco TEXT, email TEXT,
                 profissao TEXT, funcionario INTEGER, recebeuDano INTEGER, codigo TEXT, cargo TEXT, salario TEXT
)""")

c.execute("""CREATE TABLE dano(
idDano text, tipoDeDano text, pagamento text, idBuraco text, idCidadao text
)""")

c.execute("""CREATE TABLE buraco(
identificador TEXT, endereco TEXT, tamanho INTEGER, localizacao TEXT, prioridade INTEGER, registradoPor TEXT
)""")

c.execute("""CREATE TABLE ordemDeTrabalho(
identificador text, endereco text, tamanho integer, localizacao text, prioridade integer,
 registradoPor text, codigo text, descricao text,
                 situacao text, equipeDeReparo text, equipamentos text, horasAplicadas integer
)""")


#c.executescript('drop table if exists reparo;')

c.execute("""CREATE TABLE reparo(
identificador TEXT, endereco TEXT, tamanho INTEGER, localizacao TEXT, prioridade INTEGER, registradoPor TEXT,
 codigo TEXT, descricao TEXT, situacao TEXT,
                 equipeDeReparo TEXT, equipamentos TEXT, horasAplicadas INTEGER, codigoReparo TEXT,
                  descricaoReparo TEXT, status TEXT, materialUtilizado TEXT,
                 custo INTEGER
)""")

c.execute("""CREATE TABLE equipeDeReparo (
identificador TEXT, numeroDePessoas INTEGER, funcionarios TEXT
)""")

c.execute("""CREATE TABLE equipamento(
codigo text, descricao text, fabricante text, tamanho integer, peso integer
)""")

c.execute("""CREATE TABLE material(
codigo TEXT, descricao TEXT, valor INTEGER, quantidade INTEGER, tipo TEXT
)""")

conn.commit()

conn.close()