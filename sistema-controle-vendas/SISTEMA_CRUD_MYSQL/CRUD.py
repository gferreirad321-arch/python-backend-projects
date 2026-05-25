# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026

from conexao import conectar, fechar_conexao

# PRODUTOS

def criar_produto():
    # Exercicio 1: cadastrar um novo produto na tabela produtos (descricao, preco).

    try:
        
        conexao = conectar()

        print('==== CADASTRO DE PRODUTO ====') 

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'

        cursor = conexao.cursor()

        descricao_prod = input('Digite a descrição do produto: ')
        preco_prod = float(input('Digite o valor do produto: '))

        query = '''
        INSERT INTO produtos (descricao, preco)
        VALUES (%s, %s)
        '''

        cursor.execute(query, (descricao_prod, preco_prod))
        conexao.commit()

        cursor.close()
        fechar_conexao(conexao)

        return f'Produto {descricao_prod}, R$ {preco_prod} cadastrado com sucesso!'

    except Exception as erro:
        return f'Erro: {erro}'
        

def listar_produtos():
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.

    try:
        conexao = conectar()

        print('==== LISTAGEM DE PRODUTOS ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        query = '''
            SELECT id, descricao, preco FROM produtos
        '''

        cursor.execute(query)

        resultado = cursor.fetchall()
        
        for produto in resultado:
            print(f'''
                ID: {produto[0]}
                DESCRIÇÃO: {produto[1]}
                PREÇO: {produto[2]:.2f}
            ''')
        
        cursor.close()

        fechar_conexao(conexao)
    
    except Exception as erro:
        return f'Erro: {erro}'


def atualizar_produto():
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.
    
    try:
        conexao = conectar()

        print('==== ATUALIZE UM PRODUTO ====')

        if conexao is None:
            return 'Erro ao seu conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        descricao = input('Atualize a descricao do produto: ')
        preco = input('Atualize o preço do produto (opcional): ')
        id_produto = int(input('Atualize o id de um produto: '))

        if preco == '':

            query = '''
                UPDATE produtos
                SET descricao = %s
                WHERE id = %s
            '''

            cursor.execute(query, (descricao, id_produto))

            preco = None

        else:
            preco = float(preco)

            query = '''
                UPDATE produtos
                SET descricao = %s, preco = %s
                WHERE id = %s
            '''
            
            cursor.execute(query, (descricao, preco, id_produto))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'''
            Produto atualizado com sucesso!

            Nova descrição: {descricao}
            Novo preço: {'Não alterado' if preco is None else f'R$ {preco:.2f}'}
        '''

    except Exception as erro:
        return f'Erro: {erro}'


def excluir_produto():
    # Exercicio 4: excluir um produto por id, tratando dependencias em vendas_produtos.

    try:
        conexao = conectar()

        print('==== EXCLUSÃO DE PRODUTO ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_produto = int(input('Digite o id do produto que desejas excluir: '))

        query = '''
            DELETE FROM vendas_produtos
            WHERE id_produto = %s
            '''

        query_produto = '''
            DELETE FROM produtos
            WHERE id = %s
            '''
        
        cursor.execute(query, (id_produto,))

        cursor.execute(query_produto, (id_produto,))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'Produto {id_produto} excluido com sucesso!'
    
    except Exception as erro:
        return f'Erro: {erro}'


# VENDEDORES

def criar_vendedor():
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.

    try:
        conexao = conectar()

        print('==== CADASTRO DE VENDEDORES ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        novo_vendedor = input('Digite o nome do vendedor a ser cadastrado: ')

        query = '''
            INSERT INTO vendedores (nome)
            VALUES (%s)
            '''
        
        cursor.execute(query, (novo_vendedor,))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'Novo vendedor cadastrado: {novo_vendedor}'
    
    except Exception as erro:
        return f'Erro: {erro}'


def listar_vendedores():
    # Exercicio 6: listar todos os vendedores cadastrados.
   
    try:
       conexao = conectar()

       print('==== LISTA DE VENDEDORES ====')

       if conexao is None:
           return 'Erro ao se conectar com Banco MySQL.'
       
       cursor = conexao.cursor()

       query = '''
            SELECT id, nome FROM vendedores
        '''
       
       cursor.execute(query)

       resultado = cursor.fetchall()

       for vendedor in resultado:
           print(f'''
            ID: {vendedor[0]}
            Nome: {vendedor[1]}
            ''')
       
       cursor.close()

       fechar_conexao(conexao)

    except Exception as erro:
        return f'Erro: {erro}'


def atualizar_vendedor():
    # Exercicio 7: atualizar o nome de um vendedor existente por id.

    try:
        conexao = conectar()

        print('==== ATUALIZAR VENDEDOR ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_vendedor = int(input('Digite o ID do vendedor: '))
        novo_vendedor = input('Atualize o nome do vendedor: ')

        query = '''
            UPDATE vendedores
            SET nome = %s
            WHERE id = %s
        '''

        cursor.execute(query, (novo_vendedor, id_vendedor))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'''
            Vendedor atualizado!

            ID: {id_vendedor}
            Novo vendedor: {novo_vendedor}
        '''
    
    except Exception as erro:
        return f'Erro: {erro}'


def excluir_vendedor():
    # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    try:
        conexao = conectar()

        print('==== EXCLUSÃO DE VENDEDOR ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_vendedores = int(input('Digite ID que deseja excluir: '))

        query_verificacao = '''
            SELECT * FROM vendas
            WHERE id_vendedor = %s
            '''
        
        cursor.execute(query_verificacao, (id_vendedores,))

        resultado = cursor.fetchone()

        if resultado:
            cursor.close()
            fechar_conexao(conexao)
            return 'Não é possível excluir esse vendedor, pois existem vendas vinculadas.'

        query = '''
            DELETE FROM vendedores
            WHERE id = %s
            '''
        
        cursor.execute(query, (id_vendedores,))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'Vendedor {id_vendedores} excluido com sucesso!'
    
    except Exception as erro:
        return f'Erro: {erro}'


# VENDAS

def criar_venda_com_itens():
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.

    try:
        conexao = conectar()

        print('==== CRIAÇÃO DE VENDA ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_vendedor = int(input('Informe o ID do vendedor: '))
        data_e_hora = str(input('Informe data e hora da venda: '))
        desconto = (input('Informe o valor de desconto: '))
        if desconto ==  '':
            desconto = None
        else:
            desconto = float(desconto)

        valor_final = float(input('Informe o valor final: '))

        query_venda = '''
            INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final)
            VALUES (%s, %s, %s, %s)
            '''
        
        cursor.execute(query_venda, (id_vendedor, data_e_hora, desconto, valor_final,))

        id_venda = cursor.lastrowid

        id_produto = int(input('Informe ID do produto: '))
        quantidade = int(input('Informe quantidade vendida: '))
        valor_unitario = float(input('Informe valor unitário: '))
        valor_total = quantidade * valor_unitario

        query = '''
            INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total)
            VALUES (%s, %s, %s, %s, %s)
            '''
        
        cursor.execute(query, (id_venda, id_produto, quantidade, valor_unitario, valor_total,))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'''
            Venda cadastrada:
            
            ID venda: {id_venda}
            ID produto: {id_produto}
            Quantidade: {quantidade}
            Valor unitário: {valor_unitario:.2f}
            Valor final: {valor_final:.2f}
            '''
    
    except Exception as erro:
        return f'Erro: {erro}'
    

def listar_vendas_completas():
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).

    try:
        conexao = conectar()

        print('==== LISTAGEM DE VENDAS ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'

        cursor = conexao.cursor()

        query = '''
            SELECT
            vendedores.nome,
            produtos.descricao, 
            vendas_produtos.quantidade,
            vendas_produtos.valor_unitario,
            vendas_produtos.valor_total
            FROM vendas INNER JOIN vendedores
                ON vendas.id_vendedor = vendedores.id
            INNER JOIN vendas_produtos
                ON vendas.id = vendas_produtos.id_venda
            INNER JOIN produtos
                ON vendas_produtos.id_produto = produtos.id
            '''
        
        cursor.execute(query)
        
        resultado = cursor.fetchall()

        cursor.close()

        fechar_conexao(conexao)

        for vendas_produtos in resultado:
            print(f'''
                  Lista de vendas:
                  
                  Vendedores: {vendas_produtos[0]}
                  Produtos: {vendas_produtos[1]}
                  Quantidades: {vendas_produtos[2]}
                  Valor unitário: {vendas_produtos[3]}
                  Valor total: {vendas_produtos[4]}    
                  ''')

    except Exception as erro:
        return f'Erro: {erro}'


def atualizar_venda_e_itens():
    # Exercicio 11: atualizar dados da venda (desconto/valor_final) e seus itens.

    try:
        conexao = conectar()

        print('==== ATUALIZAR VENDA E ITENS ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_venda = int(input('Digite o ID da venda: '))
        id_produto = int(input('Digite o ID do produto: '))
        
        novo_desconto = float(input('Informe o novo desconto: '))
        novo_valor_final = float(input('Informe o novo valor final: '))

        query_vendas = '''
            UPDATE vendas
            SET desconto = %s, valor_final = %s
            WHERE id = %s
            '''

        cursor.execute(query_vendas, (novo_desconto, novo_valor_final, id_venda))

        nova_quantidade = int(input('Informe nova quantidade: '))
        novo_valor_unitario = float(input('Informe o novo valor unitario: '))
        novo_valor_total = nova_quantidade * novo_valor_unitario


        query_itens = '''
            UPDATE vendas_produtos
            SET quantidade = %s, valor_unitario = %s, valor_total = %s
            WHERE id_venda = %s
            AND id_produto = %s
            '''
        
        cursor.execute(query_itens, (nova_quantidade, novo_valor_unitario, novo_valor_total, id_venda, id_produto))

        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'''
            Venda atualizada com sucesso!:

            ID venda: {id_venda}
            ID produto: {id_produto}
            Novo desconto: R$ {novo_desconto:.2f}
            Novo valor final: R$ {novo_valor_final:.2f}
            '''
    
    except Exception as erro:
        return f'Erro: {erro}'

      
def excluir_venda():
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    
    try:
        conexao = conectar()

        print('==== EXCLUSÃO DE VENDA ====')

        if conexao is None:
            return 'Erro ao se conectar com Banco MySQL.'
        
        cursor = conexao.cursor()

        id_venda = int(input('Informe o ID da venda que deseja excluir: '))

        query_venda_produto = '''
                    DELETE FROM vendas_produtos
                    WHERE id_venda = %s
                '''
        
        cursor.execute(query_venda_produto, (id_venda,))

        query_venda = '''
                DELETE FROM vendas
                WHERE id = %s
            '''
        
        cursor.execute(query_venda, (id_venda,))
        
        conexao.commit()

        cursor.close()

        fechar_conexao(conexao)

        return f'Venda {id_venda} excluida com sucesso!'

    except Exception as erro:
        return f'Erro: {erro}'


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Sair")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")

            try:
                retorno = funcao()

                if retorno is not None:
                    print(retorno)

            except Exception as erro:
                print(f"Erro na execução: {erro}")

            input("\nENTER para continuar...")

        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu()