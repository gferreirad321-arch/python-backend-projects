import pymysql

def conectar():
    try:
        print("Tentando conectar...")

        conexao = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='projeto_vendas_eletronicos_unifecaf'
        )

        print("Conectado com sucesso!")
        return conexao

    except Exception as e:
        print("ERRO AO CONECTAR:", e)
        return None


def fechar_conexao(conexao):
    try:
        if conexao:
            conexao.close()
            print("Conexão encerrada.")
    except Exception as e:
        print("ERRO AO FECHAR CONEXÃO:", e)