from app.usuario import create_usuario, read_usuario, update_usuario, delete_usuario
from app.vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from app.produto import create_produto, read_produto, update_produto, delete_produto
from app.compra import create_compra, read_compra, update_compra, delete_compra

# ================== MENU PRINCIPAL ==================

key = 0
sub = 0
while (key != 'S'):
    print("\n1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compra")
    key = input("\nDigite a opção desejada? (S para sair) ").strip().upper()

    if (key == '1'):
        print("\nMenu do USUÁRIO")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("\nDigite a opção desejada? (V para voltar) ").strip().upper()
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

    elif (key == '2'):
        print("\nMenu do VENDEDOR")
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("\nDigite a opção desejada? (V para voltar) ").strip().upper()
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
        
    elif (key == '3'):
        print("\nMenu do PRODUTO")
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("\nDigite a opção desejada? (V para voltar) ").strip().upper()

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
    
    elif (key == '4'):
            print("\nMenu de Compra")
            print("1-Create Compra")
            print("2-Read Compra")
            print("3-Update Compra")
            print("4-Delete Compra")
            sub = input("\nDigite a opção desejada? (V para voltar) ").strip().upper()
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

print("Tchau Prof...")
