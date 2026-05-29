import requests

from App import TipoAtivo, Severidades, Status
from utils import escolher_enum


# CRIAR ATIVO

def criar_ativo_terminal():

    tipo_ativo = escolher_enum(TipoAtivo, "TIPO DE ATIVO")
    if not tipo_ativo:
        return

    hostname = input("Hostname: ")
    responsavel = input("Responsável: ")
    setor = input("Setor: ")


    dados = {
        "hostname": hostname,
        "responsavel": responsavel,
        "setor": setor,
        "notebook": None,
        "servidor": None,
        "roteador": None,
        "sistema_interno": None,
        "software_licenciado":None,
        "tipo_ativo": tipo_ativo
    }

    if tipo_ativo==TipoAtivo.NOTEBOOK.value:
        dados['notebook']=input('Qual o notebook: ')
    elif tipo_ativo==TipoAtivo.SERVIDOR.value:
        dados['servidor']=input('Qual o servidor: ')
    elif tipo_ativo==TipoAtivo.ROTEADOR.value:
        dados['roteador']=input('Qual o roteador: ')
    elif tipo_ativo==TipoAtivo.SISTEMA_INTERNO.value:
        dados['sistema_interno']=input('Qual o sistema interno: ')
    elif tipo_ativo==TipoAtivo.SOFTWARE_LICENCIADO.value:
        dados['software_licenciado']=input('Qual o software licenciado: ')

    print(dados)

    resposta = requests.post(
        "http://127.0.0.1:5000/ativos",
        json=dados
    )

    print(resposta.json())


# ATUALIZAR ATIVO

def criar_atualizar_ativo_terminal():

    id_ativo = input('Qual o id: ')

    tipo_ativo = escolher_enum(TipoAtivo, "TIPO DE ATIVO")
    if not tipo_ativo:
        return

    notebook = input('Qual o notebook: ')
    servidor = input('Qual o servidor: ')
    roteador = input('Qual o roteador: ')
    sistema_interno = input('Qual o sistema interno: ')
    software_licenciado = input('Qual o software licenciado: ')

    dados = {
        "notebook": notebook,
        "servidor": servidor,
        "roteador": roteador,
        "sistema_interno": sistema_interno,
        "software_licenciado": software_licenciado,
        "tipo_ativo": tipo_ativo
    }

    resposta = requests.put(
        f"http://127.0.0.1:5000/ativos/{id_ativo}",
        json=dados
    )

    print(resposta.json())


# DELETAR ATIVO

def criar_deletar_ativo():

    id_ativo = input('Qual o id para deletar: ')

    resposta = requests.delete(
        f"http://127.0.0.1:5000/ativos/{id_ativo}"
    )

    print(resposta.json())

# LISTAR ATIVOS

def criar_listar_ativo():

    resposta = requests.get("http://127.0.0.1:5000/ativos")

    print(resposta.json())

# CRIAR VULNERABILIDADE

def criar_vulnerabilidades_terminal():

    descricao = input('Qual a descrição: ')
    categoria= input('Qual a categoria: ')
    ativo_id = input('Qual o ID do ativo: ')

    severidade = escolher_enum(Severidades, "SEVERIDADE")
    if not severidade:
        return

    status = escolher_enum(Status, "STATUS")
    if not status:
        return

    dados = {
        "descricao": descricao,
        "severidade": severidade,
        "status": status,
        "categoria":categoria,
        "ativo_id": ativo_id
    }

    resposta = requests.post(
        "http://127.0.0.1:5000/vulnerabilidades",
        json=dados
    )

    print(resposta.json())


# LISTAR VULNERABILIDADES

def criar_lista_vulnerabilidades_terminal():

    id_ativo = input('Qual o ID do ativo: ')

    resposta = requests.get(
        f"http://127.0.0.1:5000/vulnerabilidades/{id_ativo}"
    )

    print(resposta.json())

# MENU

while True:

    print('\n1 - criar ativo')
    print('2 - atualizar ativo')
    print('3 - deletar ativo')
    print('4 - listar ativos')
    print('5 - criar vulnerabilidade')
    print('6 - listar vulnerabilidades')
    print('0 - sair')

    opcao = input('Escolha uma opção: ')

    if opcao == '1':
        criar_ativo_terminal()

    elif opcao == '2':
        criar_atualizar_ativo_terminal()

    elif opcao == '3':
        criar_deletar_ativo()

    elif opcao == '4':
        criar_listar_ativo()

    elif opcao == '5':
        criar_vulnerabilidades_terminal()

    elif opcao == '6':
        criar_lista_vulnerabilidades_terminal()

    elif opcao == '0':
        break

    else:
        print('Opção inválida')