# Avaliação Continuada 3 - 1 ponto
# PROJETO DE VENDAS - parte 1
# Exercicios de estatisticas de vendas.
# Entrega - dia 17/05/2026


from banco import conectar, fechar_conexao


def total_vendas_periodo():
    # Exercicio 1: calcular o valor total vendido em um periodo usando vendas.valor_final.
    #tenta executar o bloco abaixo
    try:
        conexao = conectar()

        if conexao is None:
            return 'Erro ao conectar com o Banco MySQL!'

        # cursor -> executar comandos do SQL
        cursor = conexao.cursor()

        # Guarda o comando SQL dentro da variável query
        query = '''
        SELECT SUM(valor_final)
        FROM  vendas
        '''

        cursor.execute(query)
        resultado = cursor.fetchone()
        total = resultado[0]

        fechar_conexao(conexao)
        return f'Valor total vendido foi de R$ {total:.2f}'
    
    except Exception as erro:
        return f'Erro para gerar o relatório: {erro}'


def qtd_vendas_por_vendedor():
    # Exercicio 2: contar quantas vendas cada vendedor realizou usando vendas.id_vendedor.
    try:
        conexao = conectar()

        if conexao is None:
            return 'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = '''
        SELECT id_vendedor, COUNT(*)
        FROM vendas
        GROUP BY id_vendedor
        '''

        cursor.execute(query)

        # pega todos os resultados da consulta
        resultados = cursor.fetchall()
        fechar_conexao(conexao)

        relatorio = 'Quantidade de vendas por vendedor: '
        for vendedor, quantidade in resultados:
            relatorio += f'Vendedor {vendedor}: {quantidade} vendas'

        return relatorio

    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'



def ticket_medio_geral():
    # Exercicio 3: calcular o ticket medio geral a partir de vendas.valor_final.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT AVG(valor_final) FROM vendas '''

        cursor.execute(query)

        # pega o resultado da consulta
        resultados = cursor.fetchone()

        ticket_medio = resultados[0]

        fechar_conexao(conexao)

        ticket = f'Valor do ticket médio geral: R$ {ticket_medio:.2f}'
        return ticket

         # caso aconteça algum erro
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'



def ticket_medio_por_vendedor():
    # Exercicio 4: calcular o ticket medio de cada vendedor cruzando vendas e vendedores.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT vendedores.nome, AVG(vendas.valor_final) FROM vendas
        INNER JOIN vendedores ON vendas.id_vendedor= vendedores.id
        GROUP BY vendedores.nome '''

        cursor.execute(query)

        resultados = cursor.fetchall()
        fechar_conexao(conexao)

        ticket = 'Ticket médio por vendedor:'

        for vendedor, media in resultados:
            ticket += f'{vendedor}: R$ {media:.2f}'

        return ticket
    
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'



def produto_mais_vendido_qtd():
    # Exercicio 5: identificar o produto mais vendido por quantidade em vendas_produtos.
    try: 
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT id_produto, SUM(quantidade) AS total_vendido
        FROM vendas_produtos
        GROUP BY id_produto
        ORDER BY total_vendido DESC LIMIT 1 '''

        cursor.execute(query)

        resultados = cursor.fetchone()
        id_produto = resultados[0]
        quantidade = resultados[1]

        fechar_conexao(conexao)

        return f'Produto mais vendido: {id_produto} com {quantidade} vendas'

    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'





def produto_mais_rentavel_valor():
    # Exercicio 6: identificar o produto que gerou maior faturamento somando vendas_produtos.valor_total.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT id_produto, SUM(valor_total) AS faturamento
        FROM vendas_produtos
        GROUP BY id_produto
        ORDER BY faturamento DESC
        LIMIT 1 '''

        cursor.execute(query)

        resultados = cursor.fetchone()
        id_produto = resultados[0]
        valor_total = resultados[1]
        fechar_conexao(conexao)

        return f'Produto com maior faturamento: {id_produto} com R$ {valor_total:.2f}'
    
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'




def total_descontos_aplicados():
    # Exercicio 7: somar todos os descontos concedidos usando vendas.desconto.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT SUM(desconto) FROM vendas '''

        cursor.execute(query)

        resultados = cursor.fetchone()
        descontos = resultados[0]
        fechar_conexao(conexao)

        return f'Descontos concedidos: R$ {descontos:.2f}'
    
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'


def percentual_desconto_medio():
    # Exercicio 8: calcular o percentual medio de desconto comparando desconto e valor_final das vendas.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT AVG((desconto / valor_final) * 100) FROM vendas '''

        cursor.execute(query)

        resultados = cursor.fetchone()
        percentual = resultados[0]
        fechar_conexao(conexao)

        return f'Percentual médio de desconto: {percentual:.2f}%'
    
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'
    


def faturamento_por_dia():
    # Exercicio 9: agrupar o faturamento por dia com base em vendas.data_e_hora e vendas.valor_final.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com o Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT DATE(data_e_hora), SUM(valor_final) FROM vendas
        GROUP BY DATE(data_e_hora)'''

        cursor.execute(query)

        resultados = cursor.fetchall()

        fechar_conexao(conexao)
        faturamento = 'Faturamento diário: '


        for data, valor in resultados:
            faturamento += f'{data}: R$ {valor:.2f} / '

        return faturamento
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'



def top_3_vendedores_faturamento():
    # Exercicio 10: listar os 3 vendedores com maior faturamento total no periodo.
    try:
        conexao = conectar()

        if conexao is None:
            return f'Erro ao conectar com Banco MySQL!'
        
        cursor = conexao.cursor()

        query = ''' SELECT vendedores.nome, SUM(vendas.valor_final) AS faturamento FROM vendas
                    INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id
                    GROUP BY vendedores.nome
                    ORDER BY faturamento DESC
                    LIMIT 3'''

        cursor.execute(query)
        
        resultados = cursor.fetchall()
        fechar_conexao(conexao)

        vendedores = 'Os 3 melhores vendedores: '

        for nome, faturamento in resultados:
            vendedores += f'{nome}: R$ {faturamento:.2f} / '

        return vendedores
    except Exception as erro:
        return f'Erro para gerar relatório: {erro}'



def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            resultado = funcao()

            if resultado is None:
                print("Relatorio em estrutura base (return vazio).")
            else:
                print(resultado)
        else:
            print("Opcao invalida. Tente novamente.")


menu_relatorios()