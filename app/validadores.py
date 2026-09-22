import re


def ler_sim_nao(msg):
    while True:
        valor = input(msg).strip().upper()    # strip() remove espaço
        if valor in ('S', 'N'):
            return valor
        print("Opção inválida! Digite apenas S ou N.")


def ler_texto(msg):
    while True:
        valor = input(msg).strip()
        if valor and valor.replace(' ', '').isalpha():  # isalpha() valida letra
            return valor
        print("Valor inválido! Digite apenas letras e espaços.")


def ler_numero(msg, qtd=None):
    while True:
        valor = input(msg).strip()
        if valor.isdigit() and (qtd is None or len(valor) == qtd):  # isdigit valida núm
            return valor
        if qtd is not None:
            print(f"Valor inválido! Digite exatamente {qtd} números.")
        else:
            print("Valor inválido! Digite apenas números.")


def ler_cpf(msg):
    while True:
        valor = input(msg).strip()
        if valor.isdigit() and len(valor) == 11:
            return valor
        print("CPF inválido! Digite 11 números.")


def cpf_cnpj_valido(valor):
    valor = valor.upper()
    if valor.isdigit() and len(valor) == 11:
        return True
    if len(valor) == 14 and re.fullmatch(r'[A-Z0-9]{12}[0-9]{2}', valor):
        return True
    return False


def ler_cpf_cnpj(msg):
    while True:
        valor = input(msg).strip().upper()
        if cpf_cnpj_valido(valor):
            return valor
        print("CPF/CNPJ inválido! CPF: 11 números. CNPJ: 14 caracteres (12 alfanuméricos + 2 dígitos verificadores numéricos).")


def ler_logradouro(msg):
    while True:
        valor = input(msg).strip()
        if valor and any(ch.isalpha() for ch in valor):
            return valor
        print("Logradouro inválido! Digite um endereço válido.")


def ler_cep(msg):
    while True:
        valor = input(msg).strip()
        if valor.isdigit() and len(valor) == 8:
            return valor
        print("CEP inválido! Digite 8 números.")


def ler_telefone(msg):
    while True:
        valor = input(msg).strip()
        if valor.isdigit():
            return valor
        print("Telefone inválido! Digite apenas números.")