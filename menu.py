import time
from app.usuario import create_usuario, read_usuario, update_usuario, delete_usuario
from app.vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from app.produto import create_produto, read_produto, update_produto, delete_produto
from app.compra import create_compra, read_compra, update_compra, delete_compra
from app.redis_sessao import (exigir_sessao, encerrar_sessao, sessao_expirou, ler_opcao,
                              mongo_para_redis, redis_para_mongo,
                              SessaoExpirada, SESSAO_ESPERA_LOGIN)
from app.redis_crud import create_item, read_itens, update_item, delete_item

# ================== MENU PRINCIPAL ==================
# EX3:
#  - o programa SEMPRE pede login ao abrir (a sessão anterior é encerrada);
#  - TODO acesso a um menu (principal ou submenu) verifica a sessão no Redis e mostra
#    na tela "[Sessão] verificada em '<menu>'";
#  - se a sessão expirar, o sistema faz logout (aviso na tela), descarta o que foi digitado
#    e exige novo login no próximo acesso. O programa não fecha.

encerrar_sessao()

key = 0
sub = 0
while (key != 'S'):
    try:
        if not exigir_sessao("Menu principal"):
            break

        print("\n1-CRUD Usuário")
        print("2-CRUD Vendedor")
        print("3-CRUD Produto")
        print("4-CRUD Compra")
        print("5-Mongo -> Redis")
        print("6-Redis -> Mongo")
        print("7-CRUD Redis (Favoritos e Endereços)")
        key = ler_opcao("\nDigite a opção desejada? (S para sair) ")
        if key is None or sessao_expirou():
            continue

        if (key == '1'):
            if not exigir_sessao("Menu do USUÁRIO"):
                break
            print("\nMenu do USUÁRIO")
            print("1-Create Usuário")
            print("2-Read Usuário")
            print("3-Update Usuário")
            print("4-Delete Usuário")
            sub = ler_opcao("\nDigite a opção desejada? (V para voltar) ")
            if sub is None or sessao_expirou():
                continue
            if (sub == '1'):
                print("Create usuario")
                create_usuario()

            elif (sub == '2'):
                nome = input("Read usuário, deseja algum nome especifico? ")
                read_usuario(nome)

            elif (sub == '3'):
                nome = input("Update usuário, deseja algum nome especifico? ")
                update_usuario(nome)

            elif (sub == '4'):
                print("delete usuario")
                nome = input("Nome a ser deletado: ")
                sobrenome = input("Sobrenome a ser deletado: ")
                delete_usuario(nome, sobrenome)

            elif (sub != 'V'):
                print("Opção inválida.")

        elif (key == '2'):
            if not exigir_sessao("Menu do VENDEDOR"):
                break
            print("\nMenu do VENDEDOR")
            print("1-Create Vendedor")
            print("2-Read Vendedor")
            print("3-Update Vendedor")
            print("4-Delete Vendedor")
            sub = ler_opcao("\nDigite a opção desejada? (V para voltar) ")
            if sub is None or sessao_expirou():
                continue
            if (sub == '1'):
                print("Create vendedor")
                create_vendedor()

            elif (sub == '2'):
                nome = input("Read vendedor, deseja algum nome especifico? ")
                cpf_cnpj = input("Ou algum CPF/CNPJ especifico? ")
                read_vendedor(nome, cpf_cnpj)

            elif (sub == '3'):
                nome = input("Update vendedor, deseja algum nome especifico? ")
                update_vendedor(nome)

            elif (sub == '4'):
                print("delete vendedor")
                nome = input("Nome a ser deletado: ")
                cpf_cnpj = input("CPF/CNPJ a ser deletado: ")
                delete_vendedor(nome, cpf_cnpj)

            elif (sub != 'V'):
                print("Opção inválida.")

        elif (key == '3'):
            if not exigir_sessao("Menu do PRODUTO"):
                break
            print("\nMenu do PRODUTO")
            print("1-Create Produto")
            print("2-Read Produto")
            print("3-Update Produto")
            print("4-Delete Produto")
            sub = ler_opcao("\nDigite a opção desejada? (V para voltar) ")
            if sub is None or sessao_expirou():
                continue
            if (sub == '1'):
                print("Create produto")
                create_produto()

            elif (sub == '2'):
                nome = input("Read produto, deseja algum nome especifico? ")
                categoria = input("Ou alguma categoria especifica? ")
                read_produto(nome, categoria)

            elif (sub == '3'):
                nome = input("Update produto, deseja algum nome especifico? ")
                update_produto(nome)

            elif (sub == '4'):
                print("delete produto")
                nome = input("Nome do produto a ser deletado: ")
                cnpj_vendedor = input("CPF/CNPJ do vendedor deste produto: ")
                delete_produto(nome, cnpj_vendedor)

            elif (sub != 'V'):
                print("Opção inválida.")

        elif (key == '4'):
            if not exigir_sessao("Menu de COMPRA"):
                break
            print("\nMenu de Compra")
            print("1-Create Compra")
            print("2-Read Compra")
            print("3-Update Compra")
            print("4-Delete Compra")
            sub = ler_opcao("\nDigite a opção desejada? (V para voltar) ")
            if sub is None or sessao_expirou():
                continue
            if (sub == '1'):
                print("Create compra")
                create_compra()

            elif (sub == '2'):
                cpf_usuario = input("Read compra, deseja algum CPF de usuário especifico? ")
                read_compra(cpf_usuario)

            elif (sub == '3'):
                compra_id = input("ID da compra a ser atualizada: ")
                update_compra(compra_id)

            elif (sub == '4'):
                print("delete compra")
                compra_id = input("ID da compra a ser deletada: ")
                delete_compra(compra_id)

            elif (sub != 'V'):
                print("Opção inválida.")

        # EX3: Mongo -> Redis (copia, o Mongo não perde nada)
        elif (key == '5'):
            if not exigir_sessao("Mongo -> Redis"):
                break
            print("\nMongo -> Redis (Favoritos e Endereços)")
            mongo_para_redis()

        # EX3: Redis -> Mongo (devolve os itens editados)
        elif (key == '6'):
            if not exigir_sessao("Redis -> Mongo"):
                break
            print("\nRedis -> Mongo (Favoritos e Endereços)")
            redis_para_mongo()

        # EX3: CRUD dos itens no Redis
        elif (key == '7'):
            if not exigir_sessao("Menu CRUD REDIS"):
                break
            print("\nMenu CRUD REDIS (Favoritos e Endereços)")
            print("1-Create item")
            print("2-Read itens")
            print("3-Update item")
            print("4-Delete item")
            sub = ler_opcao("\nDigite a opção desejada? (V para voltar) ")
            if sub is None or sessao_expirou():
                continue
            if (sub == '1'):
                create_item()

            elif (sub == '2'):
                read_itens()

            elif (sub == '3'):
                update_item()

            elif (sub == '4'):
                delete_item()

            elif (sub != 'V'):
                print("Opção inválida.")

        elif (key != 'S'):
            print("Opção inválida.")
    
    except SessaoExpirada:
        time.sleep(SESSAO_ESPERA_LOGIN)
        key = 0
        continue

encerrar_sessao()   # logout ao sair
print("Tchau Prof...")