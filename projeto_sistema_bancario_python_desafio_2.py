from time import sleep
from datetime import datetime
import os

LIMITE_SAQUES_POR_DIA = 3
LIMITE_SAQUE = 500
LIMITE_DE_OPERACOES_POR_DIA = 10
numero_da_conta = 1
lista_de_usuarios = []  # Lista de usuários cadastrados {cpf, nome, data_de_nascimento, endereco}
lista_de_contas = []  # Lista de contas cadastradas {cpf, agencia, conta, saldo, lista_de_operacoes: [(operacao, valor, data)]}

# Função para exibir o menu principal
def menu_principal():
    print(f"""
        ======= Bem-Vindo ao Sistema Bancário em Python! =======
        
        1 - Criar novo usuário
        2 - Entrar com usuário cadastrado
        3 - Listar usuários cadastrados
        4 - Listar contas cadastradas
        5 - Sair
    
    """)

# Função para exibir o menu de criação de usuário
def menu_criar_usuario(usuarios, contas):
    global numero_da_conta
    print(f"""
        ======= Criar novo usuário =======
        
    """)
    cpf = input("Digite o CPF do usuário (somente números): ")
    if usuario_cadastrado(cpf, usuarios):  # Verifica se o usuário já está cadastrado
        print("\n\nUsuário já cadastrado com esse CPF!")
        voltar_menu()
        return
    nome = input("Digite o nome do usuário: ")
    data_de_nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ")
    rua = input("Digite o nome da rua: ")
    numero = input("Digite o número da casa: ")
    bairro = input("Digite o nome do bairro: ")
    cidade = input("Digite o nome da cidade: ")
    estado = input("Digite a sigla do estado: ")
    endereco = f"{rua}, {numero} - {bairro} - {cidade}/{estado}"
    usuarios.append({"cpf": cpf, "nome": nome, "data_de_nascimento": data_de_nascimento, "endereco": endereco})
    contas.append({"cpf": cpf, "agencia": "0001", "conta": f"{numero_da_conta}", "saldo": 0.0, "lista_de_operacoes": []})
    numero_da_conta += 1
    print("\n\nUsuário cadastrado com sucesso!")
    voltar_menu()

# Função para verificar se o usuário já está cadastrado
def usuario_cadastrado(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False

# Função para exibir o menu de seleção de usuários cadastrados
def menu_usuario_cadastrado():
    print(f"""
        ======= Menu de seleção de usuário =======
        
        1 - Buscar usuário por nome
        2 - Buscar usuário por CPF
        3 - Voltar ao menu principal
    
    """)

# Função para exibir o menu de seleção de usuário por nome
def menu_usuario_por_nome(usuarios):
    print(f"""
        ======= Buscar usuário por nome =======
        
    """)
    nome = input("Digite o nome do usuário: ")
    usuario = buscar_usuario_por_nome(nome)
    if usuario:
        clear()
        return usuario
    else:
        print("\n\nUsuário não encontrado!")
        voltar_menu()

# Função para buscar usuário por Nome
def buscar_usuario_por_nome(nome):
    for usuario in lista_de_usuarios:
        if usuario["nome"] == nome:
            return usuario
    return None

# Função para exibir o menu de seleção de usuário por CPF
def menu_usuario_por_cpf(usuarios):
    print(f"""
        ======= Buscar usuário por CPF =======
        
    """)
    cpf = input("Digite o CPF do usuário (apenas números): ")
    usuario = buscar_usuario_por_cpf(cpf, usuarios)
    if usuario:
        clear()
        return usuario
    else:
        print("\n\nUsuário não encontrado!")
        voltar_menu()

# Funcão para buscar usuário por CPF
def buscar_usuario_por_cpf(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

# Função para exibir o menu de seleção de conta caso o usuário tenha mais de uma conta
def menu_conta_cadastrada(usuario, contas):
    contas = buscar_contas_por_usuario(usuario, contas)
    if len(contas) == 1:
        return contas[0]
    elif len(contas) > 1:
        numero_do_menu = 0
        print(f"""
            ======= Menu de seleção de conta =======
            
            0 - Voltar
        
        """)
        for conta in contas:
            print(f"    {numero_do_menu + 1} - Conta: {conta['conta']}/{conta['agencia']}")
            numero_do_menu += 1
        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            return None
        elif int(opcao) > 0 and int(opcao) <= len(contas):
            return contas[int(opcao) - 1]
        else:
            print("Opção inválida!")
            voltar_menu()

# Função para buscar as contas de um usuário
def buscar_contas_por_usuario(usuario, contas):
    contas_usuario = []
    for conta in contas:
        if conta["cpf"] == usuario["cpf"]:
            contas_usuario.append(conta)
    return contas_usuario

# Função para exibir o menu de operações do usuário
def menu_operacoes(usuario, conta):
    print(f"""
        ======= Bem vindo(a) {usuario["nome"]} Conta: {conta["conta"]}/{conta["agencia"]} =======
        
        1 - Realizar depósito
        2 - Realizar saque
        3 - Extrato bancário
        
        4 - Cadastrar nova conta
        5 - Excluir conta
        6 - Excluir usuário
        7 - Sair para o menu principal
    
    """)

# Função para exibir o menu de criação de conta
def menu_criar_conta():
    print(f"""
        ======= Criar nova conta =======
        
        1 - Criar nova conta
        2 - Voltar ao menu de operações
    
    """)

# Função para exibir o menu de exclusão de conta
def menu_excluir_conta():
    print(f"""
        ======= Excluir conta =======
        
        1 - Excluir conta
        2 - Voltar ao menu de operações
    
    """)

# Função para exibir o menu de exclusão de usuário
def menu_excluir_usuario():
    print(f"""
        ======= Excluir usuário =======
        
        1 - Excluir usuário
        2 - Voltar ao menu de operações
    
    """)

#Função para exibir o menu de confirmação de exclusão de conta
def menu_confirmacao_exclusao_conta(conta, agencia):
    print(f"""
        ======= Confirmar exclusão de conta {conta}/{agencia} =======
        
        1 - Confirmar exclusão de conta
        2 - Cancelar exclusão de conta
    
    """)

# Função para exibir o menu de confirmação de exclusão de usuário
def menu_confirmacao_exclusao_usuario(usuario):
    print(f"""
        ======= Confirmar exclusão de usuário {usuario} =======
        
        1 - Confirmar exclusão de usuário
        2 - Cancelar exclusão de usuário
    
    """)

# Função para limpar o console windows
def clear():
    os.system('cls||echo -e \\\\033c')

# Função para voltar ao menu anterior
def voltar_menu():
    print()
    input("Pressione ENTER para voltar ao menu anterior...")
    clear()

# Função para realizar um depósito
def deposito(conta, valor, /):
    if valor <= 0:
        print("Valor inválido!")
        voltar_menu()
        return
    elif pode_realizar_operacao(conta):
        conta["saldo"] += valor
        conta["lista_de_operacoes"].append(("deposito", valor, datetime.now()))
        print(f"Deposito de R$ {valor.__format__('0.2f')} realizado com sucesso!")
    else:
        print("Limite de operações por dia atingido!")
    voltar_menu()

# Função para realizar um saque
def saque(*, conta, valor):

    if limite_de_saques_por_dia(conta):
        print("Limite de saques por dia atingido!")
        voltar_menu()
        return
    elif valor > LIMITE_SAQUE:
        print(f"Valor de saque superior ao limite de R$ {LIMITE_SAQUE.__format__('0.2f')}")
        voltar_menu()
        return
    elif conta["saldo"] < valor:
        print("Saldo insuficiente!")
        voltar_menu()
        return
    elif valor <= 0:
        print("Valor inválido!")
        voltar_menu()
        return
    elif pode_realizar_operacao(conta):
        conta["saldo"] -= valor
        conta["lista_de_operacoes"].append(("saque", valor, datetime.now()))
        print(f"Saque de R$ {valor.__format__('0.2f')} realizado com sucesso!")
    voltar_menu()

# Função para determinar se o usuário ultrapassou o limite de saques por dia
def limite_de_saques_por_dia(conta):
    saques = []
    for operacao in conta["lista_de_operacoes"]:
        if operacao[0] == "saque":
            saques.append(operacao)
    if len(saques) >= LIMITE_SAQUES_POR_DIA:
        return True
    return False

# Função para exibir o extrato bancário
def extrato(usuario, /, *, conta):
    saldo = conta["saldo"]
    lista_de_operacao_realizada_saque_ou_deposito = conta["lista_de_operacoes"]
    clear()
    print("Extrato bancário")
    print()
    print("Operações realizadas:")
    print()

    for operacao_realizada in lista_de_operacao_realizada_saque_ou_deposito:
        if operacao_realizada[0] == "saque":
            print(f"- R$ {operacao_realizada[1].__format__('0.2f')} às {operacao_realizada[2].strftime('%d/%m/%Y %H:%M:%S')}")
        elif operacao_realizada[0] == "deposito":
            print(f"+ R$ {operacao_realizada[1].__format__('0.2f')} às {operacao_realizada[2].strftime('%d/%m/%Y %H:%M:%S')}")

    print()
    print(f"Saldo atual: R$ {saldo.__format__('0.2f')} às {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    voltar_menu()

# Função para determinar se o usuário pode realizar uma operação
def pode_realizar_operacao(conta):
    if len(conta["lista_de_operacoes"]) > LIMITE_DE_OPERACOES_POR_DIA:
        return False
    return True

# Função para criar uma nova conta
def criar_conta(contas, usuario):
    global numero_da_conta
    cpf = usuario["cpf"]
    contas.append({"cpf": cpf, "agencia": "0001", "conta": f"{numero_da_conta}", "saldo": 0.0, "lista_de_operacoes": []})
    numero_da_conta += 1
    print("\n\nConta cadastrada com sucesso!")
    voltar_menu()

# Função para excluir uma conta
def excluir_conta(usuario, contas):
    contas_usuario = buscar_contas_por_usuario(usuario, contas)
    conta = menu_conta_cadastrada(usuario, contas_usuario)
    clear()
    if conta:
        menu_confirmacao_exclusao_conta(conta["conta"], conta["agencia"])
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            contas.remove(conta)
            print("\nConta excluída com sucesso!")
            voltar_menu()
        elif opcao == '2':
            pass
        else:
            print("Opção inválida!")
            voltar_menu()

# Função para excluir um usuário
def excluir_usuario(usuario, usuarios, contas):
    menu_confirmacao_exclusao_usuario(usuario["nome"])
    opcao = input("Escolha uma opção: ")
    if opcao == '1':
        usuarios.remove(usuario)
        contas_usuario = buscar_contas_por_usuario(usuario, contas)
        for conta in contas_usuario:
            contas.remove(conta)
        print("\nUsuário excluído com sucesso!")
        voltar_menu()
    elif opcao == '2':
        pass
    else:
        print("Opção inválida!")
        voltar_menu()

# Função para listar os usuários cadastrados
def listar_usuarios(usuarios):
    print(f"""
        ======= Lista de usuários cadastrados =======
        
    """)
    for usuario in usuarios:
        print(f"CPF: {usuario['cpf']} - Nome: {usuario['nome']} - Data de nascimento: {usuario['data_de_nascimento']} - Endereço: {usuario['endereco']}")
    voltar_menu()

# Função para listar as contas cadastradas
def listar_contas(contas):
    print(f"""
        ======= Lista de contas cadastradas =======
        
    """)
    for conta in contas:
        print(f"CPF: {conta['cpf']} - Agência: {conta['agencia']} - Conta: {conta['conta']} - Saldo: R$ {conta['saldo'].__format__('0.2f')}")
    voltar_menu()


# Loop principal
while True:
    clear()
    menu_principal()
    opcao = input("Escolha uma opção: ")
    if opcao == '1':
        clear()
        menu_criar_usuario(lista_de_usuarios, lista_de_contas)
    elif opcao == '2':
        clear()
        menu_usuario_cadastrado()
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            clear()
            usuario = menu_usuario_por_nome(lista_de_usuarios)
            conta = menu_conta_cadastrada(usuario, lista_de_contas)
            while opcao != '7':
                clear()
                menu_operacoes(usuario, conta)
                opcao = input("Escolha uma opção: ")
                if opcao == '1':
                    valor = float(input("\nDigite o valor do depósito: "))
                    deposito(conta, valor)
                elif opcao == '2':
                    valor = float(input("\nDigite o valor do saque: "))
                    saque(conta=conta, valor=valor)
                elif opcao == '3':
                    extrato(usuario, conta=conta)
                elif opcao == '4':
                    clear()
                    menu_criar_conta()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        criar_conta(lista_de_contas, usuario)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '5':
                    clear()
                    menu_excluir_conta()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        excluir_conta(usuario, lista_de_contas)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '6':
                    clear()
                    menu_excluir_usuario()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        excluir_usuario(usuario, lista_de_usuarios, lista_de_contas)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '7':
                    clear()
                    break
                else:
                    print("Opção inválida!")
                    voltar_menu()
        elif opcao == '2':
            clear()
            usuario = menu_usuario_por_cpf(lista_de_usuarios)
            conta = menu_conta_cadastrada(usuario, lista_de_contas)
            while opcao != '7':
                clear()
                menu_operacoes(usuario, conta)
                opcao = input("Escolha uma opção: ")
                if opcao == '1':
                    valor = float(input("\nDigite o valor do depósito: "))
                    deposito(conta, valor)
                elif opcao == '2':
                    valor = float(input("\nDigite o valor do saque: "))
                    saque(conta=conta, valor=valor)
                elif opcao == '3':
                    extrato(usuario, conta=conta)
                elif opcao == '4':
                    clear()
                    menu_criar_conta()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        criar_conta(lista_de_contas, usuario)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '5':
                    clear()
                    menu_excluir_conta()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        excluir_conta(usuario, lista_de_contas)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '6':
                    clear()
                    menu_excluir_usuario()
                    opcao = input("Escolha uma opção: ")
                    if opcao == '1':
                        clear()
                        excluir_usuario(usuario, lista_de_usuarios, lista_de_contas)
                    elif opcao == '2':
                        clear()
                        pass
                    else:
                        print("Opção inválida!")
                        voltar_menu()
                elif opcao == '7':
                    clear()
                    break
                else:
                    print("Opção inválida!")
                    voltar_menu()
        elif opcao == '3':
            clear()
            break
        else:
            print("Opção inválida!")
            voltar_menu()
    elif opcao == '3':
        clear()
        listar_usuarios(lista_de_usuarios)
    elif opcao == '4':
        clear()
        listar_contas(lista_de_contas)
    elif opcao == '5':
        print("Saindo do sistema...")
        sleep(2)
        exit()
    else:
        print("Opção inválida!")
        voltar_menu()